from course_knowledge.database import vector_literal
from course_knowledge.embeddings import AzureOpenAIEmbedder


class FakeEmbeddings:
    def create(self, *, input, model):
        assert model == "embedding-deployment"
        return type("Response", (), {"data": [type("Item", (), {"index": 1, "embedding": [2.0]}), type("Item", (), {"index": 0, "embedding": [1.0]})]})()


class FakeClient:
    embeddings = FakeEmbeddings()


def test_embeddings_are_returned_in_input_order() -> None:
    embedder = AzureOpenAIEmbedder(FakeClient(), "embedding-deployment")

    assert embedder.embed(["first", "second"]) == [[1.0], [2.0]]


def test_vector_literal_is_valid_pgvector_syntax() -> None:
    assert vector_literal([1.0, -0.25, 0.3333333333]) == "[1,-0.25,0.3333333333]"
