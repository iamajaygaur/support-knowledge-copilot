from __future__ import annotations

import pickle
import re
from pathlib import Path

from rank_bm25 import BM25Okapi

from knowledge_copilot.models import Chunk, RetrievedChunk

TOKEN_RE = re.compile(r"[a-z0-9_./+-]+", re.IGNORECASE)


def tokenize(text: str) -> list[str]:
    return [t.lower() for t in TOKEN_RE.findall(text)]


class BM25Store:
    def __init__(self, path: Path) -> None:
        self.path = Path(path)
        self.chunks: list[Chunk] = []
        self._bm25: BM25Okapi | None = None
        self._corpus_tokens: list[list[str]] = []

    def build(self, chunks: list[Chunk]) -> None:
        self.chunks = list(chunks)
        self._corpus_tokens = [tokenize(c.text) for c in self.chunks]
        self._bm25 = BM25Okapi(self._corpus_tokens) if self.chunks else None

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"chunks": [c.model_dump(mode="json") for c in self.chunks]}
        with self.path.open("wb") as fh:
            pickle.dump(payload, fh)

    def load(self) -> None:
        if not self.path.exists():
            raise FileNotFoundError(
                f"BM25 index not found at {self.path}. Run ingest.py first."
            )
        with self.path.open("rb") as fh:
            payload = pickle.load(fh)
        self.chunks = [Chunk.model_validate(item) for item in payload["chunks"]]
        self._corpus_tokens = [tokenize(c.text) for c in self.chunks]
        self._bm25 = BM25Okapi(self._corpus_tokens) if self.chunks else None

    def search(self, query: str, limit: int = 10) -> list[RetrievedChunk]:
        if self._bm25 is None:
            self.load()
        assert self._bm25 is not None
        tokens = tokenize(query)
        if not tokens:
            return []
        scores = self._bm25.get_scores(tokens)
        ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)[:limit]
        results: list[RetrievedChunk] = []
        for idx, score in ranked:
            if score <= 0:
                continue
            results.append(
                RetrievedChunk(
                    chunk=self.chunks[idx],
                    score=float(score),
                    sources=["sparse"],
                )
            )
        return results

    def get_by_ids(self, chunk_ids: list[str]) -> dict[str, Chunk]:
        if not self.chunks and self.path.exists():
            self.load()
        return {c.chunk_id: c for c in self.chunks if c.chunk_id in set(chunk_ids)}
