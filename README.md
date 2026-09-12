# Course GraphRAG Teaching Platform

This project demonstrates when graph augmentation improves retrieval over a conventional vector database. It treats the supplied course files as immutable source material and builds a traceable knowledge model around them.

The first implementation milestone is schema-first: source inventory, hierarchy, content-addressed sections/chunks, deterministic relationships, and an Apache AGE graph projection. No UI is part of this milestone.

## Layout

- `Courses/` — supplied source courseware; never rewritten by ingestion.
- `catalog/` — minimal course descriptors that provide facts unavailable in the file names.
- `migrations/` — PostgreSQL schema and graph projection migration.
- `src/course_knowledge/` — application package (ingestion and retrieval will live here).
- `docs/` — data-model and demonstration design.

## First local step

Copy `.env.example` to `.env`, add the PostgreSQL password locally, then run migrations with the implementation CLI once it is added. `.env` is ignored and must never be committed.
# Course Knowledge Platform

## MCP access profiles

The command-line interface remains the operator interface. REST and MCP are adapters over the same Python application service; they must never invoke the CLI as a subprocess.

Two read-only MCP servers are available:

- `course-knowledge-author-mcp`: course catalogue, module asset metadata, hybrid search, and bounded graph context for instructors/authors.
- `course-knowledge-student-mcp`: course-scoped search and grounded, cited answers. It deliberately has no ingestion, migration, reindexing, raw graph query, or author-wide search tools.

For local Claude Desktop development, install the project into its virtual environment and configure the student server as a stdio command:

```json
{
  "mcpServers": {
    "course-learning": {
      "command": "D:\\Sample-Projects\\ai-experiments\\bitc-graphrag-chatbot\\.venv\\Scripts\\course-knowledge-student-mcp.exe",
      "cwd": "D:\\Sample-Projects\\ai-experiments\\bitc-graphrag-chatbot"
    }
  }
}
```

This local profile is for development and a single trusted machine. It is not student identity enforcement: a remote deployment must authenticate the user (Microsoft Entra ID/OAuth), derive allowed course keys from enrolment claims, apply rate limits/audit logs, and expose only the student MCP tools over Streamable HTTP. That remote endpoint is what ChatGPT can connect to; it cannot directly start this local stdio server. Keep Azure OpenAI, PostgreSQL, and Content Safety keys on the server, never in the student client.

## Web/API development

Add Azure Blob Storage and the three long random static keys to `.env`. The backend provides Swagger documentation at `http://127.0.0.1:8000/docs`.

```powershell
.\.venv\Scripts\course-knowledge-api.exe
cd web
Copy-Item .env.local.example .env.local
npm install
npm run dev
```

Set `NEXT_PUBLIC_STUDENT_API_KEY` to the same development value as `STUDENT_API_KEY`. This is a prototype-only browser key: replace it with signed student sessions before public deployment. The remote student MCP endpoint is `http://127.0.0.1:8000/mcp/mcp` and expects `Authorization: Bearer <MCP_STATIC_API_KEY>`.

An admin creates courses/modules through `/docs`, then uploads Markdown or text to `POST /api/admin/modules/{course_key}/{module_key}/files`. The original file is put in Blob Storage; Markdown/text are chunked and embedded immediately, while binary formats are marked `pending_extraction` until their extractor is added.
