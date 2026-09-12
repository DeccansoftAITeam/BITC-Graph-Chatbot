# %% Retrieve documents structurally through real Apache AGE edges.
from course_knowledge.database import connect
from course_knowledge.settings import database_settings

with connect(database_settings()) as database, database.cursor() as cursor:
    cursor.execute('SET search_path = ag_catalog, "$user", public')
    cursor.execute("SELECT * FROM cypher('course_graph', $$ MATCH (c:Course)-[:HAS_MODULE]->(m:Module)-[:HAS_SOURCE]->(s:Source) RETURN c.title,m.title,s.filename LIMIT 20 $$) AS (course agtype,module agtype,document agtype)")
    for row in cursor.fetchall(): print(row)
