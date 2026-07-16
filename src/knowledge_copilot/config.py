from functools import lru_cache
from pathlib import Path
from typing import Any

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(PROJECT_ROOT / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    google_api_key: str = ""
    # Prefer local embedded Qdrant when qdrant_path is set (default).
    # Set qdrant_path empty and qdrant_url to use a Docker/server instance.
    qdrant_path: Path | None = PROJECT_ROOT / "data" / "qdrant"
    qdrant_url: str = "http://localhost:6333"
    qdrant_collection: str = "support_chunks"
    embedding_model: str = "gemini-embedding-001"
    llm_model: str = "gemini-flash-latest"
    bm25_path: Path = PROJECT_ROOT / "data" / "bm25" / "index.pkl"

    @field_validator("qdrant_path", mode="before")
    @classmethod
    def _empty_qdrant_path(cls, value: Any) -> Any:
        if value is None or value == "" or str(value).lower() in {"none", "null"}:
            return None
        return value

    @field_validator("qdrant_path", "bm25_path", mode="after")
    @classmethod
    def _resolve_paths(cls, value: Path | None) -> Path | None:
        if value is None:
            return None
        path = Path(value)
        if not path.is_absolute():
            path = PROJECT_ROOT / path
        return path

    dense_k: int = 10
    sparse_k: int = 10
    rrf_k: int = 60
    rerank_pool: int = 20
    final_k: int = 5
    retrieval_confidence_threshold: float = 0.25

    # gemini-embedding-001 supports matryoshka dims; 768 is a good local default
    embedding_dim: int = 768

    docs_dir: Path = PROJECT_ROOT / "docs"
    reports_dir: Path = PROJECT_ROOT / "reports"
    golden_qa_path: Path = PROJECT_ROOT / "data" / "eval" / "golden_qa.jsonl"


@lru_cache
def get_settings() -> Settings:
    return Settings()
