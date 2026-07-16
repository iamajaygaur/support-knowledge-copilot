from knowledge_copilot.models import Chunk, RetrievedChunk
from knowledge_copilot.retrieve.fusion import reciprocal_rank_fusion


def _rc(chunk_id: str, score: float, source: str) -> RetrievedChunk:
    return RetrievedChunk(
        chunk=Chunk(
            chunk_id=chunk_id,
            text=f"text for {chunk_id}",
            source_name="s.md",
            source_path="docs/s.md",
        ),
        score=score,
        sources=[source],
    )


def test_rrf_prefers_items_in_both_lists():
    dense = [_rc("a", 0.9, "dense"), _rc("b", 0.8, "dense"), _rc("c", 0.7, "dense")]
    sparse = [_rc("c", 12.0, "sparse"), _rc("a", 10.0, "sparse"), _rc("d", 8.0, "sparse")]
    fused = reciprocal_rank_fusion([dense, sparse], k=60)
    assert fused[0].chunk.chunk_id in {"a", "c"}
    top_ids = {item.chunk.chunk_id for item in fused[:2]}
    assert "a" in top_ids and "c" in top_ids
    both = next(item for item in fused if item.chunk.chunk_id == "a")
    assert set(both.sources) == {"dense", "sparse"}
