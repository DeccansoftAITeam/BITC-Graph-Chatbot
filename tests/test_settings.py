from course_knowledge.settings import AzureOpenAISettings, DatabaseSettings


def test_connection_parameters_are_named_and_complete() -> None:
    settings = DatabaseSettings("host", 5432, "coursesdb", "user", "secret", "require")

    assert settings.connection_kwargs == {
        "host": "host", "port": 5432, "dbname": "coursesdb", "user": "user",
        "password": "secret", "sslmode": "require",
    }


def test_azure_settings_keep_chat_and_embedding_endpoints_separate() -> None:
    settings = AzureOpenAISettings("https://chat.openai.azure.com", "key", "embedding", "https://embed.cognitiveservices.azure.com",
                                   "2024-12-01-preview", "chat", "2024-10-21")

    assert settings.embedding_endpoint.endswith("cognitiveservices.azure.com")
