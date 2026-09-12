"""Create a deterministic, content-addressed inventory of supplied course files.

This stage does not write to PostgreSQL. It makes the source model reviewable before
database ingestion and proves that duplicate assets receive one canonical hash.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path


EXTENSION_TO_TYPE = {
    ".md": "markdown",
    ".pdf": "pdf",
    ".docx": "docx",
    ".txt": "transcript",
    ".mp4": "video",
}


@dataclass(frozen=True)
class CourseDescriptor:
    course_id: str
    title: str
    version: str
    status: str
    description: str
    source_root: str
    technology_tags: list[str]


@dataclass(frozen=True)
class SourcePlacement:
    course_id: str
    module_key: str
    module_title: str
    item_title: str
    module_ordinal: tuple[int, ...]
    source_path: str
    source_type: str
    byte_size: int
    content_sha256: str


def parse_descriptor(path: Path) -> CourseDescriptor:
    """Parse the intentionally small catalog YAML subset without runtime dependencies."""
    values: dict[str, str | list[str]] = {"technology_tags": []}
    reading_tags = False
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        if raw_line.startswith("  - ") and reading_tags:
            assert isinstance(values["technology_tags"], list)
            values["technology_tags"].append(raw_line[4:].strip())
            continue
        reading_tags = raw_line.strip() == "technology_tags:"
        if ":" in raw_line and not reading_tags:
            key, value = raw_line.split(":", 1)
            values[key.strip()] = value.strip().strip('"')
    required = ("course_id", "title", "version", "status", "description", "source_root")
    missing = [key for key in required if not values.get(key)]
    if missing:
        raise ValueError(f"{path}: missing {', '.join(missing)}")
    return CourseDescriptor(
        course_id=str(values["course_id"]), title=str(values["title"]),
        version=str(values["version"]), status=str(values["status"]), description=str(values["description"]),
        source_root=str(values["source_root"]),
        technology_tags=list(values["technology_tags"]),
    )


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def module_details(path: Path) -> tuple[str, str, str, tuple[int, ...]]:
    stem = path.stem
    match = re.match(r"^(\d+(?:\.\d+)?)\s*-\s*(.+)$", stem)
    if match:
        ordinal = tuple(int(part) for part in match.group(1).split("."))
        item_title = match.group(2).strip()
        module_title = f"Module {match.group(1)}"
        key = "module-" + "-".join(str(part) for part in ordinal)
    else:
        ordinal, item_title, module_title = (9999,), stem, stem
        key = re.sub(r"[^a-z0-9]+", "-", item_title.lower()).strip("-")
    return key, module_title, item_title, ordinal


def build_inventory(project_root: Path) -> tuple[list[CourseDescriptor], list[SourcePlacement]]:
    descriptors = [parse_descriptor(path) for path in sorted((project_root / "catalog").glob("*.yaml"))]
    placements: list[SourcePlacement] = []
    for course in descriptors:
        root = project_root / course.source_root
        if not root.is_dir():
            raise FileNotFoundError(f"Source root does not exist: {root}")
        for file in sorted(path for path in root.rglob("*") if path.is_file()):
            module_key, module_title, item_title, module_ordinal = module_details(file)
            placements.append(SourcePlacement(
                course_id=course.course_id, module_key=module_key, module_title=module_title,
                item_title=item_title,
                module_ordinal=module_ordinal, source_path=file.relative_to(project_root).as_posix(),
                source_type=EXTENSION_TO_TYPE.get(file.suffix.lower(), "other"),
                byte_size=file.stat().st_size, content_sha256=file_hash(file),
            ))
    return descriptors, placements


def inventory_report(descriptors: list[CourseDescriptor], placements: list[SourcePlacement]) -> dict:
    unique_hashes = {item.content_sha256 for item in placements}
    duplicate_groups: dict[str, list[str]] = {}
    for item in placements:
        duplicate_groups.setdefault(item.content_sha256, []).append(item.source_path)
    duplicates = [paths for paths in duplicate_groups.values() if len(paths) > 1]
    return {
        "schema_version": 1,
        "courses": [asdict(item) for item in descriptors],
        "summary": {
            "course_count": len(descriptors), "source_placements": len(placements),
            "unique_sources": len(unique_hashes), "duplicate_source_groups": len(duplicates),
        },
        "duplicate_source_groups": duplicates,
        "source_placements": [asdict(item) for item in placements],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Inventory course sources before PostgreSQL ingestion.")
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path, default=Path("var/source-inventory.json"))
    args = parser.parse_args()
    root = args.project_root.resolve()
    descriptors, placements = build_inventory(root)
    output = args.output if args.output.is_absolute() else root / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(inventory_report(descriptors, placements), indent=2) + "\n", encoding="utf-8")
    print(f"Inventory written to {output}")


if __name__ == "__main__":
    main()
