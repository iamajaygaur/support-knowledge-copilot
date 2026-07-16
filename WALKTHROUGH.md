# Walkthrough Script (2–3 minutes)

Use this while screen-recording for your portfolio.

## Before recording

```bash
cd ~/support-knowledge-copilot
source .venv/bin/activate
python ingest.py --source docs/ --rebuild   # only if index is stale
streamlit run streamlit_app.py
```

In the UI:
- Strategy: **hybrid**
- **LLM rerank**: unchecked (faster / fewer API calls)

---

## Recording outline

### 1. Intro (15 sec)
> “This is a Support Knowledge Copilot. It uses hybrid retrieval — dense embeddings plus BM25 — then generates grounded answers and verifies every citation.”

Show the sidebar briefly (hybrid strategy, example questions).

### 2. Ingestion mention (10 sec)
> “Documents are chunked by heading, embedded with Gemini, and stored under the same chunk IDs in Qdrant and BM25 so fusion and citation checks share one evidence identity.”

Optional: flash the terminal with `python ingest.py --source docs/ --rebuild` already completed.

### 3. Good answer with verified citations (45–60 sec)
Click: **What does error AUTH-4291 mean and how do I fix it?**

Point out:
- Answer mentions 5 MFA attempts / 30-minute soft lock
- Citations include Authentication Error Codes + April 2026 release notes
- Citation verdicts are **supported**
- Confidence breakdown shows `citation_support_rate: 1`

### 4. Outdated-document trap (40 sec)
Ask: **When I rotate an API token, how long does the old token stay valid?**

Point out:
- Correct answer is **1-hour overlap** (April 2026 / current API docs)
- Older Dec 2025 notes said immediate invalidation — the assistant should prefer the newer guidance

### 5. No-answer case (30 sec)
Click: **What is our pet-friendly vacation policy for bringing dogs to the office?**

Point out:
- Explicit refusal / “not in the docs”
- Closest sections may appear, but it does **not** invent a policy
- This is the hallucination-control story for interviews

### 6. Close (15 sec)
> “Eval separately measures retrieval, citation support, and refusal accuracy. Hybrid helps most on exact tokens like error codes.”

Show `reports/eval_hybrid.md` summary if available.

---

## Backup CLI demos (if Streamlit is slow)

```bash
python ask.py "What does error AUTH-4291 mean and how do I fix it?" --no-rerank
python ask.py "When I rotate an API token, how long does the old token stay valid?" --no-rerank
python ask.py "What is our pet-friendly vacation policy for bringing dogs to the office?" --no-rerank
```
