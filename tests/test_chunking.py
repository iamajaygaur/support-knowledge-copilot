from knowledge_copilot.ingest.chunking import chunk_by_headings, chunk_fixed_size
from knowledge_copilot.ingest.loaders import LoadedDocument
from knowledge_copilot.models import DocType


def _doc(text: str) -> LoadedDocument:
    return LoadedDocument(
        source_path="docs/faq/sample.md",
        source_name="sample.md",
        text=text,
        doc_type=DocType.FAQ,
        section_heading="Sample",
    )


def test_heading_chunker_splits_sections():
    text = """# Title

## One

Alpha content about passwords. """ + ("detail " * 80) + """

## Two

Beta content about tokens. """ + ("extra " * 80) + """
"""
    # Small max_chars prevents merge of adjacent short sections.
    chunks = chunk_by_headings(_doc(text), max_chars=200)
    assert len(chunks) >= 2
    assert all(c.chunk_id for c in chunks)
    assert any("Alpha" in c.text for c in chunks)
    assert any("Beta" in c.text for c in chunks)


def test_fixed_chunker_uses_overlap():
    text = "word " * 500
    chunks = chunk_fixed_size(_doc(text), size=200, overlap=50)
    assert len(chunks) > 1
    assert chunks[0].chunk_id != chunks[1].chunk_id
