from course_knowledge.evaluation import source_hit, summarize
from course_knowledge.retrieval import FusedCandidate, RetrievalCandidate


def result(course_key: str, source: str) -> FusedCandidate:
    return FusedCandidate(RetrievalCandidate("chunk", "text", {"course_key": course_key, "source": source}), 1.0, ("vector",))


def test_source_hit_uses_expected_course_and_source_pair() -> None:
    assert source_hit([result("openai-courseware", "mcp.md")], (("openai-courseware", "mcp.md"),))
    assert not source_hit([result("gh-300", "mcp.md")], (("openai-courseware", "mcp.md"),))


def test_summary_handles_empty_and_nonempty_results() -> None:
    assert summarize([]) == {"questions": 0, "source_hit_rate": 0.0}
    assert summarize([True, False, True]) == {"questions": 3, "source_hit_rate": 2 / 3}
