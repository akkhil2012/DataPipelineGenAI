"""Command line interface for the pipeline."""

from __future__ import annotations

from pathlib import Path

import typer

from .config import PipelineConfig, SummariserConfig
from .pipeline import Pipeline

app = typer.Typer(help="Run the DataPipeline GenAI analytics workflow.")


@app.command()
def run(
    input: Path = typer.Option(..., exists=True, readable=True, help="Path to the input CSV."),
    output: Path = typer.Option(..., help="Destination path for the JSON analytics report."),
    summariser: str = typer.Option("heuristic", help="Summarisation backend (heuristic or llm)."),
    model: str = typer.Option("gpt-4o-mini", help="Model identifier when using the LLM backend."),
    minimum_tokens: int = typer.Option(12, min=0, help="Minimum number of tokens required to analyse a transcript."),
) -> None:
    """Execute the pipeline and write the resulting report."""

    config = PipelineConfig(
        input_path=input,
        output_path=output,
        summariser=SummariserConfig(strategy=summariser, model=model),
        minimum_tokens=minimum_tokens,
    )

    pipeline = Pipeline(config)
    result = pipeline.run()
    pipeline.write_output(result)
    typer.echo(f"Report written to {output}")


if __name__ == "__main__":
    app()
