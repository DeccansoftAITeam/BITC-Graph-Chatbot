"""Safe pre-session check: prints no secrets."""
from course_knowledge.database import connect
from course_knowledge.embeddings import AzureOpenAIEmbedder
from course_knowledge.settings import azure_openai_settings, database_settings

azure = azure_openai_settings()
with connect(database_settings()) as connection, connection.cursor() as cursor:
    cursor.execute("SELECT count(*) AS courses FROM courses")
    courses = cursor.fetchone()["courses"]
    cursor.execute("SELECT count(*) AS chunks, count(embedding) AS embeddings FROM chunks")
    chunks = cursor.fetchone()
print({"courses": courses, **chunks, "embedding_deployment": azure.embedding_deployment})
print({"embedding_dimensions": len(AzureOpenAIEmbedder.from_settings(azure).embed(["workshop health check"])[0])})
