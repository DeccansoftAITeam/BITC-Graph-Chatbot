-- Run after canonical tables are populated. It never becomes the system of record.
SET search_path = ag_catalog, "$user", public;
SELECT create_graph('course_graph')
WHERE NOT EXISTS (SELECT 1 FROM ag_catalog.ag_graph WHERE name = 'course_graph');

-- The ingestion service creates idempotent AGE nodes/edges from courses, modules,
-- sources, technologies, and module_prerequisites. Cypher is intentionally bounded
-- to read-only traversal in the MCP API.
