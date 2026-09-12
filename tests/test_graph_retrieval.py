from course_knowledge.graph_retrieval import agtype_text


def test_agtype_text_decodes_age_json_strings() -> None:
    assert agtype_text('"OpenAI Developer Courseware"') == "OpenAI Developer Courseware"


def test_agtype_text_preserves_non_json_values() -> None:
    assert agtype_text("Module 11") == "Module 11"
