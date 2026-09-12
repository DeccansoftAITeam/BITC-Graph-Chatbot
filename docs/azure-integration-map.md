# Azure Service Integration Map

The platform demonstrates a complete Azure AI application while keeping retrieval explainable.

| Azure capability | Application responsibility | Graph connection | Phase |
|---|---|---|---|
| Microsoft Foundry SDK | Call the selected teaching/answer model; later run an optional guided-agent lab | `Technology: Microsoft Foundry` linked to labs and sources | 1 |
| Azure OpenAI | Batch embeddings during ingestion; query embeddings and grounded answer generation | Embedding-bearing chunks retain the model deployment used | 1 |
| Azure Communication Services | Real-time learner/instructor chat or notifications; store only thread reference and opted-in feedback | A learner question can be linked to a cited source as feedback, not as corpus truth | 2 |
| Azure Database for PostgreSQL | Canonical course model, full-text search, pgvector embeddings, and Apache AGE graph traversal | This is where graph nodes and edges live | 1 |
| Azure Blob Storage | Immutable binary course assets: PDFs, recordings, video, images, and original uploads | `sources.storage_uri` points to the blob; hash guarantees identity | 1 |
| Azure AI Content Safety | Moderate learner input and generated answers; optionally flag new submitted material for review | Safety event is audit metadata, never a semantic course relationship | 1 |

## Design boundary

PostgreSQL is the single **knowledge database**, not the only Azure service. Blob Storage holds binary files; Azure OpenAI/Foundry provide model calls; Content Safety moderates requests and replies; ACS provides communications. The course hierarchy, source provenance, chunks, vectors, and graph live in PostgreSQL.

## Demonstration flow

```text
Learner question
  → Content Safety (input gate)
  → PostgreSQL: keyword + vector retrieval + bounded AGE expansion
  → Azure OpenAI / Foundry model: grounded response
  → Content Safety (output gate)
  → response with source citation and visible graph path

Course upload → Blob Storage (original) → PostgreSQL sources/sections/chunks/graph
```

Azure Communication Services is intentionally outside the retrieval critical path. It can carry an instructor-learner conversation, notifications, or escalation, but a normal RAG answer should not depend on it.
