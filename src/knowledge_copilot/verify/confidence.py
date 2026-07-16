from __future__ import annotations

from knowledge_copilot.models import Citation, CitationVerdict, RetrievedChunk


def _norm_retrieval_score(retrieved: list[RetrievedChunk]) -> float:
    if not retrieved:
        return 0.0
    scores = [item.score for item in retrieved]
    top = max(scores)
    # RRF scores are small (~0.03); BM25 can be large; cosine is 0-1.
    if top <= 1.0:
        return max(0.0, min(1.0, top))
    # Soft-normalize larger sparse scores
    return max(0.0, min(1.0, top / (top + 5.0)))


def score_confidence(
    *,
    retrieved: list[RetrievedChunk],
    citations: list[Citation],
    no_answer: bool,
    unverified: list[str],
) -> tuple[float, dict[str, float]]:
    retrieval_score = _norm_retrieval_score(retrieved)

    if citations:
        supported = sum(1 for c in citations if c.verdict == CitationVerdict.SUPPORTED)
        partial = sum(1 for c in citations if c.verdict == CitationVerdict.PARTIAL)
        citation_support_rate = (supported + 0.5 * partial) / len(citations)
    else:
        # No citations: ok for explicit no-answer, weak otherwise
        citation_support_rate = 1.0 if no_answer else 0.2

    # Completeness: fewer unverified bullets => higher
    answer_completeness = 1.0 / (1.0 + 0.35 * len(unverified))

    answered_component = 0.0 if no_answer else 1.0

    breakdown = {
        "retrieval_score": round(retrieval_score, 4),
        "citation_support_rate": round(citation_support_rate, 4),
        "answer_completeness": round(answer_completeness, 4),
        "answered": float(answered_component),
    }
    confidence = (
        0.35 * retrieval_score
        + 0.35 * citation_support_rate
        + 0.20 * answer_completeness
        + 0.10 * answered_component
    )
    return round(confidence, 4), breakdown
