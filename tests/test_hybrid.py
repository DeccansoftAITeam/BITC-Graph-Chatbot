from course_knowledge.hybrid import HybridRetriever


def test_candidate_keeps_a_complete_citation() -> None:
    candidate = HybridRetriever.candidate({"chunk_id": "id", "text_content": "content", "course_key": "course",
                                             "course_title": "Course", "module_title": "Module", "canonical_filename": "source.md", "source_id": "source-id"})

    assert candidate.metadata == {"course_key": "course", "course_title": "Course", "module_title": "Module", "source": "source.md", "source_id": "source-id"}
