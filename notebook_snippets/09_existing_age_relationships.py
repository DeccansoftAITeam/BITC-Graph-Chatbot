# %% List actual relationship types in the current AGE graph.
from course_knowledge.database import connect
from course_knowledge.settings import database_settings

with connect(database_settings()) as database, database.cursor() as cursor:
    cursor.execute('SET search_path = ag_catalog, "$user", public')
    cursor.execute("SELECT * FROM cypher('course_graph', $$ MATCH ()-[r]->() RETURN DISTINCT label(r) $$) AS (relationship agtype)")
    print(cursor.fetchall())
