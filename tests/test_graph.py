from course_knowledge.graph import cypher_string


def test_cypher_strings_escape_quotes_and_backslashes() -> None:
    assert cypher_string("O'Reilly\\course") == "'O\\'Reilly\\\\course'"
