"""Configuration models for the pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class SummariserConfig:
    """Configuration for the summariser component."""

    strategy: str = "heuristic"
    model: str = "gpt-4o-mini"
    max_words: int = 120

    def __post_init__(self) -> None:  # type: ignore[override]
        if self.strategy not in {"heuristic", "llm"}:
            raise ValueError("strategy must be either 'heuristic' or 'llm'")
        if not isinstance(self.model, str) or not self.model:
            raise ValueError("model must be a non-empty string")
        if not (20 <= int(self.max_words) <= 500):
            raise ValueError("max_words must be between 20 and 500")


@dataclass(frozen=True)
class PipelineConfig:
    """Top-level pipeline configuration."""

    input_path: Path
    output_path: Path
    summariser: SummariserConfig = field(default_factory=SummariserConfig)
    minimum_tokens: int = 12

    def __post_init__(self) -> None:  # type: ignore[override]
        input_path = Path(self.input_path).expanduser().resolve()
        output_path = Path(self.output_path).expanduser().resolve()
        object.__setattr__(self, "input_path", input_path)
        object.__setattr__(self, "output_path", output_path)

        if self.minimum_tokens < 0:
            raise ValueError("minimum_tokens must be non-negative")
