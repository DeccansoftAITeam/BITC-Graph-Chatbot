from course_knowledge.content import ParentSection, child_chunks, markdown_sections


def test_sections_keep_hierarchical_heading_context() -> None:
    sections = markdown_sections("""Intro text.

# Authentication
Use credentials.

## Managed identity
Use DefaultAzureCredential.
""")

    assert [section.heading_path for section in sections] == [
        "Document introduction", "Authentication", "Authentication > Managed identity"
    ]
    assert sections[1].text.startswith("# Authentication")


def test_child_chunks_never_exceed_maximum_word_estimate() -> None:
    section = ParentSection("test", "Test", 1, " ".join(f"word{index}" for index in range(650)))

    chunks = child_chunks(section, max_tokens=300)

    assert [chunk.token_estimate for chunk in chunks] == [300, 300, 50]
    assert [chunk.ordinal for chunk in chunks] == [1, 2, 3]


def test_small_chunk_limit_is_rejected() -> None:
    section = ParentSection("test", "Test", 1, "short text")

    try:
        child_chunks(section, max_tokens=19)
    except ValueError as error:
        assert "at least 20" in str(error)
    else:
        raise AssertionError("Expected a value error")
