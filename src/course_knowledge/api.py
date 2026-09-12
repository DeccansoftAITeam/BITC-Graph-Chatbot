"""HTTP API and authenticated remote MCP host for BestITCourses."""
from __future__ import annotations

from hashlib import sha256
import json
from os import getenv
from pathlib import Path
from uuid import uuid4

import uvicorn
from fastapi import Depends, FastAPI, File, Header, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from .database import connect
from .database import store_embeddings
from .content import child_chunks, markdown_sections
from .embeddings import AzureOpenAIEmbedder
from .graph import GraphProjector
from .mcp_servers import create_student_server
from .services import CourseKnowledgeService
from .settings import azure_openai_settings, blob_storage_settings, database_settings
from .storage import BlobAssetStore

load_dotenv(override=True)


def _key(expected_name: str):
    def verify(x_api_key: str | None = Header(default=None)) -> None:
        expected = getenv(expected_name)
        if not expected or x_api_key != expected:
            raise HTTPException(401, "Invalid API key")
    return verify


student_key = _key("STUDENT_API_KEY")
admin_key = _key("ADMIN_API_KEY")


class ChatRequest(BaseModel):
    course_key: str | None = None
    question: str = Field(min_length=3, max_length=4000)


class CourseCreate(BaseModel):
    course_key: str = Field(pattern=r"^[a-z0-9-]+$")
    title: str
    description: str = ""


class ModuleCreate(BaseModel):
    course_key: str
    module_key: str = Field(pattern=r"^[a-z0-9-]+$")
    title: str
    ordinal: float = Field(gt=0)


app = FastAPI(title="BestITCourses API", version="0.2.0")
app.add_middleware(CORSMiddleware, allow_origins=[getenv("WEB_ORIGIN", "http://localhost:3000")], allow_methods=["*"], allow_headers=["*"])


def index_markdown(connection, source_id: str, text: str) -> None:
    """Synchronously index small Markdown uploads; binary formats stay pending for an extractor job."""
    chunks_to_embed: list[dict] = []
    with connection.cursor() as cursor:
        for section in markdown_sections(text):
            cursor.execute("""INSERT INTO source_sections(source_id,parent_section_key,heading_path,ordinal,text_content,token_count)
                VALUES(%s,%s,%s,%s,%s,%s) ON CONFLICT(source_id,parent_section_key) DO UPDATE SET text_content=EXCLUDED.text_content
                RETURNING id::text""", (source_id, section.key, section.heading_path, section.ordinal, section.text, len(section.text.split())))
            section_id = cursor.fetchone()["id"]
            for chunk in child_chunks(section):
                digest = sha256(chunk.text.encode()).hexdigest()
                cursor.execute("""INSERT INTO chunks(normalized_text_sha256,chunker_version,text_content,token_count)
                    VALUES(%s,'v1-heading-paragraph-300',%s,%s) ON CONFLICT(normalized_text_sha256) DO UPDATE SET text_content=EXCLUDED.text_content
                    RETURNING id::text,text_content""", (digest, chunk.text, chunk.token_estimate))
                row = cursor.fetchone()
                cursor.execute("INSERT INTO section_chunks(section_id,chunk_id,ordinal) VALUES(%s,%s,%s) ON CONFLICT(section_id,chunk_id) DO UPDATE SET ordinal=EXCLUDED.ordinal", (section_id, row["id"], chunk.ordinal))
                chunks_to_embed.append({"id": row["id"], "text_content": row["text_content"]})
    if chunks_to_embed:
        settings = azure_openai_settings()
        vectors = AzureOpenAIEmbedder.from_settings(settings).embed([row["text_content"] for row in chunks_to_embed])
        store_embeddings(connection, chunks_to_embed, vectors, settings.embedding_deployment)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "bestitcourses-api"}


@app.get("/api/courses", dependencies=[Depends(student_key)])
def courses() -> list[dict]:
    return CourseKnowledgeService().list_courses()


@app.get("/api/courses/{course_key}/modules", dependencies=[Depends(student_key)])
def modules(course_key: str) -> list[dict]:
    return CourseKnowledgeService().list_modules(course_key)


@app.get("/api/library", dependencies=[Depends(student_key)])
def library() -> list[dict]:
    """Dynamic course/module/document map used by the student course library."""
    with connect(database_settings()) as connection, connection.cursor() as cursor:
        cursor.execute("""SELECT c.course_key, c.title AS course_title, m.module_key, m.title AS module_title,
            m.ordinal, s.id::text AS source_id, s.canonical_filename, s.source_type, s.storage_uri
            FROM courses c JOIN course_versions v ON v.course_id=c.id AND v.is_latest
            JOIN modules m ON m.course_version_id=v.id LEFT JOIN module_sources ms ON ms.module_id=m.id
            LEFT JOIN sources s ON s.id=ms.source_id ORDER BY c.title,m.ordinal,ms.ordinal,s.canonical_filename""")
        return list(cursor.fetchall())


def _age_entity(value: object) -> dict:
    """Convert AGE's JSON-with-::vertex/::edge suffix to API-safe JSON."""
    return json.loads(str(value).rsplit("::", 1)[0])


@app.get("/api/graph", dependencies=[Depends(student_key)])
def graph() -> dict:
    """Read the real Apache AGE projection, not a UI-generated approximation."""
    with connect(database_settings()) as connection, connection.cursor() as cursor:
        cursor.execute('SET search_path = ag_catalog, "$user", public')
        cursor.execute("""SELECT * FROM cypher('course_graph', $$ MATCH (n)-[r]->(m) RETURN n,r,m $$)
            AS (node agtype, edge agtype, target agtype)""")
        nodes: dict[str, dict] = {}
        edges: dict[str, dict] = {}
        for row in cursor.fetchall():
            node, edge, target = (_age_entity(row[key]) for key in ("node", "edge", "target"))
            nodes[str(node["id"])] = node
            nodes[str(target["id"])] = target
            edges[str(edge["id"])] = edge
    return {"nodes": list(nodes.values()), "edges": list(edges.values())}


@app.post("/api/chat", dependencies=[Depends(student_key)])
def chat(request: ChatRequest) -> dict:
    return CourseKnowledgeService().ask(request.question, request.course_key, moderate=True)


@app.post("/api/admin/courses", dependencies=[Depends(admin_key)])
def create_course(request: CourseCreate) -> dict:
    with connect(database_settings()) as connection, connection.cursor() as cursor:
        cursor.execute("""INSERT INTO courses(course_key,title,description,status) VALUES (%s,%s,%s,'draft') RETURNING id::text""", (request.course_key, request.title, request.description))
        course_id = cursor.fetchone()["id"]
        cursor.execute("INSERT INTO course_versions(course_id,version_label,is_latest) VALUES (%s,'1.0',true)", (course_id,))
        connection.commit()
        GraphProjector(connection).sync()
    return {"course_key": request.course_key, "status": "draft"}


@app.post("/api/admin/modules", dependencies=[Depends(admin_key)])
def create_module(request: ModuleCreate) -> dict:
    with connect(database_settings()) as connection, connection.cursor() as cursor:
        cursor.execute("""INSERT INTO modules(course_version_id,module_key,title,ordinal)
            SELECT v.id,%s,%s,%s FROM course_versions v JOIN courses c ON c.id=v.course_id
            WHERE c.course_key=%s AND v.is_latest RETURNING id::text""", (request.module_key, request.title, request.ordinal, request.course_key))
        if not cursor.fetchone():
            raise HTTPException(404, "Course not found")
        connection.commit()
        GraphProjector(connection).sync()
    return {"course_key": request.course_key, "module_key": request.module_key}


@app.post("/api/admin/modules/{course_key}/{module_key}/files", dependencies=[Depends(admin_key)])
async def upload_file(course_key: str, module_key: str, file: UploadFile = File(...)) -> dict:
    content = await file.read()
    if not content or len(content) > 25 * 1024 * 1024:
        raise HTTPException(400, "File must be between 1 byte and 25 MB")
    filename = Path(file.filename or "upload.bin").name
    digest = sha256(content).hexdigest()
    blob_uri = BlobAssetStore(blob_storage_settings()).upload(f"courses/{course_key}/{module_key}/{digest}-{filename}", content, file.content_type)
    source_type = "markdown" if filename.lower().endswith((".md", ".txt")) else "other"
    extracted_text = content.decode("utf-8") if source_type == "markdown" else None
    with connect(database_settings()) as connection, connection.cursor() as cursor:
        cursor.execute("""INSERT INTO sources(content_sha256,source_type,media_type,canonical_filename,byte_size,storage_uri,extraction_status,extracted_text,extracted_at)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,CASE WHEN %s IS NULL THEN NULL ELSE now() END)
            ON CONFLICT(content_sha256) DO UPDATE SET storage_uri=EXCLUDED.storage_uri RETURNING id::text""",
            (digest, source_type, file.content_type, filename, len(content), blob_uri, "extracted" if extracted_text else "pending", extracted_text, extracted_text))
        source_id = cursor.fetchone()["id"]
        cursor.execute("""INSERT INTO module_sources(module_id,source_id,source_path,display_title)
            SELECT m.id,%s,%s,%s FROM modules m JOIN course_versions v ON v.id=m.course_version_id JOIN courses c ON c.id=v.course_id
            WHERE c.course_key=%s AND m.module_key=%s AND v.is_latest ON CONFLICT DO NOTHING""", (source_id, blob_uri, filename, course_key, module_key))
        if extracted_text:
            index_markdown(connection, source_id, extracted_text)
        connection.commit()
        GraphProjector(connection).sync()
    return {"source_id": source_id, "filename": filename, "blob_uri": blob_uri, "index_status": "indexed" if extracted_text else "pending_extraction"}


@app.middleware("http")
async def secure_mcp(request, call_next):
    if request.url.path.startswith("/mcp"):
        expected = getenv("MCP_STATIC_API_KEY")
        if not expected or request.headers.get("authorization") != f"Bearer {expected}":
            from fastapi.responses import JSONResponse
            return JSONResponse({"detail": "Invalid MCP bearer token"}, status_code=401)
    return await call_next(request)


app.mount("/mcp", create_student_server().streamable_http_app())


def run() -> None:
    uvicorn.run("course_knowledge.api:app", host=getenv("API_HOST", "127.0.0.1"), port=int(getenv("API_PORT", "8000")))
