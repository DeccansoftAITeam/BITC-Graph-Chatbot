from course_knowledge.retrieval import RetrievalCandidate, reciprocal_rank_fusion


def candidate(chunk_id: str) -> RetrievalCandidate:
    return RetrievalCandidate(chunk_id, f"text for {chunk_id}", {"course": "demo"})


def test_rrf_promotes_a_result_found_by_both_retrieval_legs() -> None:
    results = reciprocal_rank_fusion({"vector": [candidate("a"), candidate("b")], "keyword": [candidate("b"), candidate("c")]})

    assert [result.candidate.chunk_id for result in results] == ["b", "a", "c"]
    assert results[0].matched_legs == ("vector", "keyword")


def test_rrf_rejects_invalid_rank_constant() -> None:
    try:
        reciprocal_rank_fusion({}, constant=0)
    except ValueError as error:
        assert "positive" in str(error)
    else:
        raise AssertionError("Expected a ValueError")
