from __future__ import annotations

from knowledge_copilot.llm import generate_json
from knowledge_copilot.models import RetrievedChunk


RERANK_PROMPT = """You are a relevance ranker for a support knowledge base.
Score how useful each passage is for answering the question.
Return ONLY valid JSON: {{"rankings": [{{"chunk_id": "...", "score": 0.0}}]}}
Scores must be between 0 and 1. Include every chunk_id exactly once, best first.

Question: {question}

Passages:
{passages}
"""


def rerank_with_llm(
    question: str,
    chunks: list[RetrievedChunk],
    *,
    top_n: int,
) -> list[RetrievedChunk]:
    if not chunks:
        return []
    if len(chunks) <= top_n:
        return chunks

    passages = "\n\n".join(
        f"[{item.chunk.chunk_id}] {item.chunk.section_heading}\n{item.chunk.text[:800]}"
        for item in chunks
    )
    data = generate_json(
        RERANK_PROMPT.format(question=question, passages=passages),
        temperature=0.0,
    )
    rankings = data.get("rankings", [])
    if not rankings:
        return chunks[:top_n]

    by_id = {item.chunk.chunk_id: item for item in chunks}
    ordered: list[RetrievedChunk] = []
    seen: set[str] = set()
    for row in rankings:
        chunk_id = row.get("chunk_id")
        if chunk_id in by_id and chunk_id not in seen:
            item = by_id[chunk_id].model_copy(deep=True)
            item.score = float(row.get("score", item.score))
            if "rerank" not in item.sources:
                item.sources.append("rerank")
            ordered.append(item)
            seen.add(chunk_id)

    for item in chunks:
        if item.chunk.chunk_id not in seen:
            ordered.append(item)

    return ordered[:top_n]
