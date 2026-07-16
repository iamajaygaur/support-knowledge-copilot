from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from rich.console import Console

from knowledge_copilot.config import get_settings
from knowledge_copilot.eval.metrics import (
    citation_support_rate,
    refusal_correct,
)
from knowledge_copilot.retrieve.pipeline import retrieve
from knowledge_copilot.service import ask

console = Console()


@dataclass
class GoldenItem:
    id: str
    question: str
    category: str
    relevant_sources: list[str] = field(default_factory=list)
    expect_no_answer: bool = False
    notes: str = ""


@dataclass
class EvalResult:
    item: GoldenItem
    strategy: str
    retrieved_sources: list[str]
    recall_at_5: float
    mrr: float
    correct_source: float
    citation_support: float
    refusal_ok: float
    confidence: float
    no_answer: bool
    answer: str


def load_golden(path: Path) -> list[GoldenItem]:
    items: list[GoldenItem] = []
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            data = json.loads(line)
            items.append(GoldenItem(**data))
    return items


def _source_keys(path_or_name: str) -> set[str]:
    lowered = path_or_name.lower().replace("\\", "/")
    return {lowered, Path(lowered).name, Path(lowered).stem}


def _matches_relevant(source: str, relevant_labels: list[str]) -> bool:
    keys = _source_keys(source)
    return any(keys & _source_keys(label) for label in relevant_labels)


def _correct_source_at_k(retrieved_sources: list[str], relevant_labels: list[str], k: int = 5) -> float:
    if not relevant_labels:
        return 0.0
    return 1.0 if any(_matches_relevant(src, relevant_labels) for src in retrieved_sources[:k]) else 0.0


def _recall_at_k(retrieved_sources: list[str], relevant_labels: list[str], k: int = 5) -> float:
    if not relevant_labels:
        return 0.0
    top = retrieved_sources[:k]
    hits = sum(1 for label in relevant_labels if any(_matches_relevant(src, [label]) for src in top))
    return hits / len(relevant_labels)


def _mrr_for_labels(retrieved_sources: list[str], relevant_labels: list[str]) -> float:
    if not relevant_labels:
        return 0.0
    for rank, src in enumerate(retrieved_sources, start=1):
        if _matches_relevant(src, relevant_labels):
            return 1.0 / rank
    return 0.0


def run_eval(
    strategy: str = "hybrid",
    use_rerank: bool = True,
    *,
    retrieval_only: bool = False,
    limit: int | None = None,
) -> Path:
    settings = get_settings()
    golden_path = settings.golden_qa_path
    if not golden_path.exists():
        raise FileNotFoundError(f"Golden set not found: {golden_path}")

    items = load_golden(golden_path)
    if limit is not None:
        items = items[:limit]
    results: list[EvalResult] = []

    for item in items:
        console.print(f"[cyan]{item.id}[/cyan] {item.question[:80]}")
        if retrieval_only:
            chunks = retrieve(item.question, strategy=strategy, use_rerank=use_rerank)
            retrieved_sources = [c.chunk.source_path or c.chunk.source_name for c in chunks]
            results.append(
                EvalResult(
                    item=item,
                    strategy=strategy,
                    retrieved_sources=retrieved_sources,
                    recall_at_5=_recall_at_k(retrieved_sources, item.relevant_sources, k=5),
                    mrr=_mrr_for_labels(retrieved_sources, item.relevant_sources),
                    correct_source=_correct_source_at_k(
                        retrieved_sources, item.relevant_sources, k=5
                    )
                    if item.relevant_sources
                    else (1.0 if item.expect_no_answer else 0.0),
                    citation_support=0.0,
                    refusal_ok=1.0 if item.expect_no_answer else 0.0,
                    confidence=0.0,
                    no_answer=False,
                    answer="(retrieval-only eval)",
                )
            )
            continue

        response = ask(item.question, strategy=strategy, use_rerank=use_rerank)
        retrieved_sources = [
            c.chunk.source_path or c.chunk.source_name for c in response.retrieval.chunks
        ]
        results.append(
            EvalResult(
                item=item,
                strategy=strategy,
                retrieved_sources=retrieved_sources,
                recall_at_5=_recall_at_k(retrieved_sources, item.relevant_sources, k=5),
                mrr=_mrr_for_labels(retrieved_sources, item.relevant_sources),
                correct_source=_correct_source_at_k(
                    retrieved_sources, item.relevant_sources, k=5
                )
                if item.relevant_sources
                else (1.0 if item.expect_no_answer else 0.0),
                citation_support=citation_support_rate(response),
                refusal_ok=refusal_correct(response, item.expect_no_answer),
                confidence=response.confidence,
                no_answer=response.no_answer,
                answer=response.answer,
            )
        )

    suffix = f"{strategy}_retrieval" if retrieval_only else strategy
    report_path = _write_report(results, suffix, retrieval_only=retrieval_only)
    console.print(f"[green]Report written to[/green] {report_path}")
    return report_path


def _write_report(
    results: list[EvalResult],
    strategy: str,
    *,
    retrieval_only: bool = False,
) -> Path:
    settings = get_settings()
    settings.reports_dir.mkdir(parents=True, exist_ok=True)
    path = settings.reports_dir / f"eval_{strategy}.md"

    n = len(results) or 1
    retrieval_rows = [r for r in results if r.item.relevant_sources]
    rn = len(retrieval_rows) or 1
    avg = {
        "recall@5": sum(r.recall_at_5 for r in retrieval_rows) / rn,
        "mrr": sum(r.mrr for r in retrieval_rows) / rn,
        "correct_source@5": sum(r.correct_source for r in retrieval_rows) / rn,
        "citation_support": sum(r.citation_support for r in results) / n,
        "refusal_accuracy": sum(r.refusal_ok for r in results) / n,
        "avg_confidence": sum(r.confidence for r in results) / n,
    }

    by_category: dict[str, list[EvalResult]] = {}
    for result in results:
        by_category.setdefault(result.item.category, []).append(result)

    mode = "retrieval-only" if retrieval_only else "full (answer + citations)"
    lines = [
        f"# Evaluation Report — `{strategy}`",
        "",
        f"Mode: **{mode}**",
        f"Questions: **{len(results)}**",
        "",
        "## Summary",
        "",
        f"| Metric | Value |",
        f"| --- | --- |",
        f"| Correct source in top-5 | {avg['correct_source@5']:.1%} |",
        f"| Recall@5 | {avg['recall@5']:.1%} |",
        f"| MRR | {avg['mrr']:.3f} |",
    ]
    if not retrieval_only:
        lines.extend(
            [
                f"| Citation support rate | {avg['citation_support']:.1%} |",
                f"| Refusal accuracy | {avg['refusal_accuracy']:.1%} |",
                f"| Avg confidence | {avg['avg_confidence']:.3f} |",
            ]
        )

    lines.extend(["", "## By category", ""])
    for category, rows in sorted(by_category.items()):
        m = len(rows) or 1
        line = (
            f"- **{category}** (n={len(rows)}): "
            f"correct-source={sum(r.correct_source for r in rows)/m:.1%}"
        )
        if not retrieval_only:
            line += (
                f", citation-support={sum(r.citation_support for r in rows)/m:.1%}, "
                f"refusal={sum(r.refusal_ok for r in rows)/m:.1%}"
            )
        lines.append(line)

    lines.extend(["", "## Per-question", ""])
    for result in results:
        block = [
            f"### {result.item.id} — {result.item.category}",
            "",
            f"**Q:** {result.item.question}",
            "",
            f"- correct_source@5: {result.correct_source:.0%}",
            f"- recall@5: {result.recall_at_5:.0%}",
            f"- mrr: {result.mrr:.3f}",
            f"- retrieved: {', '.join(Path(s).name for s in result.retrieved_sources) or '—'}",
            "",
        ]
        if not retrieval_only:
            block[5:5] = [
                f"- citation_support: {result.citation_support:.0%}",
                f"- refusal_ok: {result.refusal_ok:.0%}",
                f"- confidence: {result.confidence:.3f}",
                f"- no_answer: {result.no_answer}",
            ]
            block.extend(
                [
                    "<details><summary>Answer</summary>",
                    "",
                    result.answer,
                    "",
                    "</details>",
                    "",
                ]
            )
        lines.extend(block)

    path.write_text("\n".join(lines), encoding="utf-8")
    return path
