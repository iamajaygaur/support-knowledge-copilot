#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from knowledge_copilot.config import get_settings
from knowledge_copilot.ingest.pipeline import ingest_documents

console = Console()


def main(
    source: Optional[Path] = typer.Option(None, "--source", help="Directory of documents to ingest"),
    rebuild: bool = typer.Option(False, "--rebuild", help="Drop and recreate the vector collection"),
    strategy: str = typer.Option("heading", "--strategy", help="Chunking strategy: heading|fixed"),
) -> None:
    """Ingest support docs into Qdrant + BM25."""
    settings = get_settings()
    source_dir = source or settings.docs_dir
    if strategy not in {"heading", "fixed"}:
        raise typer.BadParameter("strategy must be heading or fixed")

    chunks = ingest_documents(source_dir, rebuild=rebuild, strategy=strategy)  # type: ignore[arg-type]
    console.print(f"[green]Done.[/green] Indexed {len(chunks)} chunks from {source_dir}")


if __name__ == "__main__":
    typer.run(main)
