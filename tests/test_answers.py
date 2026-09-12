from course_knowledge.answers import build_prompt
from course_knowledge.retrieval import FusedCandidate, RetrievalCandidate


def test_prompt_contains_evidence_and_citation_numbers() -> None:
    result = FusedCandidate(RetrievalCandidate("chunk", "MCP is a protocol.", {
        "course_title": "OpenAI Course", "module_title": "Module 11", "source": "mcp.md", "source_id": "source"
    }), 0.1, ("vector",))

    prompt, citations = build_prompt("What is MCP?", [result], {})

    assert "[1] OpenAI Course | Module 11 | mcp.md" in prompt
    assert "Answer only from the supplied evidence" in prompt
    assert citations == ("OpenAI Course | Module 11 | mcp.md",)
