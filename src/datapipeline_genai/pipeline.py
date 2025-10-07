"""Pipeline orchestration."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .config import PipelineConfig
from .ingestion import iter_transcripts, load_conversations
from .llm import ConversationInsight, build_summariser
from .processing import prepare_transcript


@dataclass
class PipelineResult:
    """Structured outcome of a pipeline run."""

    conversations: list[dict[str, Any]]
    summary: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "conversations": self.conversations,
            "summary": self.summary,
        }


class Pipeline:
    """High level orchestrator for the analytics workflow."""

    def __init__(self, config: PipelineConfig) -> None:
        self.config = config
        self.summariser = build_summariser(
            config.summariser.strategy, config.summariser.model
        )

    def run(self) -> PipelineResult:
        df = load_conversations(self.config.input_path)
        processed: list[dict[str, Any]] = []
        insights: list[ConversationInsight] = []

        for record in iter_transcripts(df):
            processed_record = prepare_transcript(record["transcript"])
            if len(processed_record["tokens"]) < self.config.minimum_tokens:
                continue

            enriched = {**record, **processed_record}
            processed.append(enriched)
            insights.append(
                ConversationInsight(
                    conversation_id=record["conversation_id"],
                    cleaned_transcript=processed_record["cleaned_transcript"],
                    issues=processed_record["issues"],
                    sentiment=float(processed_record["sentiment"]),
                    severity=float(processed_record["severity"]),
                )
            )

        summary = self.summariser.summarise(
            insights,
            max_words=self.config.summariser.max_words,
        )

        return PipelineResult(conversations=processed, summary=summary)

    def write_output(self, result: PipelineResult) -> Path:
        output_path = self.config.output_path
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(result.to_dict(), indent=2))
        return output_path


def run_pipeline(config: PipelineConfig) -> PipelineResult:
    """Convenience function to run the pipeline and persist output."""

    pipeline = Pipeline(config)
    result = pipeline.run()
    pipeline.write_output(result)
    return result
