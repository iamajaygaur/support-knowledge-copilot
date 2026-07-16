from __future__ import annotations

from knowledge_copilot.config import get_settings
from knowledge_copilot.index.bm25_store import BM25Store
from knowledge_copilot.index.embeddings import embed_query
from knowledge_copilot.index.qdrant_store import QdrantStore
from knowledge_copilot.models import RetrievedChunk
from knowledge_copilot.retrieve.fusion import reciprocal_rank_fusion
from knowledge_copilot.retrieve.rerank import rerank_with_llm


def retrieve(
    question: str,
    *,
    strategy: str = "hybrid",
    use_rerank: bool = True,
) -> list[RetrievedChunk]:
    settings = get_settings()
    strategy = strategy.lower().strip()
    if strategy not in {"dense", "sparse", "hybrid"}:
        raise ValueError("strategy must be one of: dense, sparse, hybrid")

    dense_hits: list[RetrievedChunk] = []
    sparse_hits: list[RetrievedChunk] = []

    if strategy in {"dense", "hybrid"}:
        vector = embed_query(question)
        dense_hits = QdrantStore().search(vector, limit=settings.dense_k)

    if strategy in {"sparse", "hybrid"}:
        bm25 = BM25Store(settings.bm25_path)
        bm25.load()
        sparse_hits = bm25.search(question, limit=settings.sparse_k)

    if strategy == "dense":
        fused = dense_hits
    elif strategy == "sparse":
        fused = sparse_hits
    else:
        fused = reciprocal_rank_fusion(
            [dense_hits, sparse_hits],
            k=settings.rrf_k,
            weights=[1.0, 1.0],
        )

    pool = fused[: settings.rerank_pool]
    if use_rerank and strategy != "sparse":
        return rerank_with_llm(question, pool, top_n=settings.final_k)
    return pool[: settings.final_k]
