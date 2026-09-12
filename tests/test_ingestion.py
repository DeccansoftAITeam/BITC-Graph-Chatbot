from decimal import Decimal
from pathlib import Path

from course_knowledge.ingestion import build_ingestion_plan, ordinal_value, sha256_text


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_ingestion_plan_matches_current_course_content() -> None:
    plan = build_ingestion_plan(PROJECT_ROOT)

    assert len(plan.courses) == 2
    assert len(plan.sources) == 42
    assert plan.markdown_source_count == 41
    assert plan.section_count == 375
    assert plan.chunk_count == 527


def test_chunk_hash_normalises_line_endings_and_trailing_whitespace() -> None:
    assert sha256_text("Hello\r\nworld  \n") == sha256_text("Hello\nworld\n")


def test_decimal_module_order_preserves_sub_lessons() -> None:
    assert ordinal_value((2, 1)) == Decimal("2.1")
    assert ordinal_value((10,)) == Decimal("10")


def test_files_with_the_same_lesson_number_share_one_module() -> None:
    plan = build_ingestion_plan(PROJECT_ROOT)
    same_module = [item for item in plan.sources if item.placement.module_key == "module-2-0"]

    assert len(same_module) == 2
    assert {item.placement.item_title for item in same_module} == {"Large Project SDLC", "Small Project SDLC"}


def test_plan_can_be_safely_scoped_to_one_course() -> None:
    plan = build_ingestion_plan(PROJECT_ROOT).for_course("gh-300")

    assert [course.course_id for course in plan.courses] == ["gh-300"]
    assert all(source.placement.course_id == "gh-300" for source in plan.sources)
