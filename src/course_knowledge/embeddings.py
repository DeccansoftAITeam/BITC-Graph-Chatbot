"""Azure OpenAI batch embeddings, isolated from database and retrieval code."""
from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol

from openai import OpenAI

from .settings import AzureOpenAISettings


class EmbeddingApi(Protocol):
    class embeddings:  # type: ignore[valid-type]
        @staticmethod
        def create(*, input: Sequence[str], model: str): ...


class AzureOpenAIEmbedder:
    def __init__(self, client: EmbeddingApi, deployment: str):
        self.client = client
        self.deployment = deployment

    @classmethod
    def from_settings(cls, settings: AzureOpenAISettings) -> "AzureOpenAIEmbedder":
        endpoint = settings.embedding_endpoint.rstrip("/")
        if not endpoint.endswith("/openai/v1"):
            endpoint += "/openai/v1"
        client = OpenAI(api_key=settings.api_key, base_url=endpoint + "/")
        return cls(client, settings.embedding_deployment)

    def embed(self, texts: Sequence[str]) -> list[list[float]]:
        if not texts:
            return []
        response = self.client.embeddings.create(input=texts, model=self.deployment)
        return [list(item.embedding) for item in sorted(response.data, key=lambda item: item.index)]
