#!/usr/bin/env python3
from __future__ import annotations

import json

import typer
from rich.console import Console
from rich.panel import Panel

from knowledge_copilot.service import ask

console = Console()


def main(
    question: str = typer.Argument(..., help="Support question to answer"),
    strategy: str = typer.Option("hybrid", "--strategy", help="dense | sparse | hybrid"),
    use_rerank: bool = typer.Option(True, "--use-rerank/--no-rerank"),
    as_json: bool = typer.Option(False, "--json", help="Print full JSON response"),
) -> None:
    """Ask the Support Knowledge Copilot from the CLI."""
    if strategy not in {"dense", "sparse", "hybrid"}:
        raise typer.BadParameter("strategy must be dense, sparse, or hybrid")

    response = ask(question, strategy=strategy, use_rerank=use_rerank)
    if as_json:
        console.print_json(response.model_dump_json())
        return

    console.print(Panel(response.answer, title="Answer", border_style="green"))
    console.print(f"confidence: [cyan]{response.confidence:.2f}[/cyan]  no_answer: {response.no_answer}")
    if response.citations:
        console.print("\n[bold]Citations[/bold]")
        for citation in response.citations:
            console.print(
                f"  [{citation.verdict.value}] {citation.chunk_id} — {citation.source_name} › {citation.section_heading}"
            )
    if response.unverified:
        console.print("\n[bold]Unverified[/bold]")
        for item in response.unverified:
            console.print(f"  - {item}")
    console.print("\n[bold]Retrieved[/bold]")
    for item in response.retrieval.chunks:
        console.print(
            f"  {item.chunk.chunk_id} score={item.score:.4f} sources={','.join(item.sources)} "
            f"({item.chunk.source_name} › {item.chunk.section_heading})"
        )


if __name__ == "__main__":
    typer.run(main)
