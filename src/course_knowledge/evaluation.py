"""Golden-question retrieval evaluation; answers remain outside the scoring loop."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from .retrieval import FusedCandidate


@dataclass(frozen=True)
class GoldenQuestion:
    question_id: str
    question: str
    expected_sources: tuple[tuple[str, str], ...]


def load_questions(path: Path) -> list[GoldenQuestion]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return [GoldenQuestion(item["id"], item["question"], tuple((source["course_key"], source["source"]) for source in item["expected_sources"]))
            for item in data["questions"]]


def source_hit(results: list[FusedCandidate], expected_sources: tuple[tuple[str, str], ...]) -> bool:
    found = {(result.candidate.metadata["course_key"], result.candidate.metadata["source"]) for result in results}
    return bool(found.intersection(expected_sources))


def summarize(hits: list[bool]) -> dict[str, float | int]:
    return {"questions": len(hits), "source_hit_rate": sum(hits) / len(hits) if hits else 0.0}
