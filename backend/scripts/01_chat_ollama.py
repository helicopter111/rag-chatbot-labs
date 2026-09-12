"""Lab 1: talk to a local model. No documents. No database. Just HTTP.

Ollama is a server on your PC. Chat models are not magic functions — they
are HTTP APIs. This script posts a prompt to http://127.0.0.1:11434/api/chat
and prints tokens as they arrive.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv
import os

ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")

HOST = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434").rstrip("/")
MODEL = os.getenv("OLLAMA_CHAT_MODEL", "qwen3.5")
PROMPT = " ".join(sys.argv[1:]) or "In one sentence, what is retrieval-augmented generation?"


def main() -> None:
    print(f"Model: {MODEL}")
    print(f"Prompt: {PROMPT}\n")
    with requests.post(
        f"{HOST}/api/chat",
        json={
            "model": MODEL,
            "messages": [{"role": "user", "content": PROMPT}],
            "stream": True,
            "think": False,
        },
        stream=True,
        timeout=300,
    ) as response:
        response.raise_for_status()
        for line in response.iter_lines():
            if not line:
                continue
            payload = json.loads(line)
            piece = payload.get("message", {}).get("content") or ""
            if piece:
                print(piece, end="", flush=True)
    print("\n")


if __name__ == "__main__":
    main()
