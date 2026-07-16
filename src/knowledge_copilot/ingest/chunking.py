from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Literal

from knowledge_copilot.ingest.loaders import LoadedDocument
from knowledge_copilot.models import Chunk

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)
ChunkStrategy = Literal["heading", "fixed"]


def _chunk_id(source_path: str, section: str, index: int, text: str) -> str:
    digest = hashlib.sha1(f"{source_path}|{section}|{index}|{text[:80]}".encode()).hexdigest()[:10]
    stem = re.sub(r"[^a-z0-9]+", "-", Path(source_path).stem.lower()).strip("-")
    return f"{stem}-{index:03d}-{digest}"


def chunk_by_headings(doc: LoadedDocument, max_chars: int = 1200) -> list[Chunk]:
    """Split on markdown headings; merge tiny sections; split oversized ones."""
    text = doc.text
    matches = list(HEADING_RE.finditer(text))
    sections: list[tuple[str, str]] = []

    if not matches:
        sections.append((doc.section_heading or "Body", text))
    else:
        preamble = text[: matches[0].start()].strip()
        if preamble:
            sections.append((doc.section_heading or "Introduction", preamble))
        for i, match in enumerate(matches):
            start = match.end()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            heading = match.group(2).strip()
            body = text[start:end].strip()
            if body:
                sections.append((heading, body))

    chunks: list[Chunk] = []
    # Keep heading sections separate; only merge tiny fragments into the next section.
    pending_heading = ""
    pending_text = ""

    def flush(heading: str, body: str) -> None:
        if not body.strip():
            return
        pieces = _split_long(body, max_chars)
        for idx, piece in enumerate(pieces):
            section = heading if len(pieces) == 1 else f"{heading} (part {idx + 1})"
            chunks.append(_make_chunk(doc, section, len(chunks), piece))

    for heading, body in sections:
        if pending_text and len(pending_text) < 80:
            body = f"{pending_text}\n\n{body}".strip()
            heading = f"{pending_heading} / {heading}" if pending_heading else heading
            pending_heading, pending_text = "", ""
        elif pending_text:
            flush(pending_heading, pending_text)
            pending_heading, pending_text = "", ""

        if len(body) < 80:
            pending_heading, pending_text = heading, body
        else:
            flush(heading, body)

    if pending_text:
        flush(pending_heading, pending_text)
    return chunks


def chunk_fixed_size(doc: LoadedDocument, size: int = 800, overlap: int = 150) -> list[Chunk]:
    text = doc.text.strip()
    if not text:
        return []
    chunks: list[Chunk] = []
    start = 0
    index = 0
    while start < len(text):
        end = min(start + size, len(text))
        piece = text[start:end].strip()
        if piece:
            heading = doc.section_heading or "Body"
            chunks.append(_make_chunk(doc, heading, index, piece))
            index += 1
        if end >= len(text):
            break
        start = max(0, end - overlap)
    return chunks


def _split_long(text: str, max_chars: int) -> list[str]:
    if len(text) <= max_chars:
        return [text]
    parts: list[str] = []
    paragraphs = re.split(r"\n\s*\n", text)
    current = ""
    for para in paragraphs:
        if not current:
            current = para
        elif len(current) + len(para) + 2 <= max_chars:
            current = f"{current}\n\n{para}"
        else:
            parts.append(current)
            current = para
    if current:
        parts.append(current)

    # Hard-split any remaining oversized pieces
    final: list[str] = []
    for part in parts:
        if len(part) <= max_chars:
            final.append(part)
        else:
            for i in range(0, len(part), max_chars):
                final.append(part[i : i + max_chars])
    return final


def _make_chunk(doc: LoadedDocument, section: str, index: int, text: str) -> Chunk:
    page_number = None
    page_match = re.search(r"\[Page (\d+)\]", text)
    if page_match:
        page_number = int(page_match.group(1))

    return Chunk(
        chunk_id=_chunk_id(doc.source_path, section, index, text),
        text=text.strip(),
        source_name=doc.source_name,
        source_path=doc.source_path,
        section_heading=section,
        last_updated=doc.last_updated,
        doc_type=doc.doc_type,
        access_level=doc.access_level,
        page_number=page_number,
        metadata={"chunk_index": index},
    )


def chunk_documents(
    docs: list[LoadedDocument],
    strategy: ChunkStrategy = "heading",
) -> list[Chunk]:
    chunks: list[Chunk] = []
    for doc in docs:
        if strategy == "fixed":
            chunks.extend(chunk_fixed_size(doc))
        else:
            chunks.extend(chunk_by_headings(doc))
    return chunks
