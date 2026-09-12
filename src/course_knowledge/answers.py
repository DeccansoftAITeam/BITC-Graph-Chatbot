"""Grounded answer generation over retrieved evidence only."""
from __future__ import annotations

from dataclasses import dataclass

from openai import OpenAI

from .graph_retrieval import GraphContext
from .retrieval import FusedCandidate
from .settings import AzureOpenAISettings


@dataclass(frozen=True)
class GroundedAnswer:
    text: str
    citations: tuple[str, ...]


def build_prompt(question: str, results: list[FusedCandidate], graph_context: dict[str, list[GraphContext]]) -> tuple[str, tuple[str, ...]]:
    sources: list[str] = []
    citations: list[str] = []
    for index, result in enumerate(results, start=1):
        metadata = result.candidate.metadata
        citation = f"{metadata['course_title']} | {metadata['module_title']} | {metadata['source']}"
        citations.append(citation)
        graph = "; ".join(f"{item.course} -> {item.module} -> {item.technology}" for item in graph_context.get(metadata["source_id"], []))
        sources.append(f"[{index}] {citation}\nEvidence: {result.candidate.text}\nGraph context: {graph or 'None'}")
    prompt = f"""You are the course knowledge teaching assistant. Answer only from the supplied evidence.
If the evidence is insufficient, say so plainly. Cite factual claims using [1], [2], etc.
Graph context is structural curriculum context; do not treat it as factual teaching content unless supported by Evidence.

Question: {question}

Sources:
{chr(10).join(sources)}
"""
    return prompt, tuple(citations)


class GroundedAnswerer:
    def __init__(self, settings: AzureOpenAISettings):
        self.settings = settings
        self.client = OpenAI(api_key=settings.api_key, base_url=settings.endpoint.rstrip("/") + "/openai/v1/")

    def answer(self, question: str, results: list[FusedCandidate], graph_context: dict[str, list[GraphContext]]) -> GroundedAnswer:
        prompt, citations = build_prompt(question, results, graph_context)
        response = self.client.responses.create(model=self.settings.chat_deployment, input=prompt, max_output_tokens=1200)
        return GroundedAnswer(response.output_text.strip(), citations)
