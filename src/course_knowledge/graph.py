"""Project verified relational course facts into Apache AGE."""
from __future__ import annotations

from typing import Any

import psycopg


def cypher_string(value: Any) -> str:
    """Quote values for the small, internally generated AGE Cypher surface."""
    return "'" + str(value).replace("\\", "\\\\").replace("'", "\\'") + "'"


class GraphProjector:
    """AGE is a derived, rebuildable graph; relational PostgreSQL remains canonical."""

    def __init__(self, connection: psycopg.Connection):
        self.connection = connection

    def execute(self, statement: str) -> None:
        delimiter_index = 0
        delimiter = "$course_graph$"
        while delimiter in statement:
            delimiter_index += 1
            delimiter = f"$course_graph_{delimiter_index}$"
        with self.connection.cursor() as cursor:
            cursor.execute('SET search_path = ag_catalog, "$user", public')
            cursor.execute(f"SELECT * FROM cypher('course_graph', {delimiter}{statement}{delimiter}) AS (result agtype)")

    def rows(self, query: str) -> list[dict[str, Any]]:
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            return list(cursor.fetchall())

    def sync(self) -> dict[str, int]:
        courses = self.rows("SELECT id, course_key, title FROM courses")
        modules = self.rows("""SELECT m.id, m.module_key, m.title, m.ordinal, c.id AS course_id
            FROM modules m JOIN course_versions cv ON cv.id=m.course_version_id JOIN courses c ON c.id=cv.course_id""")
        sources = self.rows("SELECT id, canonical_filename, source_type FROM sources")
        technologies = self.rows("SELECT id, normalized_name, display_name FROM technologies")
        module_sources = self.rows("SELECT module_id, source_id FROM module_sources")
        course_technologies = self.rows("SELECT course_id, technology_id FROM course_technologies")
        for course in courses:
            self.execute(f"MERGE (n:Course {{id:{cypher_string(course['id'])}}}) SET n.course_key={cypher_string(course['course_key'])}, n.title={cypher_string(course['title'])}")
        for module in modules:
            self.execute(f"MERGE (n:Module {{id:{cypher_string(module['id'])}}}) SET n.module_key={cypher_string(module['module_key'])}, n.title={cypher_string(module['title'])}, n.ordinal={cypher_string(module['ordinal'])}")
            self.execute(f"MATCH (c:Course {{id:{cypher_string(module['course_id'])}}}), (m:Module {{id:{cypher_string(module['id'])}}}) MERGE (c)-[:HAS_MODULE]->(m)")
        for source in sources:
            self.execute(f"MERGE (n:Source {{id:{cypher_string(source['id'])}}}) SET n.filename={cypher_string(source['canonical_filename'])}, n.source_type={cypher_string(source['source_type'])}")
        for technology in technologies:
            self.execute(f"MERGE (n:Technology {{id:{cypher_string(technology['id'])}}}) SET n.name={cypher_string(technology['display_name'])}, n.normalized_name={cypher_string(technology['normalized_name'])}")
        for relation in module_sources:
            self.execute(f"MATCH (m:Module {{id:{cypher_string(relation['module_id'])}}}), (s:Source {{id:{cypher_string(relation['source_id'])}}}) MERGE (m)-[:HAS_SOURCE]->(s)")
        for relation in course_technologies:
            self.execute(f"MATCH (c:Course {{id:{cypher_string(relation['course_id'])}}}), (t:Technology {{id:{cypher_string(relation['technology_id'])}}}) MERGE (c)-[:USES_TECHNOLOGY]->(t)")
        self.connection.commit()
        return {"nodes": len(courses) + len(modules) + len(sources) + len(technologies),
                "edges": len(modules) + len(module_sources) + len(course_technologies)}
