from __future__ import annotations

from pathlib import Path

from rich.console import Console

from knowledge_copilot.config import get_settings
from knowledge_copilot.index.bm25_store import BM25Store
from knowledge_copilot.index.embeddings import embed_texts
from knowledge_copilot.index.qdrant_store import QdrantStore
from knowledge_copilot.ingest.chunking import ChunkStrategy, chunk_documents
from knowledge_copilot.ingest.loaders import load_documents
from knowledge_copilot.models import Chunk

console = Console()


def ingest_documents(
    source: Path,
    *,
    rebuild: bool = False,
    strategy: ChunkStrategy = "heading",
) -> list[Chunk]:
    settings = get_settings()
    source = Path(source)
    if not source.exists():
        raise FileNotFoundError(f"Source path not found: {source}")

    console.print(f"[bold]Loading documents from[/bold] {source}")
    docs = load_documents(source)
    console.print(f"Loaded [cyan]{len(docs)}[/cyan] documents")

    chunks = chunk_documents(docs, strategy=strategy)
    console.print(
        f"Created [cyan]{len(chunks)}[/cyan] chunks using [magenta]{strategy}[/magenta] strategy"
    )
    if not chunks:
        raise RuntimeError("No chunks produced — check your source documents.")

    console.print("Generating embeddings…")
    vectors = embed_texts([c.text for c in chunks])

    qdrant = QdrantStore()
    if rebuild:
        qdrant.recreate_collection()
    else:
        qdrant.ensure_collection()
    qdrant.upsert_chunks(chunks, vectors)
    console.print(f"Upserted [cyan]{len(chunks)}[/cyan] vectors into Qdrant")

    bm25 = BM25Store(settings.bm25_path)
    bm25.build(chunks)
    bm25.save()
    console.print(f"Built BM25 index at [cyan]{settings.bm25_path}[/cyan]")

    return chunks
