"""Deterministic, explainable source extraction and parent-child chunking."""

from __future__ import annotations

import re
from dataclasses import dataclass


HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
WORD = re.compile(r"\S+")


@dataclass(frozen=True)
class ParentSection:
    key: str
    heading_path: str
    ordinal: int
    text: str


@dataclass(frozen=True)
class ChildChunk:
    parent_key: str
    ordinal: int
    text: str
    token_estimate: int


def normalise_text(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.replace("\r\n", "\n").split("\n")).strip()


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "untitled"


def markdown_sections(text: str) -> list[ParentSection]:
    """Split Markdown at headings while retaining heading context in every parent."""
    lines = normalise_text(text).splitlines()
    sections: list[ParentSection] = []
    levels: dict[int, str] = {}
    current_lines: list[str] = []
    current_key = "document-introduction"
    current_path = "Document introduction"

    def flush() -> None:
        body = "\n".join(current_lines).strip()
        if body:
            sections.append(ParentSection(current_key, current_path, len(sections) + 1, body))

    for line in lines:
        match = HEADING.match(line)
        if not match:
            current_lines.append(line)
            continue
        flush()
        level, title = len(match.group(1)), match.group(2)
        levels[level] = title
        for deeper in [key for key in levels if key > level]:
            del levels[deeper]
        current_path = " > ".join(levels[key] for key in sorted(levels))
        current_key = f"section-{len(sections) + 1}-{slug(current_path)}"
        current_lines = [line]
    flush()
    return sections


def estimated_tokens(text: str) -> int:
    """Stable conservative estimate; model-specific token counting remains optional."""
    return len(WORD.findall(text))


def child_chunks(section: ParentSection, max_tokens: int = 300) -> list[ChildChunk]:
    if max_tokens < 20:
        raise ValueError("max_tokens must be at least 20")
    paragraphs = [part.strip() for part in re.split(r"\n\s*\n", section.text) if part.strip()]
    chunks: list[str] = []
    current: list[str] = []
    current_size = 0
    for paragraph in paragraphs:
        words = WORD.findall(paragraph)
        if len(words) > max_tokens:
            if current:
                chunks.append("\n\n".join(current))
                current, current_size = [], 0
            for start in range(0, len(words), max_tokens):
                chunks.append(" ".join(words[start : start + max_tokens]))
            continue
        if current and current_size + len(words) > max_tokens:
            chunks.append("\n\n".join(current))
            current, current_size = [], 0
        current.append(paragraph)
        current_size += len(words)
    if current:
        chunks.append("\n\n".join(current))
    return [ChildChunk(section.key, index, text, estimated_tokens(text)) for index, text in enumerate(chunks, start=1)]
