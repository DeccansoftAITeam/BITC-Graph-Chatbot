"""Application settings loaded from the local, ignored .env file."""

from __future__ import annotations

from dataclasses import dataclass
from os import getenv

from dotenv import load_dotenv


@dataclass(frozen=True)
class DatabaseSettings:
    host: str
    port: int
    database: str
    user: str
    password: str
    sslmode: str

    @property
    def connection_kwargs(self) -> dict[str, str | int]:
        return {"host": self.host, "port": self.port, "dbname": self.database,
                "user": self.user, "password": self.password, "sslmode": self.sslmode}


@dataclass(frozen=True)
class AzureOpenAISettings:
    endpoint: str
    api_key: str
    embedding_deployment: str
    embedding_endpoint: str
    embedding_api_version: str
    chat_deployment: str
    api_version: str


@dataclass(frozen=True)
class ContentSafetySettings:
    endpoint: str
    api_key: str
    max_allowed_severity: int


@dataclass(frozen=True)
class BlobStorageSettings:
    connection_string: str
    container: str


def database_settings() -> DatabaseSettings:
    load_dotenv(override=True)
    values = {key: getenv(f"POSTGRES_{key}") for key in ("HOST", "PORT", "DB", "USER", "PASSWORD", "SSLMODE")}
    missing = [key for key, value in values.items() if not value]
    if missing:
        raise RuntimeError(f"Missing .env settings: {', '.join('POSTGRES_' + key for key in missing)}")
    return DatabaseSettings(host=str(values["HOST"]), port=int(str(values["PORT"])),
                            database=str(values["DB"]), user=str(values["USER"]),
                            password=str(values["PASSWORD"]), sslmode=str(values["SSLMODE"]))


def azure_openai_settings() -> AzureOpenAISettings:
    load_dotenv(override=True)
    keys = ("ENDPOINT", "API_KEY", "EMBEDDING_DEPLOYMENT", "CHAT_DEPLOYMENT")
    values = {key: getenv(f"AZURE_OPENAI_{key}") for key in keys}
    missing = [key for key, value in values.items() if not value]
    if missing:
        raise RuntimeError(f"Missing .env settings: {', '.join('AZURE_OPENAI_' + key for key in missing)}")
    endpoint = str(values["ENDPOINT"])
    embedding_endpoint = getenv("AZURE_OPENAI_EMBEDDING_ENDPOINT") or endpoint.replace(".openai.azure.com", ".cognitiveservices.azure.com")
    return AzureOpenAISettings(endpoint=endpoint, api_key=str(values["API_KEY"]),
                               embedding_deployment=str(values["EMBEDDING_DEPLOYMENT"]), embedding_endpoint=embedding_endpoint,
                               embedding_api_version=getenv("AZURE_OPENAI_EMBEDDING_API_VERSION", "2024-12-01-preview"),
                               chat_deployment=str(values["CHAT_DEPLOYMENT"]),
                               api_version=getenv("AZURE_OPENAI_API_VERSION", "2024-10-21"))


def content_safety_settings() -> ContentSafetySettings:
    load_dotenv(override=True)
    endpoint, key = getenv("CONTENT_SAFETY_ENDPOINT"), getenv("CONTENT_SAFETY_KEY")
    if not endpoint or not key:
        raise RuntimeError("Missing .env settings: CONTENT_SAFETY_ENDPOINT, CONTENT_SAFETY_KEY")
    return ContentSafetySettings(endpoint, key, int(getenv("CONTENT_SAFETY_MAX_ALLOWED_SEVERITY", "2")))


def blob_storage_settings() -> BlobStorageSettings:
    load_dotenv(override=True)
    connection_string = getenv("AZURE_STORAGE_CONNECTION_STRING")
    container = getenv("AZURE_STORAGE_CONTAINER", "bestitcourses-content")
    if not connection_string:
        raise RuntimeError("Missing .env setting: AZURE_STORAGE_CONNECTION_STRING")
    return BlobStorageSettings(connection_string, container)
