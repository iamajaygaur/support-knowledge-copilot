from __future__ import annotations

import re

from knowledge_copilot.generate.prompt import SYSTEM_PROMPT, build_user_prompt, format_context
from knowledge_copilot.llm import generate_text
from knowledge_copilot.models import RetrievedChunk

NO_ANSWER_PATTERNS = [
    r"could not find",
    r"not (?:found|available) in the (?:docs|documentation|context)",
    r"insufficient (?:context|information)",
    r"i don't have enough",
    r"no (?:relevant|matching) (?:information|documentation)",
]


def generate_answer(question: str, chunks: list[RetrievedChunk]) -> tuple[str, list[str], bool]:
    """Return (answer_text, unverified_items, no_answer_flag)."""
    if not chunks:
        return (
            "I could not find this in the docs. No relevant sections were retrieved.",
            ["No retrieved context"],
            True,
        )

    user_prompt = build_user_prompt(question, format_context(chunks))
    content = generate_text(user_prompt, system=SYSTEM_PROMPT, temperature=0.1)
    answer, unverified = _parse_sections(content)
    no_answer = _is_no_answer(answer)
    return answer, unverified, no_answer


def _parse_sections(content: str) -> tuple[str, list[str]]:
    answer_match = re.search(
        r"ANSWER:\s*(.*?)(?:\n\s*UNVERIFIED:|\Z)", content, flags=re.DOTALL | re.IGNORECASE
    )
    unverified_match = re.search(r"UNVERIFIED:\s*(.*)\Z", content, flags=re.DOTALL | re.IGNORECASE)

    answer = answer_match.group(1).strip() if answer_match else content.strip()
    unverified_raw = unverified_match.group(1).strip() if unverified_match else ""
    unverified: list[str] = []
    if unverified_raw and unverified_raw.lower() not in {"none", "n/a", "na", "-"}:
        for line in unverified_raw.splitlines():
            cleaned = re.sub(r"^[-*•]\s*", "", line).strip()
            if cleaned:
                unverified.append(cleaned)
    return answer, unverified


def _is_no_answer(answer: str) -> bool:
    lowered = answer.lower()
    return any(re.search(pattern, lowered) for pattern in NO_ANSWER_PATTERNS)
