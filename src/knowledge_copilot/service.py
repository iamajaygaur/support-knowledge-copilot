from __future__ import annotations

from knowledge_copilot.generate.answer import generate_answer
from knowledge_copilot.models import AskResponse, CitationVerdict, RetrievalInfo
from knowledge_copilot.retrieve.pipeline import retrieve
from knowledge_copilot.verify.citations import verify_citations
from knowledge_copilot.verify.confidence import score_confidence


def ask(
    question: str,
    *,
    strategy: str = "hybrid",
    use_rerank: bool = True,
) -> AskResponse:
    retrieved = retrieve(question, strategy=strategy, use_rerank=use_rerank)

    if not retrieved:
        return AskResponse(
            answer="I could not find this in the docs. No relevant sections were retrieved.",
            citations=[],
            confidence=0.05,
            unverified=["No retrieved context"],
            retrieval=RetrievalInfo(strategy=strategy, chunks=[]),
            no_answer=True,
            confidence_breakdown={
                "retrieval_score": 0.0,
                "citation_support_rate": 1.0,
                "answer_completeness": 0.5,
                "answered": 0.0,
            },
            closest_sections=[],
        )

    answer, unverified, no_answer = generate_answer(question, retrieved)
    citations = [] if no_answer else verify_citations(answer, retrieved)

    for citation in citations:
        if citation.verdict in {CitationVerdict.NOT_SUPPORTED, CitationVerdict.PARTIAL}:
            note = f"Citation [{citation.chunk_id}] is {citation.verdict.value}: {citation.claim}"
            if note not in unverified:
                unverified.append(note)

    confidence, breakdown = score_confidence(
        retrieved=retrieved,
        citations=citations,
        no_answer=no_answer,
        unverified=unverified,
    )

    closest = [
        {
            "chunk_id": item.chunk.chunk_id,
            "source_name": item.chunk.source_name,
            "section_heading": item.chunk.section_heading,
        }
        for item in retrieved
    ]

    if no_answer:
        answer = (
            "I could not find this in the docs with enough confidence.\n\n"
            f"{answer}\n\n"
            "Closest matching sections:\n"
            + "\n".join(
                f"- {c['source_name']} › {c['section_heading']} [{c['chunk_id']}]" for c in closest
            )
        )

    return AskResponse(
        answer=answer,
        citations=citations,
        confidence=confidence,
        unverified=unverified,
        retrieval=RetrievalInfo(strategy=strategy, chunks=retrieved),
        no_answer=no_answer,
        confidence_breakdown=breakdown,
        closest_sections=closest if no_answer else [],
    )
