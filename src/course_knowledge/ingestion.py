"""Prepare course material for deterministic PostgreSQL ingestion."""
from __future__ import annotations

import hashlib
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path

from .content import ChildChunk, ParentSection, child_chunks, markdown_sections, normalise_text
from .inventory import CourseDescriptor, SourcePlacement, build_inventory


def sha256_text(text: str) -> str:
    return hashlib.sha256(normalise_text(text).encode("utf-8")).hexdigest()


def ordinal_value(ordinal: tuple[int, ...]) -> Decimal:
    return Decimal(".".join(str(part) for part in ordinal))


@dataclass(frozen=True)
class PreparedSource:
    placement: SourcePlacement
    extracted_text: str | None
    sections: tuple[ParentSection, ...]
    chunks: tuple[ChildChunk, ...]


@dataclass(frozen=True)
class IngestionPlan:
    courses: tuple[CourseDescriptor, ...]
    sources: tuple[PreparedSource, ...]

    @property
    def markdown_source_count(self) -> int:
        return sum(source.placement.source_type == "markdown" for source in self.sources)

    @property
    def section_count(self) -> int:
        return sum(len(source.sections) for source in self.sources)

    @property
    def chunk_count(self) -> int:
        return sum(len(source.chunks) for source in self.sources)

    def for_course(self, course_id: str) -> "IngestionPlan":
        courses = tuple(course for course in self.courses if course.course_id == course_id)
        if not courses:
            raise ValueError(f"Unknown course: {course_id}")
        return IngestionPlan(courses, tuple(source for source in self.sources if source.placement.course_id == course_id))


def build_ingestion_plan(project_root: Path) -> IngestionPlan:
    courses, placements = build_inventory(project_root)
    prepared: list[PreparedSource] = []
    for placement in placements:
        if placement.source_type != "markdown":
            prepared.append(PreparedSource(placement, None, (), ()))
            continue
        text = (project_root / placement.source_path).read_text(encoding="utf-8")
        sections = tuple(markdown_sections(text))
        chunks = tuple(chunk for section in sections for chunk in child_chunks(section))
        prepared.append(PreparedSource(placement, text, sections, chunks))
    return IngestionPlan(tuple(courses), tuple(prepared))
