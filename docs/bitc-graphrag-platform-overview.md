# BITC Knowledge Graph Learning Platform

## 1. Project name

**BITC Knowledge Graph Learning Platform**

A teaching platform that demonstrates how GraphRAG improves course discovery, learning assistance, and source-grounded answers over vector-only retrieval.

## 2. Product features

### Student Learning Assistant

- Browse courses, modules, and source documents.
- Ask questions across one or many courses.
- Receive grounded answers with course, module, and document citations.
- Explore the live course knowledge graph.

### Author Learning Assistant

- Create and manage courses, modules, and documents.
- Upload original course documents to Azure Blob Storage.
- Trigger extraction, chunking, embeddings, and graph projection.
- Inspect retrieval evidence and graph relationships.

### Chatbot

- Next.js learning interface backed by FastAPI.
- Hybrid retrieval and grounded Azure OpenAI answers.
- Azure AI Content Safety checks for student prompts and generated answers.

### MCP servers

- **BITC Student Learning MCP**: constrained learning/search/ask tools for course consumers.
- **BITC Authoring Knowledge MCP**: catalogue, module, source metadata, and graph-aware author tools.
- Local stdio support for Claude-compatible clients; remote Streamable HTTP support for hosted MCP clients.

### Visual Graph Explorer

- Visualizes real Apache AGE nodes and edges.
- Shows Course, Module, Source/Document, and Technology relationships.
- Supports graph exploration as a teaching aid, not merely as a hidden retrieval implementation detail.

## 3. Dynamic knowledge lifecycle

When an author creates or updates learning content:

```text
Course / module / document created
        ↓
Original document uploaded to Azure Blob Storage
        ↓
Metadata linked in PostgreSQL
        ↓
Text extracted into sections and chunks
        ↓
Azure OpenAI embeddings stored through pgvector
        ↓
Apache AGE nodes and edges are merged into the course graph
        ↓
Content becomes available to search, chat, and MCP clients
```

The relational tables remain the canonical source of truth. AGE is a deterministic graph projection which can be rebuilt from the relational data.

## 4. Why GraphRAG instead of only a vector database?

Vector search is excellent for finding text that is semantically similar to a question. It does not inherently understand explicit relationships such as prerequisites, module membership, shared technology, dependencies, or source provenance.

| Approach | Strength | Limitation |
|---|---|---|
| Keyword search | Exact terms, filenames, acronyms, known product names | Misses paraphrases and conceptual similarity |
| Vector search | Semantic similarity and natural-language questions | Does not natively traverse or reason over explicit relationships |
| GraphRAG | Retrieves evidence and expands/ranks it using verified relationships | Requires deliberate graph modelling and lifecycle management |

The BITC retrieval demonstration is:

```text
Keyword candidates + vector candidates + graph-related candidates
                         ↓
                 Reciprocal Rank Fusion
                         ↓
      Grounded answer with citations and graph context
```

## 5. Questions where GraphRAG adds value

These questions require relationship traversal, filtering, or multi-hop context that similarity alone cannot reliably guarantee:

- “Which modules should I complete before the MCP module?”
- “Show all documents connected to Azure OpenAI through the course graph.”
- “Which courses teach both embeddings and Model Context Protocol?”
- “What GitHub Copilot content is related to concepts taught in the OpenAI course?”
- “Which source documents belong to modules that use a specific technology?”
- “Why is this module recommended after another module?”

A vector database can return text that mentions the concepts. GraphRAG can prove and navigate the explicit course/module/source/technology path behind the answer.

## 6. Real-world GraphRAG use cases

- Enterprise knowledge assistants: connect policy, procedure, team, product, and document relationships.
- Customer support: trace product, version, error, workaround, and knowledge-base relationships.
- Software engineering: connect repository, service, API, owner, dependency, issue, and runbook data.
- Learning platforms: connect course, module, objective, prerequisite, assessment, document, and technology data.
- Research assistants: connect paper, author, claim, dataset, method, and citation relationships.
- Compliance and risk: connect regulation, control, evidence, process, system, and owner relationships.

## 7. GraphRAG implementation options

### Azure Cosmos DB

Use when a globally distributed operational application needs managed graph/document storage at scale. Cosmos DB can model connected entities and serve graph-oriented application workloads.

### Neo4j

Use when graph modelling, Cypher queries, graph algorithms, and deep relationship analysis are the central product capability. Neo4j provides a graph-native developer experience and mature visualization tooling.

### PostgreSQL with Apache AGE

Use when relational business data, full-text search, vectors, and graph projection should remain in one database platform. This is the chosen BITC implementation because it makes the data lifecycle clear for students.

## 8. BITC implementation

| Component | Technology | Responsibility |
|---|---|---|
| Web application | Next.js | Student/author learning experience and visual graph explorer |
| API | Python FastAPI | Chat, course library, administration, upload, and remote MCP host |
| Relational data | Azure Database for PostgreSQL | Canonical course/module/source/chunk metadata |
| Vector retrieval | pgvector | Azure OpenAI embedding storage and similarity search |
| Graph | Apache AGE | Course, module, source, and technology nodes/edges |
| AI extension | `azure_ai` | In-database Azure AI capabilities; available for teaching semantic operations |
| Embeddings and chat | Azure OpenAI / Foundry | `text-embedding-3-large` embeddings and grounded responses |
| Source files | Azure Blob Storage | Original uploaded course documents |
| Safety | Azure AI Content Safety | Prompt and answer moderation |
| Extensibility | MCP | Student and author access from compatible AI clients |

## 9. Teaching demonstrations

1. Compare keyword-only retrieval with vector-only retrieval.
2. Show RRF hybrid retrieval and its evidence chunks.
3. Display the AGE graph path that supplies curriculum context.
4. Compare a vector-only answer with a graph-aware answer for a multi-hop query.
5. Create a new course/module/document and show the new database rows, embedding, node, and edge.
6. Query the same content through the web chatbot and Student MCP server.
7. Demonstrate source citations, Blob-backed documents, and Content Safety controls.

## 10. Important design principles

- Keep raw files in Blob Storage; store metadata and extracted knowledge in PostgreSQL.
- Keep PostgreSQL relational data canonical; make the AGE graph rebuildable.
- Never treat graph structure as teaching evidence unless a cited source supports the claim.
- Keep author capabilities separate from student capabilities.
- Use citations for every grounded answer.
- Start with keyword + vector + graph RRF; make model-based reranking an optional advanced demonstration.

## 11. Future enhancements

- Microsoft Entra ID authentication and course enrolment authorization.
- Short-lived SAS links for private document citations.
- Background extraction for PDF, DOCX, and PPTX files.
- Incremental graph outbox worker instead of full projection synchronization.
- Retrieval evaluation dataset with real anonymized student questions.
- Optional `azure_ai.rank()` semantic reranking experiment.
