from __future__ import annotations

from knowledge_copilot.models import RetrievedChunk


def reciprocal_rank_fusion(
    result_lists: list[list[RetrievedChunk]],
    *,
    k: int = 60,
    weights: list[float] | None = None,
) -> list[RetrievedChunk]:
    """Merge ranked lists with Reciprocal Rank Fusion over shared chunk IDs."""
    if weights is None:
        weights = [1.0] * len(result_lists)
    if len(weights) != len(result_lists):
        raise ValueError("weights must match number of result lists")

    scores: dict[str, float] = {}
    best: dict[str, RetrievedChunk] = {}

    for weight, results in zip(weights, result_lists, strict=True):
        for rank, item in enumerate(results, start=1):
            chunk_id = item.chunk.chunk_id
            scores[chunk_id] = scores.get(chunk_id, 0.0) + weight * (1.0 / (k + rank))
            if chunk_id not in best:
                best[chunk_id] = item.model_copy(deep=True)
                best[chunk_id].sources = list(item.sources)
            else:
                for source in item.sources:
                    if source not in best[chunk_id].sources:
                        best[chunk_id].sources.append(source)

    fused = []
    for chunk_id, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
        item = best[chunk_id]
        item.score = score
        fused.append(item)
    return fused
