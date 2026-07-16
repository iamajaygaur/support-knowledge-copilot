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
    "What does error AUTH-4291 mean and how do I fix it?",
    "How do I reset MFA for a locked employee account?",
    "When I rotate an API token, how long does the old token stay valid?",
    "What is our pet-friendly vacation policy for bringing dogs to the office?",
    "What does HOOK-5008 mean?",
]


def render_response(response: AskResponse) -> None:
    col_a, col_b = st.columns([1.2, 1])
    with col_a:
        st.subheader("Answer")
        if response.no_answer:
            st.warning(response.answer)
        else:
            st.write(response.answer)

        st.subheader("What I could not verify")
        if response.unverified:
            for item in response.unverified:
                st.markdown(f"- {item}")
        else:
            st.success("Nothing flagged.")

    with col_b:
        st.metric("Confidence", f"{response.confidence:.2f}")
        st.write("Confidence breakdown")
        st.json(response.confidence_breakdown)

        st.subheader("Citations")
        if not response.citations:
            st.info("No citations to verify.")
        for citation in response.citations:
            color = {
                CitationVerdict.SUPPORTED: "green",
                CitationVerdict.PARTIAL: "orange",
                CitationVerdict.NOT_SUPPORTED: "red",
            }[citation.verdict]
            st.markdown(
                f":{color}[**{citation.verdict.value}**] "
                f"`{citation.chunk_id}` — {citation.source_name} › {citation.section_heading}"
            )
            st.caption(citation.claim)
            if citation.rationale:
                st.caption(f"Reason: {citation.rationale}")

    st.subheader("Retrieved chunks")
    for item in response.retrieval.chunks:
        with st.expander(
            f"{item.chunk.chunk_id} · score={item.score:.4f} · sources={','.join(item.sources)}"
        ):
            st.markdown(
                f"**{item.chunk.source_name}** › {item.chunk.section_heading}  \n"
                f"Updated: {item.chunk.last_updated or 'unknown'} · "
                f"Type: {item.chunk.doc_type.value}"
            )
            st.write(item.chunk.text)


st.set_page_config(page_title="Support Knowledge Copilot", layout="wide")
st.title("Support Knowledge Copilot")
st.caption("Hybrid retrieval · grounded answers · verified citations")

with st.sidebar:
    st.header("Settings")
    strategy = st.selectbox("Retrieval strategy", ["hybrid", "dense", "sparse"], index=0)
    use_rerank = st.checkbox("LLM rerank", value=False)
    compare_strategies = st.checkbox("Compare hybrid vs dense", value=False)
    st.caption("Tip: leave rerank off on free-tier keys to use fewer API calls.")
    st.markdown("**Example questions**")
    for example in EXAMPLE_QUESTIONS:
        if st.button(example, key=f"ex-{example[:24]}"):
            st.session_state["question"] = example

question = st.text_input(
    "Support question",
    value=st.session_state.get("question", ""),
    placeholder="How do I reset MFA for a locked account?",
)
run = st.button("Ask", type="primary")

if run and question.strip():
    with st.spinner("Retrieving, generating, and verifying citations…"):
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
            st.metric("Confidence", f"{hybrid.confidence:.2f}")
            st.caption(
                "Sources: "
                + ", ".join(
                    sorted({item.chunk.source_name for item in hybrid.retrieval.chunks})
                )
            )
            render_response(hybrid)
        with right:
            st.markdown("### Dense")
            st.metric("Confidence", f"{dense.confidence:.2f}")
            st.caption(
                "Sources: "
                + ", ".join(
                    sorted({item.chunk.source_name for item in dense.retrieval.chunks})
                )
            )
            render_response(dense)
    else:
        render_response(response)
elif run:
    st.warning("Enter a question first.")
