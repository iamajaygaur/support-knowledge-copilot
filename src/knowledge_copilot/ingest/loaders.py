from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path

from bs4 import BeautifulSoup
from pypdf import PdfReader

from knowledge_copilot.models import AccessLevel, DocType

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


@dataclass
class LoadedDocument:
    source_path: str
    source_name: str
    text: str
    doc_type: DocType = DocType.OTHER
    access_level: AccessLevel = AccessLevel.INTERNAL
    last_updated: date | None = None
    section_heading: str = ""
    pages: list[tuple[int, str]] = field(default_factory=list)


def _infer_doc_type(path: Path) -> DocType:
    parts = {p.lower() for p in path.parts}
    mapping = {
        "faq": DocType.FAQ,
        "troubleshooting": DocType.TROUBLESHOOTING,
        "onboarding": DocType.ONBOARDING,
        "api": DocType.API,
        "release-notes": DocType.RELEASE_NOTES,
        "release_notes": DocType.RELEASE_NOTES,
        "policies": DocType.POLICY,
        "policy": DocType.POLICY,
    }
    for key, value in mapping.items():
        if key in parts:
            return value
    return DocType.OTHER


def _parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, text
    meta: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        meta[key.strip().lower()] = value.strip().strip("\"'")
    return meta, text[match.end() :]


def _parse_date(value: str | None) -> date | None:
    if not value:
        return None
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y"):
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            continue
    return None


def _parse_access(value: str | None) -> AccessLevel:
    if not value:
        return AccessLevel.INTERNAL
    try:
        return AccessLevel(value.lower())
    except ValueError:
        return AccessLevel.INTERNAL


def load_markdown(path: Path) -> LoadedDocument:
    raw = path.read_text(encoding="utf-8")
    meta, body = _parse_frontmatter(raw)
    return LoadedDocument(
        source_path=str(path),
        source_name=meta.get("source_name", path.name),
        text=body.strip(),
        doc_type=_infer_doc_type(path),
        access_level=_parse_access(meta.get("access_level")),
        last_updated=_parse_date(meta.get("last_updated")),
        section_heading=meta.get("title", path.stem.replace("-", " ").title()),
    )


def load_text(path: Path) -> LoadedDocument:
    return LoadedDocument(
        source_path=str(path),
        source_name=path.name,
        text=path.read_text(encoding="utf-8").strip(),
        doc_type=_infer_doc_type(path),
        section_heading=path.stem.replace("-", " ").title(),
    )


def load_html(path: Path) -> LoadedDocument:
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    for tag in soup(["script", "style"]):
        tag.decompose()
    title = soup.title.string.strip() if soup.title and soup.title.string else path.stem
    text = soup.get_text("\n", strip=True)
    return LoadedDocument(
        source_path=str(path),
        source_name=path.name,
        text=text,
        doc_type=_infer_doc_type(path),
        section_heading=title,
    )


def load_pdf(path: Path) -> LoadedDocument:
    reader = PdfReader(str(path))
    pages: list[tuple[int, str]] = []
    parts: list[str] = []
    for i, page in enumerate(reader.pages, start=1):
        page_text = (page.extract_text() or "").strip()
        if page_text:
            pages.append((i, page_text))
            parts.append(f"[Page {i}]\n{page_text}")
    return LoadedDocument(
        source_path=str(path),
        source_name=path.name,
        text="\n\n".join(parts),
        doc_type=_infer_doc_type(path),
        section_heading=path.stem.replace("-", " ").title(),
        pages=pages,
    )


LOADERS = {
    ".md": load_markdown,
    ".markdown": load_markdown,
    ".txt": load_text,
    ".html": load_html,
    ".htm": load_html,
    ".pdf": load_pdf,
}


def load_documents(source_dir: Path) -> list[LoadedDocument]:
    docs: list[LoadedDocument] = []
    for path in sorted(source_dir.rglob("*")):
        if not path.is_file():
            continue
        loader = LOADERS.get(path.suffix.lower())
        if loader is None:
            continue
        docs.append(loader(path))
    return docs
