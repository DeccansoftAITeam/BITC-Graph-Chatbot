# %% Verify the workshop environment.
from course_knowledge.database import connect
from course_knowledge.settings import azure_openai_settings, database_settings

with connect(database_settings()) as database, database.cursor() as cursor:
    cursor.execute("SELECT count(*) AS courses FROM courses")
    print(cursor.fetchone())
print({"embedding_deployment": azure_openai_settings().embedding_deployment})
