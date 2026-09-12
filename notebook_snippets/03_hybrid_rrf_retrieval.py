# %% Compare RRF hybrid retrieval results.
from course_knowledge.database import connect
from course_knowledge.embeddings import AzureOpenAIEmbedder
from course_knowledge.hybrid import HybridRetriever
from course_knowledge.settings import azure_openai_settings, database_settings

with connect(database_settings()) as database:
    retriever = HybridRetriever(database, AzureOpenAIEmbedder.from_settings(azure_openai_settings()))
    for hit in retriever.search("How does Model Context Protocol work?", 5):
        print(hit.matched_legs, hit.candidate.metadata["source"])
