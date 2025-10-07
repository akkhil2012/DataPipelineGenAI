"""Command line interface for the pipeline."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

from .config import PipelineConfig, SummariserConfig
from .pipeline import Pipeline


def _build_parser() -> argparse.ArgumentParser:
    """Create the top level argument parser for the CLI."""

    parser = argparse.ArgumentParser(
        prog="datapipeline-genai",
        description="Run the DataPipeline GenAI analytics workflow.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser(
        "run",
        help="Execute the pipeline and write the resulting report.",
        description="Execute the pipeline and write the resulting report.",
    )
    run_parser.add_argument(
        "--input",
        type=Path,
        required=True,
        help="Path to the input CSV file containing support transcripts.",
    )
    run_parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Destination path for the JSON analytics report.",
    )
    run_parser.add_argument(
        "--summariser",
        default="heuristic",
        choices=("heuristic", "llm"),
        help="Summarisation backend to use (default: heuristic).",
    )
    run_parser.add_argument(
        "--model",
        default="gpt-4o-mini",
        help="Model identifier when using the LLM backend.",
    )
    run_parser.add_argument(
        "--minimum-tokens",
        type=int,
        default=12,
        metavar="N",
        help="Minimum number of tokens required to analyse a transcript.",
    )

    return parser


def main(argv: Iterable[str] | None = None) -> None:
    """Entrypoint for the command line interface."""

    parser = _build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)

    if args.command != "run":
        parser.error(f"Unsupported command: {args.command}")

    config = PipelineConfig(
        input_path=args.input,
        output_path=args.output,
        summariser=SummariserConfig(strategy=args.summariser, model=args.model),
        minimum_tokens=args.minimum_tokens,
    )

    pipeline = Pipeline(config)
    result = pipeline.run()
    pipeline.write_output(result)
    print(f"Report written to {args.output}")


if __name__ == "__main__":
    main()
