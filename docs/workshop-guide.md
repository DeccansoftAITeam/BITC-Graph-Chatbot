# BestITCourses GraphRAG Workshop

## Learning path

1. Run `notebooks/00-workshop-setup.ipynb` and confirm all Azure connections.
2. Call Azure OpenAI and make embeddings in `01-azure-openai-basics.ipynb`.
3. Inspect Blob-backed documents, chunks, and vectors in `02-postgresql-documents-and-vectors.ipynb`.
4. Compare keyword, vector, and RRF retrieval in `03-hybrid-retrieval.ipynb`.
5. Query real Apache AGE nodes and edges in `04-graphrag-with-apache-age.ipynb`.
6. Run the grounded chatbot flow in `05-grounded-chatbot.ipynb`.
7. Test Azure AI Content Safety in `06-content-safety.ipynb`.
8. Configure the Student MCP in `07-student-mcp-claude-code.ipynb`.
9. Complete the admin upload-to-graph lifecycle in `08-admin-content-lifecycle.ipynb`.

## Participant setup

Copy `.env.workshop.example` to `.env`. Never commit it. Each participant must receive an individual read-only PostgreSQL account and Azure keys through a secure channel.

Start the API and web client:

```powershell
.\.venv\Scripts\course-knowledge-api.exe
cd web
npm run dev
```

## Workshop challenge

Upload one Markdown source through the Admin API. Prove it appears in Blob Storage, `sources`, `chunks`, Apache AGE, the web graph, the chatbot, and Student MCP.
