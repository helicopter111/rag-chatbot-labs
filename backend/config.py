"""Load settings from the .env file at the repo root.

A .env file is a list of KEY=value lines. We keep secrets and machine-specific
settings there so they are never copied to GitHub.
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

BACKEND_DIR = Path(__file__).resolve().parent
REPO_ROOT = BACKEND_DIR.parent

load_dotenv(REPO_ROOT / ".env")


def _env(name: str, default: str = "") -> str:
    return os.getenv(name, default).strip()


DATABASE_URL = _env("DATABASE_URL", "postgresql://rag:rag@127.0.0.1:5432/rag")
OLLAMA_HOST = _env("OLLAMA_HOST", "http://127.0.0.1:11434").rstrip("/")
LLM_PROVIDER = _env("LLM_PROVIDER", "ollama").lower()
OLLAMA_CHAT_MODEL = _env("OLLAMA_CHAT_MODEL", "qwen3.5")
OLLAMA_EMBED_MODEL = _env("OLLAMA_EMBED_MODEL", "nomic-embed-text")
EMBEDDING_DIM = int(_env("EMBEDDING_DIM", "768"))
OPENAI_API_KEY = _env("OPENAI_API_KEY")
OPENAI_CHAT_MODEL = _env("OPENAI_CHAT_MODEL", "gpt-4o-mini")
ANTHROPIC_API_KEY = _env("ANTHROPIC_API_KEY")
ANTHROPIC_CHAT_MODEL = _env("ANTHROPIC_CHAT_MODEL", "claude-3-5-haiku-latest")
TOP_K = int(_env("TOP_K", "5"))
CHUNK_SIZE = int(_env("CHUNK_SIZE", "800"))
CHUNK_OVERLAP = int(_env("CHUNK_OVERLAP", "100"))
DATA_DIR = REPO_ROOT / "data"
