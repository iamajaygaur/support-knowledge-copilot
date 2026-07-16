# Support Knowledge Copilot

A support knowledge assistant that answers questions from internal documentation using **hybrid retrieval** (dense + BM25), generates **grounded answers with citations**, and **verifies** that each citation supports its claim.

Uses **Google AI Studio** (`gemini-flash-latest` + `gemini-embedding-001`) by default.

Built as a portfolio project for interviews on RAG systems, retrieval evaluation, and citation reliability.

## Features

- Document ingestion for Markdown, HTML, TXT, and PDF
- Heading-based and fixed-size chunking
- Shared chunk IDs across **Qdrant** (dense) and **BM25** (sparse)
- Reciprocal Rank Fusion + optional LLM reranking
- Grounded generation with `[chunk_id]` citations
- Post-generation citation verification and confidence scoring
- Graceful no-answer handling with closest sections
- Golden-set evaluation (`eval.py`) and Streamlit dashboard

## Quick start

### 1. Prerequisites

- Python 3.11+
- A Google AI Studio API key ([get one here](https://aistudio.google.com/apikey))
- Docker (optional — only if you prefer server-mode Qdrant)

### 2. Setup

```bash
cd support-knowledge-copilot
python3.12 -m venv .venv   # or python3.13+
source .venv/bin/activate
pip install -e ".[dev]"

cp .env.example .env
# edit .env and set GOOGLE_API_KEY
```

By default the app uses **embedded Qdrant** at `data/qdrant` (no Docker required).

### 3. Optional: Qdrant via Docker

```bash
# in .env: set QDRANT_PATH= (empty) to use the server URL
docker compose up -d
```

### 4. Ingest the sample corpus

```bash
python ingest.py --source docs/ --rebuild
```

Dense and sparse indexes are built over the **same chunk IDs**, so fusion and citation checks share one evidence identity. Semantic search handles paraphrase; BM25 catches exact tokens like `AUTH-4291`.

### 5. Ask questions

**CLI**

```bash
python ask.py "What does AUTH-4291 mean?"
python ask.py "What does AUTH-4291 mean?" --strategy dense --json
```

**API**

```bash
uvicorn knowledge_copilot.api.main:app --reload --app-dir src
```

```bash
curl -s http://127.0.0.1:8000/ask \
  -H 'Content-Type: application/json' \
  -d '{"question":"What does AUTH-4291 mean?","strategy":"hybrid"}' | jq
```

**Dashboard**

```bash
streamlit run streamlit_app.py
# or: make ui
```

The sidebar includes example questions and an optional **hybrid vs dense** comparison view.

> **Deploy note:** Vercel hosts the **FastAPI API** (`/ask`, `/health`), not the Streamlit UI. Run Streamlit locally for the dashboard.

### 6. Run evaluation

```bash
# Fast retrieval comparison (recommended for portfolio numbers)
python eval.py --strategy dense --no-rerank --retrieval-only
python eval.py --strategy hybrid --no-rerank --retrieval-only
python eval.py --strategy sparse --no-rerank --retrieval-only

# Full answer + citation eval (uses more Gemini quota)
python eval.py --strategy hybrid --no-rerank --limit 12
```

Reports are written to `reports/eval_*.md` (55 golden questions for retrieval).

### 7. Unit tests

```bash
pytest
# or: make test
```

## Response contract

```json
{
  "answer": "…",
  "citations": [
    {
      "chunk_id": "mfa-policy-001-…",
      "claim": "…",
      "verdict": "supported",
      "source_name": "MFA Policy"
    }
  ],
  "confidence": 0.86,
  "unverified": [],
  "no_answer": false,
  "confidence_breakdown": {
    "retrieval_score": 0.81,
    "citation_support_rate": 1.0,
    "answer_completeness": 1.0,
    "answered": 1.0
  }
}
```

## Architecture

```
Question
  → Dense (Qdrant) + Sparse (BM25)
  → Reciprocal Rank Fusion
  → LLM rerank (top 20 → top 5)
  → Grounded generation with [chunk_id] citations
  → Citation verification
  → Confidence score + unverified claims
```

## Project layout

```
docs/                         Sample support corpus
data/eval/golden_qa.jsonl     Hand-written eval questions
src/knowledge_copilot/        Library code
ingest.py                     CLI ingestion
eval.py                       CLI evaluation
streamlit_app.py              Streamlit UI
```

## Deploying on Vercel (API only)

Vercel deploys the FastAPI app from root **`app.py`** (which imports `knowledge_copilot.api.main:app`).

1. Push to GitHub and import the repo in Vercel (or Redeploy after the latest push)
2. Set environment variable **`GOOGLE_API_KEY`** in Vercel → Settings → Environment Variables
3. Open these URLs after deploy succeeds:
   - `/` — API info
   - `/health` — health check
   - `/docs` — interactive Swagger UI
   - `POST /ask` — ask questions

If you still see a generic Vercel **404: NOT_FOUND**, the deploy likely used an old commit — trigger **Redeploy** from the latest `main` (`c6055d9` or newer).
## Interview talking points

1. **Shared chunk IDs** — dense and sparse indexes address different failure modes but must point at the same evidence unit for fusion and citation checks.
2. **Hybrid + RRF** — keyword-heavy queries (error codes, SKUs) benefit from BM25; paraphrases benefit from embeddings.
3. **Citation verification** — generation can invent plausible citations; a second pass checks claim–chunk support.
4. **No-answer path** — low-evidence questions should refuse instead of hallucinating policy.
5. **Separate metrics** — retrieval quality, answer quality, citation validity, and refusal accuracy are measured independently.

## Case study results

Measured on the included 55-question golden set (retrieval-only, no rerank):

| Strategy | Correct source@5 | Recall@5 | MRR |
| --- | --- | --- | --- |
| Dense | **100%** | 97.1% | 0.975 |
| Hybrid (dense + BM25 + RRF) | **100%** | **98.5%** | 0.953 |
| Sparse (BM25 only) | 88.2% | 84.2% | 0.807 |

On a 12-question full answer eval (`hybrid`, no rerank):

- Citation support rate: **91.7%**
- Refusal accuracy on answerable questions: **100%**

**Interview takeaway:** On this corpus, Gemini embeddings already hit the right source often; hybrid still improves recall and covers BM25-only failure modes. Sparse alone is weakest (88.2% correct-source). Citation verification catches unsupported claims after generation.

See `reports/eval_dense_retrieval.md`, `reports/eval_hybrid_retrieval.md`, `reports/eval_sparse_retrieval.md`, and `reports/eval_hybrid.md`.

## Walkthrough

Use [`WALKTHROUGH.md`](WALKTHROUGH.md) for a 2–3 minute screen-recording script covering ingest, a verified citation answer, an outdated-doc trap, and a no-answer refusal.

## License

MIT
