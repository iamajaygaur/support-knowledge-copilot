from __future__ import annotations

import time

from google.genai import types
from google.genai.errors import ClientError, ServerError

from knowledge_copilot.config import get_settings
from knowledge_copilot.llm import get_genai_client


def _is_retryable(exc: Exception) -> bool:
    if isinstance(exc, (ClientError, ServerError)):
        code = getattr(exc, "code", None) or getattr(exc, "status_code", None)
        if code in {429, 500, 503}:
            return True
        msg = str(exc).lower()
        return any(t in msg for t in ("429", "503", "resource_exhausted", "unavailable"))
    return False


def embed_texts(
    texts: list[str],
    *,
    batch_size: int = 32,
    task_type: str = "RETRIEVAL_DOCUMENT",
) -> list[list[float]]:
    if not texts:
        return []
    client = get_genai_client()
    settings = get_settings()
    vectors: list[list[float]] = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i : i + batch_size]
        last_exc: Exception | None = None
        for attempt in range(6):
            try:
                response = client.models.embed_content(
                    model=settings.embedding_model,
                    contents=batch,
                    config=types.EmbedContentConfig(
                        task_type=task_type,
                        output_dimensionality=settings.embedding_dim,
                    ),
                )
                for emb in response.embeddings or []:
                    vectors.append(list(emb.values or []))
                last_exc = None
                break
            except Exception as exc:  # noqa: BLE001
                last_exc = exc
                if not _is_retryable(exc) or attempt == 5:
                    raise
                time.sleep(min(2.0 * (2**attempt), 30.0))
        if last_exc is not None:
            raise last_exc
    if len(vectors) != len(texts):
        raise RuntimeError(
            f"Embedding count mismatch: got {len(vectors)} vectors for {len(texts)} texts"
        )
    return vectors


def embed_query(text: str) -> list[float]:
    return embed_texts([text], task_type="RETRIEVAL_QUERY")[0]
