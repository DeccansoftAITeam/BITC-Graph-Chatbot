# %% Create embeddings directly with the Azure OpenAI deployment.
from course_knowledge.embeddings import AzureOpenAIEmbedder
from course_knowledge.settings import azure_openai_settings

phrases = ["Model Context Protocol", "GitHub Copilot", "A tropical fruit"]
vectors = AzureOpenAIEmbedder.from_settings(azure_openai_settings()).embed(phrases)
print({"phrases": phrases, "embedding_dimensions": len(vectors[0])})
