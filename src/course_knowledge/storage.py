"""Original course assets belong in Azure Blob Storage, not PostgreSQL."""
from __future__ import annotations

from azure.storage.blob import BlobServiceClient, ContentSettings
from azure.core.exceptions import ResourceExistsError

from .settings import BlobStorageSettings


class BlobAssetStore:
    def __init__(self, settings: BlobStorageSettings):
        self.container = settings.container
        self.client = BlobServiceClient.from_connection_string(settings.connection_string)

    def upload(self, blob_name: str, content: bytes, content_type: str | None = None) -> str:
        container = self.client.get_container_client(self.container)
        try:
            container.create_container()
        except ResourceExistsError:
            pass
        blob = container.get_blob_client(blob_name)
        if not blob.exists():
            blob.upload_blob(content, overwrite=False, content_settings=ContentSettings(content_type=content_type))
        return blob.url
