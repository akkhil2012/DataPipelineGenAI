"""Data ingestion utilities without heavy dependencies."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable

REQUIRED_COLUMNS = ["conversation_id", "customer_id", "channel", "transcript"]


def load_conversations(path: Path) -> list[dict[str, str]]:
    """Load conversation transcripts from a CSV file into dictionaries."""

    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("CSV file is missing a header row")

        missing = set(REQUIRED_COLUMNS) - set(reader.fieldnames)
        if missing:
            raise ValueError(f"Missing columns in CSV: {', '.join(sorted(missing))}")

        conversations: list[dict[str, str]] = []
        for row in reader:
            conversations.append({column: str(row.get(column, "")) for column in REQUIRED_COLUMNS})

    return conversations


def iter_transcripts(rows: Iterable[dict[str, str]]) -> Iterable[dict[str, str]]:
    """Yield conversations as dictionaries."""

    for row in rows:
        yield {
            "conversation_id": row["conversation_id"],
            "customer_id": row["customer_id"],
            "channel": row["channel"],
            "transcript": row["transcript"],
        }
