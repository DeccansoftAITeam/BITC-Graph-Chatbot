# Teaching Knowledge Model

## Why `sources` is first

A source is an immutable, content-addressed teaching asset: a Markdown file, PDF, transcript, video, or README. `sources` has one row per unique byte-level source hash. It has no course-specific columns because one source may be used by many courses or modules.

Course placement belongs in `module_sources`. This separation visibly demonstrates one GraphRAG advantage: one canonical asset can have multiple teaching contexts without duplicated extraction, embeddings, or ambiguous citations.

## Canonical model

```text
courses → course_versions → modules → module_sources → sources
                                                    ↓
                                          source_sections → chunks

courses/modules/sources ↔ technologies
modules ↔ modules (PREREQUISITE_OF)
sources ↔ sources (RELATED_TO; deterministic only)
```

- **Sources** preserve provenance and content hashes.
- **Sections** are parent contexts, split at source headings or transcript boundaries.
- **Chunks** are small searchable children. Their normalized text hash deduplicates embeddings across sections and sources.
- **Relationship tables** are the canonical deterministic graph. Apache AGE is populated from them for graph traversal demonstrations.

## What will be demonstrated

1. A vector-only query returns the closest chunks.
2. Hybrid retrieval adds exact keyword matches (for API names/error codes).
3. Graph-expanded retrieval follows known edges: source → module → course, technology → courses, or module prerequisites.
4. The evaluation records whether that expansion helps a real teaching query. Graph expansion is not presented as a universal improvement.

## Initial source observations

- There are two course roots and 42 supplied files (41 Markdown, one PDF).
- The two similarly named Model Context Protocol files in OpenAI courseware are not identical: one is materially longer. They remain separate source assets; repeated normalized child chunks can still deduplicate after chunking.
- Current folders imply a course/module structure, but lack explicit metadata such as learning objectives, prerequisites, and version history. The `catalog/*.yaml` descriptors provide the initial course-level facts; module objectives/prerequisites will be added as reviewed metadata rather than guessed by an LLM.
