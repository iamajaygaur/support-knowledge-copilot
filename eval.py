#!/usr/bin/env python3
from __future__ import annotations

import typer
from rich.console import Console

from knowledge_copilot.eval.runner import run_eval

console = Console()


def main(
    strategy: str = typer.Option("hybrid", "--strategy", help="dense | sparse | hybrid"),
    use_rerank: bool = typer.Option(True, "--use-rerank/--no-rerank"),
    retrieval_only: bool = typer.Option(
        False,
        "--retrieval-only",
        help="Measure retrieval metrics only (no LLM generation). Best for hybrid vs dense.",
    ),
    limit: int | None = typer.Option(None, "--limit", help="Optional cap on number of questions"),
) -> None:
    """Run the golden-set evaluation and write a Markdown report."""
    if strategy not in {"dense", "sparse", "hybrid"}:
        raise typer.BadParameter("strategy must be dense, sparse, or hybrid")
    path = run_eval(
        strategy=strategy,
        use_rerank=use_rerank,
        retrieval_only=retrieval_only,
        limit=limit,
    )
    console.print(f"[green]Done.[/green] {path}")


if __name__ == "__main__":
    typer.run(main)
