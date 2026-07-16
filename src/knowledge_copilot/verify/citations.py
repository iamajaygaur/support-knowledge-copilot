from __future__ import annotations

import json
import re

from knowledge_copilot.llm import generate_json
from knowledge_copilot.models import Citation, CitationVerdict, RetrievedChunk

CITATION_RE = re.compile(r"\[([a-zA-Z0-9._:-]+)\]")


def extract_citation_ids(answer: str) -> list[str]:
    return list(dict.fromkeys(CITATION_RE.findall(answer)))


def _claims_for_citations(answer: str) -> list[tuple[str, str]]:
    """Pair each citation with the sentence that contains it."""
    sentences = re.split(r"(?<=[.!?])\s+", answer.strip())
    pairs: list[tuple[str, str]] = []
    for sentence in sentences:
        ids = CITATION_RE.findall(sentence)
        claim = CITATION_RE.sub("", sentence).strip()
        for chunk_id in ids:
            pairs.append((chunk_id, claim or sentence.strip()))
    for chunk_id in extract_citation_ids(answer):
        if not any(cid == chunk_id for cid, _ in pairs):
            pairs.append((chunk_id, answer[:240]))
    return pairs


def verify_citations(
    answer: str,
    retrieved: list[RetrievedChunk],
) -> list[Citation]:
    by_id = {item.chunk.chunk_id: item.chunk for item in retrieved}
    pairs = _claims_for_citations(answer)
    if not pairs:
        return []

    payload_rows = []
    for chunk_id, claim in pairs:
        chunk = by_id.get(chunk_id)
        payload_rows.append(
            {
                "chunk_id": chunk_id,
                "claim": claim,
                "chunk_text": chunk.text if chunk else "",
                "known": chunk is not None,
            }
        )

    prompt = f"""You verify whether each cited chunk supports its claim.
For each item return verdict: supported | not_supported | partial, plus a short rationale.
Return ONLY JSON: {{"results": [{{"chunk_id": "...", "claim": "...", "verdict": "...", "rationale": "..."}}]}}

Items:
{json.dumps(payload_rows, indent=2)}
"""
    data = generate_json(prompt, temperature=0.0)
    rows = data.get("results", [])

    by_key = {(row.get("chunk_id"), row.get("claim")): row for row in rows}
    citations: list[Citation] = []
    for chunk_id, claim in pairs:
        chunk = by_id.get(chunk_id)
        row = by_key.get((chunk_id, claim), {})
        if chunk is None:
            verdict = CitationVerdict.NOT_SUPPORTED
            rationale = "Cited chunk_id was not in retrieved context."
        else:
            raw = (row.get("verdict") or "partial").lower()
            try:
                verdict = CitationVerdict(raw)
            except ValueError:
                verdict = CitationVerdict.PARTIAL
            rationale = row.get("rationale") or ""

        citations.append(
            Citation(
                chunk_id=chunk_id,
                claim=claim,
                source_name=chunk.source_name if chunk else "",
                section_heading=chunk.section_heading if chunk else "",
                verdict=verdict,
                rationale=rationale,
            )
        )
    return citations
