"""Bounded, read-only AGE graph expansion for retrieved source assets."""
from __future__ import annotations

import json
from dataclasses import dataclass

import psycopg

from .graph import cypher_string


def agtype_text(value: object) -> str:
    text = str(value)
    try:
        decoded = json.loads(text)
        return str(decoded)
    except json.JSONDecodeError:
        return text.strip('"')


@dataclass(frozen=True)
class GraphContext:
    module: str
    course: str
    technology: str


class GraphExpander:
    def __init__(self, connection: psycopg.Connection):
        self.connection = connection

    def from_source(self, source_id: str) -> list[GraphContext]:
        statement = f"""MATCH (s:Source {{id:{cypher_string(source_id)}}})<-[:HAS_SOURCE]-(m:Module)<-[:HAS_MODULE]-(c:Course)-[:USES_TECHNOLOGY]->(t:Technology)
            RETURN m.title, c.title, t.name"""
        delimiter = "$expand$"
        with self.connection.cursor() as cursor:
            cursor.execute('SET search_path = ag_catalog, "$user", public')
            cursor.execute(f"SELECT * FROM cypher('course_graph', {delimiter}{statement}{delimiter}) AS (module agtype, course agtype, technology agtype)")
            rows = cursor.fetchall()
        return [GraphContext(agtype_text(row["module"]), agtype_text(row["course"]), agtype_text(row["technology"])) for row in rows]
