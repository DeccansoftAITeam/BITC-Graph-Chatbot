# GraphRAG Demonstration Scenarios

The application will always show the retrieved chunks and their citations. For selected questions, it will also show the deterministic graph path used to widen context. This makes the graph contribution inspectable rather than a black box.

| Question | Vector-only result | Graph contribution | Visible teaching point |
|---|---|---|---|
| What is MCP? | Relevant definitions in either course | Connect each definition to its course and surrounding module | Same concept, different course context |
| Which courses teach MCP and where? | Requires many similarity results and grouping | `Technology → Course → Module → Source` traversal | Precise catalog navigation |
| What should a learner take before GitHub Copilot agents? | Finds agent-related chunks | Follows reviewed `PREREQUISITE_OF` edges | Explicit curriculum sequencing |
| Why did this answer cite two MCP files? | May return overlapping passages | Shows the distinct source assets and their shared/reused child chunks | Provenance without false deduplication |
| Show the RAG material and its related embedding material | Similar passages, possibly incomplete | Follows reviewed course/module/source relationships | Intentional context expansion |

## Fair comparison

For each golden question, the evaluator runs:

1. hybrid retrieval (vector + keyword + reciprocal-rank fusion), and
2. the same retrieval with bounded deterministic graph expansion.

It records source hit rate, citation correctness, and whether added graph context was useful. A graph step stays only if it improves or preserves these metrics.
