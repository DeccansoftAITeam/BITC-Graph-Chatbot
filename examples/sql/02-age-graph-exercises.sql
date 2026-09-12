SET search_path = ag_catalog, "$user", public;
SELECT * FROM cypher('course_graph', $$ MATCH (n) RETURN n $$) AS (node agtype);
SELECT * FROM cypher('course_graph', $$ MATCH (a)-[r]->(b) RETURN a,r,b LIMIT 20 $$) AS (source agtype, relation agtype, target agtype);
