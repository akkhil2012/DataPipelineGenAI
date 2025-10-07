"""Summarisation utilities."""

from __future__ import annotations

import os
from abc import ABC, abstractmethod
from collections import Counter
from dataclasses import dataclass
from typing import Iterable, Sequence


@dataclass
class ConversationInsight:
    """Processed information about a conversation."""

    conversation_id: str
    cleaned_transcript: str
    issues: Sequence[str]
    sentiment: float
    severity: float


class Summariser(ABC):
    """Base summariser interface."""

    @abstractmethod
    def summarise(self, conversations: Iterable[ConversationInsight], *, max_words: int) -> str:
        """Return a textual summary for the conversations."""


class HeuristicSummariser(Summariser):
    """A summariser that relies on deterministic heuristics instead of an LLM."""

    def summarise(self, conversations: Iterable[ConversationInsight], *, max_words: int) -> str:
        insights = list(conversations)
        if not insights:
            return "No conversations were processed."

        issue_counter = Counter(issue for insight in insights for issue in insight.issues)
        total = sum(issue_counter.values()) or 1
        dominant = issue_counter.most_common(3)
        avg_sentiment = sum(insight.sentiment for insight in insights) / len(insights)
        avg_severity = sum(insight.severity for insight in insights) / len(insights)

        bullets = []
        for issue, count in dominant:
            percentage = int(round((count / total) * 100))
            bullets.append(f"- {issue.replace('_', ' ').title()} reported in {percentage}% of cases")

        summary_parts = [
            "Top conversation themes:",
            *bullets,
            f"Average sentiment: {avg_sentiment:.2f} (negative is friction)",
            f"Average severity: {avg_severity:.2f} (1.0 is critical)",
        ]

        text = "\n".join(summary_parts)
        words = text.split()
        if len(words) <= max_words:
            return text
        return " ".join(words[:max_words]) + " …"


class LLMSummariser(Summariser):
    """Placeholder summariser that would call a hosted LLM."""

    def __init__(self, model: str) -> None:
        self.model = model
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY environment variable must be set for LLM summarisation.")

    def summarise(self, conversations: Iterable[ConversationInsight], *, max_words: int) -> str:
        insights = list(conversations)
        payload = "\n\n".join(
            f"Conversation {insight.conversation_id}: issues={', '.join(insight.issues)}, severity={insight.severity}, sentiment={insight.sentiment}\n{insight.cleaned_transcript}"
            for insight in insights
        )
        return (
            f"[LLM summary placeholder for model {self.model} with max_words={max_words}. "
            f"Would send payload of length {len(payload.split())} words.]"
        )


def build_summariser(strategy: str, model: str) -> Summariser:
    """Factory for creating a summariser implementation."""

    if strategy == "heuristic":
        return HeuristicSummariser()
    if strategy == "llm":
        return LLMSummariser(model)
    raise ValueError(f"Unknown summariser strategy: {strategy}")
