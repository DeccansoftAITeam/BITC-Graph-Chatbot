"""Shared hybrid retrieval implementation used by future MCP and chatbot APIs."""
from __future__ import annotations

import psycopg

from .database import keyword_candidates, vector_candidates
from .embeddings import AzureOpenAIEmbedder
from .retrieval import RetrievalCandidate, reciprocal_rank_fusion


class HybridRetriever:
    def __init__(self, connection: psycopg.Connection, embedder: AzureOpenAIEmbedder):
        self.connection = connection
        self.embedder = embedder

    @staticmethod
    def candidate(row: dict[str, str]) -> RetrievalCandidate:
        return RetrievalCandidate(row["chunk_id"], row["text_content"], {
            "course_key": row["course_key"], "course_title": row["course_title"],
            "module_title": row["module_title"], "source": row["canonical_filename"], "source_id": row["source_id"],
        })

    def search(self, query: str, limit: int = 5, course_key: str | None = None) -> list:
        vector = self.embedder.embed([query])[0]
        keyword = [self.candidate(row) for row in keyword_candidates(self.connection, query, limit * 3, course_key)]
        semantic = [self.candidate(row) for row in vector_candidates(self.connection, vector, limit * 3, course_key)]
        return reciprocal_rank_fusion({"keyword": keyword, "vector": semantic})[:limit]
