# %% Inspect Blob-backed documents and run pgvector similarity search.
from course_knowledge.database import connect, vector_candidates
from course_knowledge.embeddings import AzureOpenAIEmbedder
from course_knowledge.settings import azure_openai_settings, database_settings

with connect(database_settings()) as database:
    vector = AzureOpenAIEmbedder.from_settings(azure_openai_settings()).embed(["What is MCP?"])[0]
    for result in vector_candidates(database, vector, 5):
        print(result["course_title"], result["canonical_filename"])
