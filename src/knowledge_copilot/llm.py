from __future__ import annotations

import json
import re
import time
from functools import lru_cache

from google import genai
from google.genai import types
from google.genai.errors import ClientError, ServerError

from knowledge_copilot.config import get_settings

_RETRYABLE_CODES = {429, 503, 500}


def _looks_like_placeholder(key: str) -> bool:
    lowered = key.lower()
    return (
        not key
        or "your-key" in lowered
        or "your_api" in lowered
        or key in {"sk-your-key-here", "AIzaSy-your-key-here"}
    )


@lru_cache
def get_genai_client() -> genai.Client:
    settings = get_settings()
    key = (settings.google_api_key or "").strip()
    if _looks_like_placeholder(key):
        raise RuntimeError(
            "GOOGLE_API_KEY is missing or still a placeholder. "
            "Set it in .env locally, or in Streamlit Cloud → App settings → Secrets "
            '(e.g. GOOGLE_API_KEY = "your-key"). '
            "Get a key from https://aistudio.google.com/apikey"
        )
    return genai.Client(api_key=key)


def _is_retryable(exc: Exception) -> bool:
    if isinstance(exc, (ClientError, ServerError)):
        code = getattr(exc, "code", None) or getattr(exc, "status_code", None)
        if code in _RETRYABLE_CODES:
            return True
        msg = str(exc).lower()
        return any(token in msg for token in ("429", "503", "unavailable", "resource_exhausted", "high demand"))
    return False


def _with_retries(fn, *, attempts: int = 5, base_delay: float = 2.0):
    last_exc: Exception | None = None
    for attempt in range(attempts):
        try:
            return fn()
        except Exception as exc:  # noqa: BLE001
            last_exc = exc
            if not _is_retryable(exc) or attempt == attempts - 1:
                raise
            delay = base_delay * (2**attempt)
            # Cap so demos don't hang forever
            time.sleep(min(delay, 20.0))
    assert last_exc is not None
    raise last_exc


def _candidate_models() -> list[str]:
    settings = get_settings()
    primary = settings.llm_model
    fallbacks = [
        primary,
        "gemini-flash-latest",
        "gemini-flash-lite-latest",
        "gemini-2.0-flash-lite",
        "gemini-2.0-flash",
    ]
    # Preserve order, unique
    seen: set[str] = set()
    ordered: list[str] = []
    for model in fallbacks:
        if model and model not in seen:
            ordered.append(model)
            seen.add(model)
    return ordered


def generate_text(
    prompt: str,
    *,
    system: str | None = None,
    temperature: float = 0.1,
) -> str:
    client = get_genai_client()
    config = types.GenerateContentConfig(
        temperature=temperature,
        system_instruction=system,
    )
    last_exc: Exception | None = None
    for model in _candidate_models():
        try:
            response = _with_retries(
                lambda m=model: client.models.generate_content(
                    model=m,
                    contents=prompt,
                    config=config,
                )
            )
            return (response.text or "").strip()
        except Exception as exc:  # noqa: BLE001
            last_exc = exc
            if not _is_retryable(exc):
                raise
            continue
    assert last_exc is not None
    raise last_exc


def generate_json(
    prompt: str,
    *,
    system: str | None = None,
    temperature: float = 0.0,
) -> dict:
    client = get_genai_client()
    config = types.GenerateContentConfig(
        temperature=temperature,
        system_instruction=system,
        response_mime_type="application/json",
    )
    content = ""
    last_exc: Exception | None = None
    for model in _candidate_models():
        try:
            response = _with_retries(
                lambda m=model: client.models.generate_content(
                    model=m,
                    contents=prompt,
                    config=config,
                )
            )
            content = (response.text or "").strip()
            break
        except Exception as exc:  # noqa: BLE001
            last_exc = exc
            if not _is_retryable(exc):
                raise
            continue
    else:
        assert last_exc is not None
        raise last_exc

    if not content:
        return {}
    try:
        data = json.loads(content)
        return data if isinstance(data, dict) else {"data": data}
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", content, flags=re.DOTALL)
        if not match:
            return {}
        try:
            data = json.loads(match.group(0))
            return data if isinstance(data, dict) else {"data": data}
        except json.JSONDecodeError:
            return {}
