from __future__ import annotations

from datetime import date
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class DocType(str, Enum):
    FAQ = "faq"
    TROUBLESHOOTING = "troubleshooting"
    ONBOARDING = "onboarding"
    API = "api"
    RELEASE_NOTES = "release_notes"
    POLICY = "policy"
    OTHER = "other"


class AccessLevel(str, Enum):
    PUBLIC = "public"
    INTERNAL = "internal"
    RESTRICTED = "restricted"


class Chunk(BaseModel):
    chunk_id: str
    text: str
    source_name: str
    source_path: str
    section_heading: str = ""
    last_updated: date | None = None
    doc_type: DocType = DocType.OTHER
    access_level: AccessLevel = AccessLevel.INTERNAL
    page_number: int | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class RetrievedChunk(BaseModel):
    chunk: Chunk
    score: float
    sources: list[str] = Field(default_factory=list)  # e.g. ["dense", "sparse"]


class CitationVerdict(str, Enum):
    SUPPORTED = "supported"
    NOT_SUPPORTED = "not_supported"
    PARTIAL = "partial"


class Citation(BaseModel):
    chunk_id: str
    claim: str
    source_name: str = ""
    section_heading: str = ""
    verdict: CitationVerdict = CitationVerdict.SUPPORTED
    rationale: str = ""


class RetrievalInfo(BaseModel):
    strategy: str
    chunks: list[RetrievedChunk]


class AskRequest(BaseModel):
    question: str
    strategy: str = "hybrid"  # dense | sparse | hybrid
    use_rerank: bool = True


class AskResponse(BaseModel):
    answer: str
    citations: list[Citation]
    confidence: float
    unverified: list[str]
    retrieval: RetrievalInfo
    no_answer: bool = False
    confidence_breakdown: dict[str, float] = Field(default_factory=dict)
    closest_sections: list[dict[str, str]] = Field(default_factory=list)
