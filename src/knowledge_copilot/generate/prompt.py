SYSTEM_PROMPT = """You are a support knowledge assistant for internal documentation.
Answer ONLY using the provided context chunks.
Rules:
1. Every factual claim must include a citation in the form [chunk_id].
2. If the context is insufficient, say you could not find this in the docs.
3. Do not invent policies, error codes, or procedures.
4. Prefer newer documents when context conflicts.
5. Keep answers concise and actionable for support agents.
"""


def build_user_prompt(question: str, context_blocks: str) -> str:
    return f"""Question:
{question}

Context chunks:
{context_blocks}

Respond in this exact format:
ANSWER:
<your answer with [chunk_id] citations>

UNVERIFIED:
<bullet list of things you could not verify from context, or "None">
"""


def format_context(chunks: list) -> str:
    blocks = []
    for item in chunks:
        chunk = item.chunk
        updated = chunk.last_updated.isoformat() if chunk.last_updated else "unknown"
        blocks.append(
            "\n".join(
                [
                    f"[{chunk.chunk_id}]",
                    f"source: {chunk.source_name}",
                    f"section: {chunk.section_heading}",
                    f"last_updated: {updated}",
                    f"doc_type: {chunk.doc_type.value}",
                    chunk.text,
                ]
            )
        )
    return "\n\n---\n\n".join(blocks)
