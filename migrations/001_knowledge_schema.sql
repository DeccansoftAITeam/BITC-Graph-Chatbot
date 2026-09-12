-- Canonical relational source of truth. Apache AGE is a read-only graph projection.
CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS age CASCADE;
CREATE EXTENSION IF NOT EXISTS azure_ai;

CREATE TABLE courses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    course_key TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT NOT NULL CHECK (status IN ('draft', 'published', 'archived')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE course_versions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    course_id UUID NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
    version_label TEXT NOT NULL,
    is_latest BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (course_id, version_label)
);
CREATE UNIQUE INDEX IF NOT EXISTS one_latest_course_version ON course_versions(course_id) WHERE is_latest;

CREATE TABLE modules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    course_version_id UUID NOT NULL REFERENCES course_versions(id) ON DELETE CASCADE,
    module_key TEXT NOT NULL,
    title TEXT NOT NULL,
    ordinal NUMERIC(8,3) NOT NULL CHECK (ordinal > 0),
    learning_objectives JSONB NOT NULL DEFAULT '[]'::jsonb,
    UNIQUE (course_version_id, module_key),
    UNIQUE (course_version_id, ordinal)
);

-- One row per unique raw asset, regardless of how many courses reference it.
CREATE TABLE sources (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content_sha256 CHAR(64) NOT NULL UNIQUE,
    source_type TEXT NOT NULL CHECK (source_type IN ('markdown', 'pdf', 'docx', 'transcript', 'video', 'readme', 'other')),
    media_type TEXT,
    canonical_filename TEXT NOT NULL,
    byte_size BIGINT NOT NULL CHECK (byte_size >= 0),
    storage_uri TEXT,
    extraction_status TEXT NOT NULL DEFAULT 'pending' CHECK (extraction_status IN ('pending', 'extracted', 'failed')),
    extracted_text TEXT,
    extracted_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- A source's teaching placement; preserving its on-disk path aids auditability.
CREATE TABLE module_sources (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    module_id UUID NOT NULL REFERENCES modules(id) ON DELETE CASCADE,
    source_id UUID NOT NULL REFERENCES sources(id) ON DELETE RESTRICT,
    source_path TEXT NOT NULL,
    display_title TEXT,
    ordinal INTEGER NOT NULL DEFAULT 1,
    UNIQUE (module_id, source_id, source_path)
);
CREATE INDEX IF NOT EXISTS module_sources_source_id_idx ON module_sources(source_id);

CREATE TABLE source_sections (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_id UUID NOT NULL REFERENCES sources(id) ON DELETE CASCADE,
    parent_section_key TEXT NOT NULL,
    heading_path TEXT NOT NULL,
    ordinal INTEGER NOT NULL,
    text_content TEXT NOT NULL,
    token_count INTEGER,
    UNIQUE (source_id, parent_section_key)
);
CREATE INDEX IF NOT EXISTS source_sections_source_id_idx ON source_sections(source_id);

-- Embedding-bearing children; identical normalized text creates a single chunk.
CREATE TABLE chunks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    normalized_text_sha256 CHAR(64) NOT NULL UNIQUE,
    chunker_version TEXT NOT NULL,
    text_content TEXT NOT NULL,
    token_count INTEGER NOT NULL,
    search_vector TSVECTOR GENERATED ALWAYS AS (to_tsvector('english', text_content)) STORED,
    embedding vector,
    embedding_model TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS chunks_search_vector_idx ON chunks USING GIN (search_vector);

CREATE TABLE section_chunks (
    section_id UUID NOT NULL REFERENCES source_sections(id) ON DELETE CASCADE,
    chunk_id UUID NOT NULL REFERENCES chunks(id) ON DELETE RESTRICT,
    ordinal INTEGER NOT NULL,
    PRIMARY KEY (section_id, chunk_id),
    UNIQUE (section_id, ordinal)
);
CREATE INDEX IF NOT EXISTS section_chunks_chunk_id_idx ON section_chunks(chunk_id);

CREATE TABLE technologies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    normalized_name TEXT NOT NULL UNIQUE,
    display_name TEXT NOT NULL
);
CREATE TABLE course_technologies (
    course_id UUID NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
    technology_id UUID NOT NULL REFERENCES technologies(id) ON DELETE CASCADE,
    PRIMARY KEY (course_id, technology_id)
);
CREATE TABLE module_prerequisites (
    module_id UUID NOT NULL REFERENCES modules(id) ON DELETE CASCADE,
    prerequisite_module_id UUID NOT NULL REFERENCES modules(id) ON DELETE CASCADE,
    PRIMARY KEY (module_id, prerequisite_module_id),
    CHECK (module_id <> prerequisite_module_id)
);

-- Every non-hierarchical relation must disclose where the deterministic fact came from.
CREATE TABLE source_relationships (
    source_id UUID NOT NULL REFERENCES sources(id) ON DELETE CASCADE,
    related_source_id UUID NOT NULL REFERENCES sources(id) ON DELETE CASCADE,
    relationship_type TEXT NOT NULL CHECK (relationship_type IN ('duplicate_of', 'related_to')),
    evidence TEXT NOT NULL,
    PRIMARY KEY (source_id, related_source_id, relationship_type),
    CHECK (source_id <> related_source_id)
);
