#!/usr/bin/env python3
"""Streamlit dashboard for Support Knowledge Copilot."""

from __future__ import annotations

import os
import sys
from pathlib import Path

# Ensure `src/` is importable when the package isn't installed (e.g. Streamlit Cloud)
_SRC = Path(__file__).resolve().parent / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

import streamlit as st


def _apply_streamlit_secrets() -> None:
    """Copy Streamlit Cloud secrets into env for pydantic Settings / local .env parity."""
    try:
        secrets = st.secrets
    except Exception:  # noqa: BLE001 — no secrets.toml locally is fine
        return
    for key, value in secrets.items():
        if isinstance(value, dict):
            continue
        os.environ.setdefault(str(key), str(value))


_apply_streamlit_secrets()

from knowledge_copilot.models import AskResponse, CitationVerdict
from knowledge_copilot.service import ask

EXAMPLE_QUESTIONS = [
    ("AUTH-4291", "What does error AUTH-4291 mean and how do I fix it?"),
    ("MFA reset", "How do I reset MFA for a locked employee account?"),
    ("Token rotate", "When I rotate an API token, how long does the old token stay valid?"),
    ("Pet policy", "What is our pet-friendly vacation policy for bringing dogs to the office?"),
    ("HOOK-5008", "What does HOOK-5008 mean?"),
]

APP_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Figtree:wght@500;600;700&family=Source+Serif+4:opsz,wght@8..60,600;8..60,700&display=swap');

:root {
  --ink: #14212b;
  --muted: #5b6b76;
  --line: #d7e0e6;
  --paper: #f3f6f4;
  --card: #ffffff;
  --accent: #0f766e;
  --accent-soft: #d9f2ee;
  --warn: #b45309;
  --danger: #b91c1c;
  --ok: #047857;
}

html, body, [class*="css"] {
  font-family: "Figtree", sans-serif;
}

.stApp {
  background:
    radial-gradient(1200px 480px at 8% -10%, #d9f2ee 0%, transparent 55%),
    radial-gradient(900px 420px at 100% 0%, #e8eef3 0%, transparent 50%),
    linear-gradient(180deg, #eef3f1 0%, var(--paper) 28%, #e9eef1 100%);
}

[data-testid="stHeader"] {
  background: transparent;
}

[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #f7faf9 0%, #eef3f1 100%);
  border-right: 1px solid var(--line);
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
  font-family: "Figtree", sans-serif !important;
  letter-spacing: -0.02em;
}

.skc-hero {
  position: relative;
  overflow: hidden;
  border: 1px solid var(--line);
  border-radius: 22px;
  background:
    linear-gradient(135deg, rgba(255,255,255,0.92) 0%, rgba(255,255,255,0.78) 100%);
  box-shadow: 0 18px 40px rgba(20, 33, 43, 0.06);
  padding: 1.35rem 1.5rem 1.2rem;
  margin-bottom: 1.1rem;
}

.skc-hero::before {
  content: "";
  position: absolute;
  inset: 0 auto 0 0;
  width: 6px;
  background: linear-gradient(180deg, #0f766e, #1d4e89);
}

.skc-top {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 1rem;
  flex-wrap: wrap;
}

.skc-brand {
  display: flex;
  gap: 0.95rem;
  align-items: center;
  min-width: 0;
}

.skc-mark {
  width: 52px;
  height: 52px;
  border-radius: 16px;
  display: grid;
  place-items: center;
  color: white;
  font-family: "Source Serif 4", serif;
  font-weight: 700;
  font-size: 1.15rem;
  letter-spacing: -0.04em;
  background: linear-gradient(145deg, #0f766e 0%, #155e75 55%, #1d4e89 100%);
  box-shadow: 0 10px 22px rgba(15, 118, 110, 0.28);
  flex: 0 0 auto;
}

.skc-kicker {
  margin: 0;
  color: var(--accent);
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.14em;
  text-transform: uppercase;
}

.skc-title {
  margin: 0.15rem 0 0.2rem;
  color: var(--ink);
  font-family: "Source Serif 4", serif;
  font-size: clamp(1.55rem, 2.4vw, 2.05rem);
  font-weight: 700;
  letter-spacing: -0.03em;
  line-height: 1.15;
}

.skc-subtitle {
  margin: 0;
  color: var(--muted);
  font-size: 0.98rem;
  line-height: 1.45;
  max-width: 42rem;
}

.skc-status {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.45rem;
}

.skc-live {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  border: 1px solid #b7e4dc;
  background: var(--accent-soft);
  color: var(--accent);
  border-radius: 999px;
  padding: 0.28rem 0.7rem;
  font-size: 0.78rem;
  font-weight: 700;
}

.skc-live-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #10b981;
  box-shadow: 0 0 0 4px rgba(16, 185, 129, 0.18);
}

.skc-meta {
  color: var(--muted);
  font-size: 0.78rem;
  font-weight: 600;
}

.skc-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 1rem;
}

.skc-chip {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  border: 1px solid var(--line);
  background: rgba(255,255,255,0.9);
  color: var(--ink);
  border-radius: 999px;
  padding: 0.38rem 0.75rem;
  font-size: 0.8rem;
  font-weight: 600;
}

.skc-chip span {
  color: var(--accent);
  font-weight: 700;
}

.skc-panel {
  border: 1px solid var(--line);
  border-radius: 18px;
  background: rgba(255,255,255,0.88);
  padding: 1rem 1.1rem 0.85rem;
  margin-bottom: 0.85rem;
  box-shadow: 0 10px 28px rgba(20, 33, 43, 0.04);
}

.skc-panel h3 {
  margin: 0 0 0.35rem;
  color: var(--ink);
  font-size: 1.02rem;
  font-weight: 700;
}

.skc-panel p {
  margin: 0 0 0.75rem;
  color: var(--muted);
  font-size: 0.9rem;
}

.skc-side-card {
  border: 1px solid var(--line);
  border-radius: 14px;
  background: rgba(255,255,255,0.75);
  padding: 0.8rem 0.9rem;
  margin-bottom: 0.85rem;
}

.skc-side-card strong {
  display: block;
  color: var(--ink);
  font-size: 0.86rem;
  margin-bottom: 0.25rem;
}

.skc-side-card span {
  color: var(--muted);
  font-size: 0.78rem;
  line-height: 1.4;
}

div[data-testid="stMetric"] {
  background: #fff;
  border: 1px solid var(--line);
  border-radius: 14px;
  padding: 0.65rem 0.8rem;
}

.stButton > button[kind="primary"] {
  background: linear-gradient(135deg, #0f766e, #155e75) !important;
  border: none !important;
  box-shadow: 0 8px 18px rgba(15, 118, 110, 0.25);
}

.stTabs [data-baseweb="tab-list"] {
  gap: 0.35rem;
}

.stTabs [data-baseweb="tab"] {
  border-radius: 999px;
  background: rgba(255,255,255,0.7);
  border: 1px solid var(--line);
  padding: 0.35rem 0.9rem;
}

.stTabs [aria-selected="true"] {
  background: var(--accent-soft) !important;
  border-color: #9ad9cf !important;
  color: var(--accent) !important;
}
</style>
"""


def render_header(*, strategy: str, use_rerank: bool, compare: bool) -> None:
    mode = "Compare hybrid vs dense" if compare else f"{strategy.title()} retrieval"
    rerank = "Rerank on" if use_rerank else "Rerank off"
    st.markdown(
        f"""
        <div class="skc-hero">
          <div class="skc-top">
            <div class="skc-brand">
              <div class="skc-mark">SK</div>
              <div>
                <p class="skc-kicker">Internal support RAG</p>
                <h1 class="skc-title">Support Knowledge Copilot</h1>
                <p class="skc-subtitle">
                  Hybrid retrieval over internal docs, then citation checks so every claim
                  points back to a real source section.
                </p>
              </div>
            </div>
            <div class="skc-status">
              <div class="skc-live"><span class="skc-live-dot"></span> Ready</div>
              <div class="skc-meta">{mode} · {rerank}</div>
            </div>
          </div>
          <div class="skc-chips">
            <div class="skc-chip"><span>●</span> Dense + BM25 fusion</div>
            <div class="skc-chip"><span>●</span> Grounded generation</div>
            <div class="skc-chip"><span>●</span> Citation verification</div>
            <div class="skc-chip"><span>●</span> No-answer guardrails</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_response(response: AskResponse) -> None:
    supported = sum(1 for c in response.citations if c.verdict == CitationVerdict.SUPPORTED)
    partial = sum(1 for c in response.citations if c.verdict == CitationVerdict.PARTIAL)
    unsupported = sum(1 for c in response.citations if c.verdict == CitationVerdict.NOT_SUPPORTED)
    sources = sorted({item.chunk.source_name for item in response.retrieval.chunks})

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Confidence", f"{response.confidence:.0%}")
    m2.metric("Citations", f"{supported} supported")
    m3.metric("Flags", f"{partial + unsupported}")
    m4.metric("Sources hit", str(len(sources)))

    tab_answer, tab_citations, tab_evidence, tab_debug = st.tabs(
        ["Answer", "Citations", "Evidence", "Confidence"]
    )

    with tab_answer:
        if response.no_answer:
            st.warning(response.answer)
        else:
            st.markdown(response.answer)

        st.markdown("##### Verification notes")
        if response.unverified:
            for item in response.unverified:
                st.markdown(f"- {item}")
        else:
            st.success("All surfaced claims passed verification checks.")

    with tab_citations:
        if not response.citations:
            st.info("No citations to verify for this response.")
        for citation in response.citations:
            color = {
                CitationVerdict.SUPPORTED: "green",
                CitationVerdict.PARTIAL: "orange",
                CitationVerdict.NOT_SUPPORTED: "red",
            }[citation.verdict]
            st.markdown(
                f":{color}[**{citation.verdict.value.replace('_', ' ').title()}**] "
                f"`{citation.chunk_id}` — {citation.source_name} › {citation.section_heading}"
            )
            st.caption(citation.claim)
            if citation.rationale:
                st.caption(f"Reason: {citation.rationale}")
            st.divider()

    with tab_evidence:
        if not response.retrieval.chunks:
            st.info("No chunks retrieved.")
        for item in response.retrieval.chunks:
            with st.expander(
                f"{item.chunk.source_name} › {item.chunk.section_heading} · "
                f"score {item.score:.3f} · {', '.join(item.sources)}",
                expanded=False,
            ):
                st.caption(
                    f"`{item.chunk.chunk_id}` · updated {item.chunk.last_updated or 'unknown'} · "
                    f"{item.chunk.doc_type.value}"
                )
                st.write(item.chunk.text)

    with tab_debug:
        st.json(response.confidence_breakdown)
        if sources:
            st.caption("Docs used: " + ", ".join(sources))


st.set_page_config(
    page_title="Support Knowledge Copilot",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(APP_CSS, unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### Workspace")
    st.markdown(
        """
        <div class="skc-side-card">
          <strong>Retrieval lab</strong>
          <span>Tune strategy, compare dense vs hybrid, and keep rerank off on free-tier keys.</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    strategy = st.selectbox(
        "Retrieval strategy",
        ["hybrid", "dense", "sparse"],
        index=0,
        help="Hybrid fuses dense embeddings with BM25 for error codes and exact tokens.",
    )
    use_rerank = st.checkbox(
        "LLM rerank",
        value=False,
        help="Uses an extra model call to reorder the top candidates.",
    )
    compare_strategies = st.checkbox(
        "Compare hybrid vs dense",
        value=False,
        help="Runs both strategies side-by-side for the same question.",
    )

    st.markdown("### Try a scenario")
    for label, example in EXAMPLE_QUESTIONS:
        if st.button(label, key=f"ex-{label}", use_container_width=True):
            st.session_state["question"] = example
            st.session_state["autofill_note"] = example

    if st.session_state.get("autofill_note"):
        st.caption(f"Loaded: {st.session_state['autofill_note']}")

    st.markdown("---")
    st.markdown(
        """
        <div class="skc-side-card">
          <strong>How answers are built</strong>
          <span>Retrieve → generate with [chunk_id] citations → verify each claim → score confidence.</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

render_header(strategy=strategy, use_rerank=use_rerank, compare=compare_strategies)

st.markdown(
    """
    <div class="skc-panel">
      <h3>Ask a support question</h3>
      <p>Answers stay grounded in the sample corpus (auth, MFA, webhooks, policies). Out-of-scope topics should refuse.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

question = st.text_input(
    "Support question",
    value=st.session_state.get("question", ""),
    placeholder="e.g. What does HOOK-5008 mean and how should the customer fix it?",
    label_visibility="collapsed",
)
ask_col, tip_col = st.columns([1, 2.4])
with ask_col:
    run = st.button("Ask Copilot", type="primary", use_container_width=True)
with tip_col:
    st.caption(
        "Tip: start with an error code or policy question. Use Compare mode to show dense vs hybrid live."
    )

if run and question.strip():
    with st.spinner("Retrieving evidence, drafting an answer, and verifying citations…"):
        try:
            if compare_strategies:
                hybrid = ask(question.strip(), strategy="hybrid", use_rerank=use_rerank)
                dense = ask(question.strip(), strategy="dense", use_rerank=use_rerank)
            else:
                response = ask(question.strip(), strategy=strategy, use_rerank=use_rerank)
        except Exception as exc:  # noqa: BLE001
            msg = str(exc)
            if "503" in msg or "high demand" in msg.lower() or "UNAVAILABLE" in msg:
                st.warning(
                    "Google’s model is temporarily overloaded (503). "
                    "Wait ~20–30 seconds and click Ask again. "
                    "Retries are built in now — also try with **LLM rerank** unchecked."
                )
            elif "429" in msg or "RESOURCE_EXHAUSTED" in msg:
                st.warning(
                    "Google API quota/rate limit hit. Wait a bit, uncheck **LLM rerank**, "
                    "or try again in a minute."
                )
            else:
                st.error(msg)
            st.stop()

    if compare_strategies:
        left, right = st.columns(2)
        with left:
            st.markdown("### Hybrid")
            render_response(hybrid)
        with right:
            st.markdown("### Dense")
            render_response(dense)
    else:
        render_response(response)
elif run:
    st.warning("Enter a question first.")
