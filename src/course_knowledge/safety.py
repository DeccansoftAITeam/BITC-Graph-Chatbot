"""Azure AI Content Safety input/output moderation gate."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions
from azure.core.credentials import AzureKeyCredential

from .settings import ContentSafetySettings


@dataclass(frozen=True)
class SafetyResult:
    allowed: bool
    severities: dict[str, int]


class SafetyApi(Protocol):
    def analyze_text(self, request: AnalyzeTextOptions): ...


class ContentSafetyGate:
    def __init__(self, client: SafetyApi, max_allowed_severity: int = 2):
        self.client = client
        self.max_allowed_severity = max_allowed_severity

    @classmethod
    def from_settings(cls, settings: ContentSafetySettings) -> "ContentSafetyGate":
        return cls(ContentSafetyClient(settings.endpoint, AzureKeyCredential(settings.api_key)), settings.max_allowed_severity)

    def assess(self, text: str) -> SafetyResult:
        response = self.client.analyze_text(AnalyzeTextOptions(text=text))
        severities = {str(item.category): int(item.severity or 0) for item in response.categories_analysis}
        return SafetyResult(all(value <= self.max_allowed_severity for value in severities.values()), severities)
