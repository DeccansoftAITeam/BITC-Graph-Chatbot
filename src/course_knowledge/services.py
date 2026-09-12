"""Application service boundary shared by the CLI, REST API, and MCP adapters."""
from __future__ import annotations

from dataclasses import asdict
from typing import Any

from .answers import GroundedAnswerer
from .database import connect
from .embeddings import AzureOpenAIEmbedder
from .graph_retrieval import GraphExpander
from .hybrid import HybridRetriever
from .safety import ContentSafetyGate
from .settings import azure_openai_settings, content_safety_settings, database_settings


class CourseKnowledgeService:
    """Read-only use cases. Adapters must call this class, never shell out to the CLI."""

    def list_courses(self) -> list[dict[str, Any]]:
        with connect(database_settings()) as connection, connection.cursor() as cursor:
            cursor.execute("""SELECT course_key, title, description, status
                FROM courses ORDER BY title""")
            return list(cursor.fetchall())

    def list_modules(self, course_key: str) -> list[dict[str, Any]]:
        with connect(database_settings()) as connection, connection.cursor() as cursor:
            cursor.execute("""SELECT m.module_key, m.title, m.ordinal
                FROM modules m JOIN course_versions v ON v.id=m.course_version_id
                JOIN courses c ON c.id=v.course_id
                WHERE c.course_key=%s AND v.is_latest ORDER BY m.ordinal""", (course_key,))
            return list(cursor.fetchall())

    def module_content(self, course_key: str, module_key: str) -> list[dict[str, Any]]:
        with connect(database_settings()) as connection, connection.cursor() as cursor:
            cursor.execute("""SELECT ms.display_title, s.canonical_filename, ms.source_path, s.source_type
                FROM module_sources ms JOIN modules m ON m.id=ms.module_id
                JOIN course_versions v ON v.id=m.course_version_id JOIN courses c ON c.id=v.course_id
                JOIN sources s ON s.id=ms.source_id
                WHERE c.course_key=%s AND m.module_key=%s AND v.is_latest
                ORDER BY ms.source_path""", (course_key, module_key))
            return list(cursor.fetchall())

    def search(self, query: str, limit: int = 5, course_key: str | None = None, graph_context: bool = False) -> list[dict[str, Any]]:
        limit = _bounded_limit(limit)
        azure = azure_openai_settings()
        with connect(database_settings()) as connection:
            results = HybridRetriever(connection, AzureOpenAIEmbedder.from_settings(azure)).search(query, limit, course_key)
            expander = GraphExpander(connection) if graph_context else None
            payload = []
            for result in results:
                item = {
                    "citation": result.candidate.metadata,
                    "matched_legs": list(result.matched_legs),
                    "score": round(result.rrf_score, 6),
                    "excerpt": result.candidate.text[:1200],
                }
                if expander:
                    item["graph_context"] = [asdict(value) for value in expander.from_source(result.candidate.metadata["source_id"])]
                payload.append(item)
            return payload

    def ask(self, question: str, course_key: str | None = None, limit: int = 5, moderate: bool = True) -> dict[str, Any]:
        limit = _bounded_limit(limit)
        safety = ContentSafetyGate.from_settings(content_safety_settings()) if moderate else None
        if safety and not safety.assess(question).allowed:
            return {"blocked": True, "reason": "Question blocked by Content Safety."}
        azure = azure_openai_settings()
        with connect(database_settings()) as connection:
            results = HybridRetriever(connection, AzureOpenAIEmbedder.from_settings(azure)).search(question, limit, course_key)
            contexts = {result.candidate.metadata["source_id"]: GraphExpander(connection).from_source(result.candidate.metadata["source_id"]) for result in results}
            answer = GroundedAnswerer(azure).answer(question, results, contexts)
        if safety and not safety.assess(answer.text).allowed:
            return {"blocked": True, "reason": "Generated answer blocked by Content Safety."}
        return {"blocked": False, "answer": answer.text, "citations": list(answer.citations)}


def _bounded_limit(limit: int) -> int:
    if not 1 <= limit <= 10:
        raise ValueError("limit must be between 1 and 10")
    return limit
