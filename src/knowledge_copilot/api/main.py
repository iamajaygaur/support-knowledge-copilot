from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from knowledge_copilot.config import get_settings
from knowledge_copilot.ingest.pipeline import ingest_documents
from knowledge_copilot.models import AskRequest, AskResponse
from knowledge_copilot.service import ask

app = FastAPI(
    title="Support Knowledge Copilot",
    description="Hybrid RAG assistant with verified citations",
    version="0.1.0",
)


class IngestRequest(BaseModel):
    source: str | None = None
    rebuild: bool = True
    strategy: str = Field(default="heading", pattern="^(heading|fixed)$")


@app.get("/health")
def health() -> dict:
    settings = get_settings()
    return {
        "status": "ok",
        "qdrant_mode": "local" if settings.qdrant_path else "server",
        "qdrant_path": str(settings.qdrant_path) if settings.qdrant_path else None,
        "qdrant_url": settings.qdrant_url,
        "collection": settings.qdrant_collection,
    }


@app.post("/ask", response_model=AskResponse)
def ask_endpoint(payload: AskRequest) -> AskResponse:
    try:
        return ask(
            payload.question,
            strategy=payload.strategy,
            use_rerank=payload.use_rerank,
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/ingest")
def ingest_endpoint(payload: IngestRequest) -> dict:
    settings = get_settings()
    source = payload.source or str(settings.docs_dir)
    try:
        chunks = ingest_documents(source, rebuild=payload.rebuild, strategy=payload.strategy)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return {"chunks_indexed": len(chunks), "source": source, "rebuild": payload.rebuild}
