from knowledge_copilot.verify.citations import extract_citation_ids
from knowledge_copilot.verify.confidence import score_confidence
from knowledge_copilot.models import Citation, CitationVerdict, Chunk, RetrievedChunk


def test_extract_citation_ids_preserves_order_unique():
    answer = "Reset MFA [mfa-001]. Then clear lockout [auth-002]. See also [mfa-001]."
    assert extract_citation_ids(answer) == ["mfa-001", "auth-002"]


def test_confidence_rewards_supported_citations():
    retrieved = [
        RetrievedChunk(
            chunk=Chunk(
                chunk_id="c1",
                text="hello",
                source_name="s",
                source_path="s.md",
            ),
            score=0.8,
            sources=["dense"],
        )
    ]
    citations = [
        Citation(
            chunk_id="c1",
            claim="hello",
            verdict=CitationVerdict.SUPPORTED,
        )
    ]
    conf, breakdown = score_confidence(
        retrieved=retrieved,
        citations=citations,
        no_answer=False,
        unverified=[],
    )
    assert conf > 0.7
    assert breakdown["citation_support_rate"] == 1.0
