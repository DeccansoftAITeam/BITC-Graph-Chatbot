"""PostgreSQL migrations and canonical knowledge-model writes."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import psycopg
from psycopg.rows import dict_row

from .ingestion import IngestionPlan, ordinal_value, sha256_text
from .settings import DatabaseSettings


def connect(settings: DatabaseSettings) -> psycopg.Connection:
    return psycopg.connect(**settings.connection_kwargs, row_factory=dict_row)


def apply_migrations(connection: psycopg.Connection, migrations_directory: Path) -> None:
    for migration in sorted(migrations_directory.glob("*.sql")):
        with connection.cursor() as cursor:
            cursor.execute(migration.read_text(encoding="utf-8"))
        connection.commit()
        print(f"Applied {migration.name}")


def vector_literal(values: list[float]) -> str:
    return "[" + ",".join(format(value, ".10g") for value in values) + "]"


def pending_chunks(connection: psycopg.Connection, model: str, limit: int) -> list[dict[str, Any]]:
    with connection.cursor() as cursor:
        cursor.execute("""SELECT id, text_content FROM chunks
            WHERE embedding IS NULL OR embedding_model IS DISTINCT FROM %s ORDER BY created_at LIMIT %s""", (model, limit))
        return list(cursor.fetchall())


def store_embeddings(connection: psycopg.Connection, chunks: list[dict[str, Any]], vectors: list[list[float]], model: str) -> None:
    if len(chunks) != len(vectors):
        raise ValueError("Chunk and embedding counts differ")
    with connection.cursor() as cursor:
        cursor.executemany("UPDATE chunks SET embedding=%s::vector, embedding_model=%s WHERE id=%s",
                           [(vector_literal(vector), model, chunk["id"]) for chunk, vector in zip(chunks, vectors, strict=True)])
    connection.commit()


def _citation_rows(connection: psycopg.Connection, chunk_ids: list[str], course_key: str | None = None) -> list[dict[str, Any]]:
    if not chunk_ids:
        return []
    with connection.cursor() as cursor:
        cursor.execute("""SELECT DISTINCT ON (c.id) c.id::text AS chunk_id, c.text_content, source.id::text AS source_id,
                course.course_key, course.title AS course_title, module.title AS module_title,
                source.canonical_filename
            FROM chunks c
            JOIN section_chunks sc ON sc.chunk_id=c.id
            JOIN source_sections section ON section.id=sc.section_id
            JOIN sources source ON source.id=section.source_id
            JOIN module_sources ms ON ms.source_id=source.id
            JOIN modules module ON module.id=ms.module_id
            JOIN course_versions version ON version.id=module.course_version_id
            JOIN courses course ON course.id=version.course_id
            WHERE c.id = ANY(%s::uuid[]) AND (%s::text IS NULL OR course.course_key=%s)
            ORDER BY c.id, course.course_key, module.ordinal, section.ordinal""", (chunk_ids, course_key, course_key))
        return list(cursor.fetchall())


def keyword_candidates(connection: psycopg.Connection, query: str, limit: int, course_key: str | None = None) -> list[dict[str, Any]]:
    with connection.cursor() as cursor:
        cursor.execute("""SELECT c.id::text AS chunk_id FROM chunks c
            WHERE c.search_vector @@ websearch_to_tsquery('english', %s)
              AND (%s::text IS NULL OR EXISTS (
                SELECT 1 FROM section_chunks sc JOIN source_sections ss ON ss.id=sc.section_id
                JOIN module_sources ms ON ms.source_id=ss.source_id JOIN modules m ON m.id=ms.module_id
                JOIN course_versions v ON v.id=m.course_version_id JOIN courses course ON course.id=v.course_id
                WHERE sc.chunk_id=c.id AND course.course_key=%s))
            ORDER BY ts_rank_cd(c.search_vector, websearch_to_tsquery('english', %s)) DESC LIMIT %s""",
            (query, course_key, course_key, query, limit))
        identifiers = [row["chunk_id"] for row in cursor.fetchall()]
    citations = {row["chunk_id"]: row for row in _citation_rows(connection, identifiers, course_key)}
    return [citations[identifier] for identifier in identifiers if identifier in citations]


def vector_candidates(connection: psycopg.Connection, vector: list[float], limit: int, course_key: str | None = None) -> list[dict[str, Any]]:
    with connection.cursor() as cursor:
        cursor.execute("""SELECT c.id::text AS chunk_id FROM chunks c
            WHERE c.embedding IS NOT NULL
              AND (%s::text IS NULL OR EXISTS (
                SELECT 1 FROM section_chunks sc JOIN source_sections ss ON ss.id=sc.section_id
                JOIN module_sources ms ON ms.source_id=ss.source_id JOIN modules m ON m.id=ms.module_id
                JOIN course_versions v ON v.id=m.course_version_id JOIN courses course ON course.id=v.course_id
                WHERE sc.chunk_id=c.id AND course.course_key=%s))
            ORDER BY c.embedding <=> %s::vector LIMIT %s""", (course_key, course_key, vector_literal(vector), limit))
        identifiers = [row["chunk_id"] for row in cursor.fetchall()]
    citations = {row["chunk_id"]: row for row in _citation_rows(connection, identifiers, course_key)}
    return [citations[identifier] for identifier in identifiers if identifier in citations]


class KnowledgeWriter:
    def __init__(self, connection: psycopg.Connection):
        self.connection = connection

    def scalar(self, query: str, parameters: tuple[Any, ...]) -> Any:
        with self.connection.cursor() as cursor:
            cursor.execute(query, parameters)
            row = cursor.fetchone()
        assert row is not None
        return next(iter(row.values()))

    def ingest(self, plan: IngestionPlan) -> dict[str, int]:
        modules: dict[tuple[str, str], Any] = {}
        for course in plan.courses:
            course_id = self.scalar("""INSERT INTO courses (course_key,title,description,status) VALUES (%s,%s,%s,%s)
                ON CONFLICT (course_key) DO UPDATE SET title=EXCLUDED.title,description=EXCLUDED.description,status=EXCLUDED.status,updated_at=now() RETURNING id""",
                (course.course_id, course.title, course.description, course.status))
            version_id = self.scalar("""INSERT INTO course_versions (course_id,version_label,is_latest) VALUES (%s,%s,true)
                ON CONFLICT (course_id,version_label) DO UPDATE SET is_latest=true RETURNING id""", (course_id, course.version))
            for tag in course.technology_tags:
                technology_id = self.scalar("""INSERT INTO technologies (normalized_name,display_name) VALUES (%s,%s)
                    ON CONFLICT (normalized_name) DO UPDATE SET display_name=EXCLUDED.display_name RETURNING id""", (tag.casefold(), tag))
                with self.connection.cursor() as cursor:
                    cursor.execute("INSERT INTO course_technologies (course_id,technology_id) VALUES (%s,%s) ON CONFLICT DO NOTHING", (course_id, technology_id))
            for source in (item for item in plan.sources if item.placement.course_id == course.course_id):
                key = (course.course_id, source.placement.module_key)
                if key not in modules:
                    modules[key] = self.scalar("""INSERT INTO modules (course_version_id,module_key,title,ordinal) VALUES (%s,%s,%s,%s)
                        ON CONFLICT (course_version_id,module_key) DO UPDATE SET title=EXCLUDED.title,ordinal=EXCLUDED.ordinal RETURNING id""",
                        (version_id, source.placement.module_key, source.placement.module_title, ordinal_value(source.placement.module_ordinal)))
        source_ids: dict[str, Any] = {}
        for prepared in plan.sources:
            item = prepared.placement
            source_id = source_ids.get(item.content_sha256)
            if source_id is None:
                source_id = self.scalar("""INSERT INTO sources (content_sha256,source_type,canonical_filename,byte_size,storage_uri,extraction_status,extracted_text,extracted_at)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,CASE WHEN %s THEN now() ELSE NULL END)
                    ON CONFLICT (content_sha256) DO UPDATE SET extraction_status=EXCLUDED.extraction_status,extracted_text=EXCLUDED.extracted_text,extracted_at=EXCLUDED.extracted_at RETURNING id""",
                    (item.content_sha256, item.source_type, Path(item.source_path).name, item.byte_size, item.source_path,
                     "extracted" if prepared.extracted_text else "pending", prepared.extracted_text, prepared.extracted_text is not None))
                source_ids[item.content_sha256] = source_id
            with self.connection.cursor() as cursor:
                cursor.execute("""INSERT INTO module_sources (module_id,source_id,source_path,display_title) VALUES (%s,%s,%s,%s) ON CONFLICT DO NOTHING""",
                    (modules[(item.course_id,item.module_key)], source_id, item.source_path, item.item_title))
            for section in prepared.sections:
                section_id = self.scalar("""INSERT INTO source_sections (source_id,parent_section_key,heading_path,ordinal,text_content,token_count)
                    VALUES (%s,%s,%s,%s,%s,%s) ON CONFLICT (source_id,parent_section_key) DO UPDATE SET heading_path=EXCLUDED.heading_path,ordinal=EXCLUDED.ordinal,text_content=EXCLUDED.text_content,token_count=EXCLUDED.token_count RETURNING id""",
                    (source_id, section.key, section.heading_path, section.ordinal, section.text, len(section.text.split())))
                for chunk in (value for value in prepared.chunks if value.parent_key == section.key):
                    chunk_id = self.scalar("""INSERT INTO chunks (normalized_text_sha256,chunker_version,text_content,token_count) VALUES (%s,%s,%s,%s)
                        ON CONFLICT (normalized_text_sha256) DO UPDATE SET text_content=EXCLUDED.text_content,token_count=EXCLUDED.token_count RETURNING id""",
                        (sha256_text(chunk.text), "v1-heading-paragraph-300", chunk.text, chunk.token_estimate))
                    with self.connection.cursor() as cursor:
                        cursor.execute("""INSERT INTO section_chunks (section_id,chunk_id,ordinal) VALUES (%s,%s,%s)
                            ON CONFLICT (section_id,chunk_id) DO UPDATE SET ordinal=EXCLUDED.ordinal""", (section_id, chunk_id, chunk.ordinal))
        self.connection.commit()
        return {"courses": len(plan.courses), "sources": len(source_ids), "sections": plan.section_count, "chunks": plan.chunk_count}
