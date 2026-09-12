"""Shared, model-agnostic retrieval ranking primitives for MCP and chatbot consumers."""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class RetrievalCandidate:
    chunk_id: str
    text: str
    metadata: dict[str, str]


@dataclass(frozen=True)
class FusedCandidate:
    candidate: RetrievalCandidate
    rrf_score: float
    matched_legs: tuple[str, ...]


def reciprocal_rank_fusion(legs: dict[str, Iterable[RetrievalCandidate]], constant: int = 60) -> list[FusedCandidate]:
    """Fuse independently ranked legs without relying on incomparable raw scores."""
    if constant < 1:
        raise ValueError("RRF constant must be positive")
    scores: dict[str, float] = defaultdict(float)
    candidates: dict[str, RetrievalCandidate] = {}
    matches: dict[str, list[str]] = defaultdict(list)
    for leg_name, ranked in legs.items():
        for rank, candidate in enumerate(ranked, start=1):
            scores[candidate.chunk_id] += 1 / (constant + rank)
            candidates[candidate.chunk_id] = candidate
            matches[candidate.chunk_id].append(leg_name)
    return sorted((FusedCandidate(candidates[key], score, tuple(matches[key])) for key, score in scores.items()),
                  key=lambda result: (-result.rrf_score, result.candidate.chunk_id))
