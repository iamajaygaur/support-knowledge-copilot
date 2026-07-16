from __future__ import annotations

from datetime import date
from functools import lru_cache

from qdrant_client import QdrantClient
from qdrant_client.http import models as qm

from knowledge_copilot.config import get_settings
from knowledge_copilot.models import AccessLevel, Chunk, DocType, RetrievedChunk


def _payload_from_chunk(chunk: Chunk) -> dict:
    return {
        "chunk_id": chunk.chunk_id,
        "text": chunk.text,
        "source_name": chunk.source_name,
        "source_path": chunk.source_path,
        "section_heading": chunk.section_heading,
        "last_updated": chunk.last_updated.isoformat() if chunk.last_updated else None,
        "doc_type": chunk.doc_type.value,
        "access_level": chunk.access_level.value,
        "page_number": chunk.page_number,
        "metadata": chunk.metadata,
    }


def _chunk_from_payload(payload: dict) -> Chunk:
    last_updated = payload.get("last_updated")
    return Chunk(
        chunk_id=payload["chunk_id"],
        text=payload["text"],
        source_name=payload["source_name"],
        source_path=payload["source_path"],
        section_heading=payload.get("section_heading") or "",
        last_updated=date.fromisoformat(last_updated) if last_updated else None,
        doc_type=DocType(payload.get("doc_type", "other")),
        access_level=AccessLevel(payload.get("access_level", "internal")),
        page_number=payload.get("page_number"),
        metadata=payload.get("metadata") or {},
    )


@lru_cache
def _get_client(path: str | None, url: str) -> QdrantClient:
    # Local embedded mode allows only one open client per path.
    if path:
        return QdrantClient(path=path)
    return QdrantClient(url=url)


class QdrantStore:
    def __init__(self) -> None:
        settings = get_settings()
        self.collection = settings.qdrant_collection
        self.dim = settings.embedding_dim
        path = str(settings.qdrant_path) if settings.qdrant_path else None
        self.client = _get_client(path, settings.qdrant_url)

    def ensure_collection(self) -> None:
        if not self.client.collection_exists(self.collection):
            self.recreate_collection()

    def recreate_collection(self) -> None:
        if self.client.collection_exists(self.collection):
            self.client.delete_collection(self.collection)
        self.client.create_collection(
            collection_name=self.collection,
            vectors_config=qm.VectorParams(size=self.dim, distance=qm.Distance.COSINE),
        )

    def upsert_chunks(self, chunks: list[Chunk], vectors: list[list[float]]) -> None:
        if len(chunks) != len(vectors):
            raise ValueError("chunks and vectors length mismatch")
        points = [
            qm.PointStruct(
                id=self._point_id(chunk.chunk_id),
                vector=vector,
                payload=_payload_from_chunk(chunk),
            )
            for chunk, vector in zip(chunks, vectors, strict=True)
        ]
        batch_size = 64
        for i in range(0, len(points), batch_size):
            self.client.upsert(collection_name=self.collection, points=points[i : i + batch_size])

    def search(self, vector: list[float], limit: int = 10) -> list[RetrievedChunk]:
        response = self.client.query_points(
            collection_name=self.collection,
            query=vector,
            limit=limit,
            with_payload=True,
        )
        retrieved: list[RetrievedChunk] = []
        for hit in response.points:
            payload = hit.payload or {}
            retrieved.append(
                RetrievedChunk(
                    chunk=_chunk_from_payload(payload),
                    score=float(hit.score or 0.0),
                    sources=["dense"],
                )
            )
        return retrieved

    def get_by_ids(self, chunk_ids: list[str]) -> dict[str, Chunk]:
        if not chunk_ids:
            return {}
        points = self.client.retrieve(
            collection_name=self.collection,
            ids=[self._point_id(cid) for cid in chunk_ids],
            with_payload=True,
        )
        out: dict[str, Chunk] = {}
        for point in points:
            payload = point.payload or {}
            chunk = _chunk_from_payload(payload)
            out[chunk.chunk_id] = chunk
        return out

    @staticmethod
    def _point_id(chunk_id: str) -> str:
        import hashlib
        import uuid

        digest = hashlib.md5(chunk_id.encode()).hexdigest()
        return str(uuid.UUID(digest))
