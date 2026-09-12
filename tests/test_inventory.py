from pathlib import Path

from course_knowledge.inventory import build_inventory, inventory_report


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_inventory_reads_both_course_descriptors() -> None:
    courses, placements = build_inventory(PROJECT_ROOT)
    report = inventory_report(courses, placements)

    assert {course.course_id for course in courses} == {"gh-300", "openai-courseware"}
    assert all(course.description for course in courses)
    assert report["summary"]["source_placements"] == 42
    assert report["summary"]["unique_sources"] == 42
    assert report["summary"]["duplicate_source_groups"] == 0


def test_every_placement_has_a_source_hash_and_type() -> None:
    _, placements = build_inventory(PROJECT_ROOT)

    assert all(len(placement.content_sha256) == 64 for placement in placements)
    assert {placement.source_type for placement in placements} == {"markdown", "pdf"}
    assert all(placement.item_title for placement in placements)
