from __future__ import annotations

from knowledge_copilot.models import AskResponse, CitationVerdict


def recall_at_k(retrieved_ids: list[str], relevant_ids: list[str], k: int = 5) -> float:
    if not relevant_ids:
        return 0.0
    top = set(retrieved_ids[:k])
    hits = sum(1 for rid in relevant_ids if rid in top)
    return hits / len(relevant_ids)


def mrr(retrieved_ids: list[str], relevant_ids: list[str]) -> float:
    relevant = set(relevant_ids)
    for rank, chunk_id in enumerate(retrieved_ids, start=1):
        if chunk_id in relevant:
            return 1.0 / rank
    return 0.0


def correct_source_in_top_k(retrieved_ids: list[str], relevant_ids: list[str], k: int = 5) -> float:
    if not relevant_ids:
        return 0.0
    return 1.0 if set(retrieved_ids[:k]) & set(relevant_ids) else 0.0


def citation_support_rate(response: AskResponse) -> float:
    if not response.citations:
        return 1.0 if response.no_answer else 0.0
    supported = sum(1 for c in response.citations if c.verdict == CitationVerdict.SUPPORTED)
    return supported / len(response.citations)


def refusal_correct(response: AskResponse, expect_no_answer: bool) -> float:
    return 1.0 if response.no_answer == expect_no_answer else 0.0
