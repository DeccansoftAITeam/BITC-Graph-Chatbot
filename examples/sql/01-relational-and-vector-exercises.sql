-- 1. Blob-backed source documents
SELECT canonical_filename, source_type, storage_uri FROM sources ORDER BY canonical_filename;

-- 2. Chunks and embedding state
SELECT count(*) AS chunks, count(embedding) AS embedded_chunks FROM chunks;

-- 3. Full-text search; replace the question
SELECT text_content FROM chunks
WHERE search_vector @@ websearch_to_tsquery('english', 'model context protocol') LIMIT 5;
