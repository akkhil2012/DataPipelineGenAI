"""Text processing utilities for the pipeline."""

from __future__ import annotations

import re
from collections import Counter
from typing import Iterable


def normalise_whitespace(text: str) -> str:
    """Collapse excess whitespace and trim the text."""

    return re.sub(r"\s+", " ", text).strip()


def tidy_punctuation(text: str) -> str:
    """Ensure punctuation spacing is neat."""

    text = re.sub(r"\s+([\.,;:!?])", r"\1", text)
    text = re.sub(r"([\.,;:!?])(?!\s|$)", r"\1 ", text)
    return normalise_whitespace(text)


def tokenise(text: str) -> list[str]:
    """Simple whitespace tokenizer."""

    clean = normalise_whitespace(text.lower())
    return [token for token in clean.split(" ") if token]


LANGUAGE_HINTS = {
    "es": {"hola", "gracias", "soporte"},
    "fr": {"bonjour", "merci", "facture"},
}


def detect_language(tokens: Iterable[str]) -> str:
    """Detect the likely language using naive keyword counts."""

    token_set = set(tokens)
    for code, hints in LANGUAGE_HINTS.items():
        if token_set & hints:
            return code
    return "en"


ISSUE_KEYWORDS = {
    "connectivity": {"internet", "wifi", "router", "signal", "cutting", "connect"},
    "hardware": {"firmware", "update", "device", "bricked", "lights"},
    "billing": {"billing", "charged", "invoice", "payment", "cancelled"},
    "application": {"app", "notifications", "mobile", "software"},
    "support_experience": {"support", "response", "scripted", "agent", "ticket", "login"},
}


SEVERITY_SCORES = {
    "connectivity": 0.8,
    "hardware": 0.9,
    "billing": 0.7,
    "application": 0.5,
    "support_experience": 0.6,
}


SENTIMENT_NEGATIVE = {"cutting", "bricked", "charged", "late", "never", "lockout"}
SENTIMENT_POSITIVE = {"love", "kind"}


def classify_issue(tokens: Iterable[str]) -> tuple[list[str], float]:
    """Return matching issue categories and a severity score."""

    token_counts = Counter(tokens)
    matched: list[str] = []
    severity = 0.0
    for issue, keywords in ISSUE_KEYWORDS.items():
        overlap = sum(token_counts.get(keyword, 0) for keyword in keywords)
        if overlap:
            matched.append(issue)
            severity = max(severity, SEVERITY_SCORES.get(issue, 0.4))
    return matched or ["general"], severity if matched else 0.3


def sentiment_score(tokens: Iterable[str]) -> float:
    """Naive sentiment score between -1 and 1."""

    tokens = list(tokens)
    positives = sum(1 for token in tokens if token in SENTIMENT_POSITIVE)
    negatives = sum(1 for token in tokens if token in SENTIMENT_NEGATIVE)
    total = len(tokens) or 1
    return ((positives * 1.0) - (negatives * 1.2)) / total


def prepare_transcript(transcript: str) -> dict[str, object]:
    """Full processing pipeline for a single transcript."""

    cleaned = tidy_punctuation(transcript)
    tokens = tokenise(cleaned)
    language = detect_language(tokens)
    issues, severity = classify_issue(tokens)
    sentiment = sentiment_score(tokens)

    return {
        "cleaned_transcript": cleaned,
        "tokens": tokens,
        "language": language,
        "issues": issues,
        "severity": round(severity, 2),
        "sentiment": round(sentiment, 3),
    }
