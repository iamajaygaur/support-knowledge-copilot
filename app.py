"""Vercel / ASGI entrypoint for Support Knowledge Copilot."""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure `src/` is importable when the package isn't installed yet
_SRC = Path(__file__).resolve().parent / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from knowledge_copilot.api.main import app  # noqa: E402

__all__ = ["app"]
