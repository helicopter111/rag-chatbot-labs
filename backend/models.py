"""One chat interface, several providers.

Swap OLLAMA_CHAT_MODEL or LLM_PROVIDER in .env without changing RAG code.
Embeddings always go through Ollama (nomic-embed-text) so the Postgres
`vector(768)` column stays valid when you try a different chat model.
"""

from __future__ import annotations

import json
import re
from collections.abc import Iterator

import requests

from config import (
    ANTHROPIC_API_KEY,
    ANTHROPIC_CHAT_MODEL,
    LLM_PROVIDER,
    OLLAMA_CHAT_MODEL,
    OLLAMA_EMBED_MODEL,
    OLLAMA_HOST,
    OPENAI_API_KEY,
    OPENAI_CHAT_MODEL,
)

_THINK_RE = re.compile(r"<think>.*?</think>", re.DOTALL | re.IGNORECASE)


def strip_think(text: str) -> str:
    """Some local models wrap inner reasoning in <think> tags. Hide that."""
    return _THINK_RE.sub("", text).strip()


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Turn strings into vectors using the Ollama embedding model."""
    if not texts:
        return []
    url = f"{OLLAMA_HOST}/api/embed"
    response = requests.post(
        url,
        json={"model": OLLAMA_EMBED_MODEL, "input": texts},
        timeout=120,
    )
    response.raise_for_status()
    data = response.json()
    vectors = data.get("embeddings")
    if not vectors:
        raise RuntimeError(f"Ollama embed returned no vectors: {data}")
    return vectors


def embed_query(text: str) -> list[float]:
    return embed_texts([text])[0]


def chat(messages: list[dict], *, stream: bool = False) -> str | Iterator[str]:
    provider = LLM_PROVIDER
    if provider == "ollama":
        if stream:
            return _ollama_chat_stream(messages)
        return _ollama_chat(messages)
    if provider == "openai":
        if stream:
            raise ValueError("Streaming is only wired for Ollama in this lab series.")
        return _openai_chat(messages)
    if provider == "anthropic":
        if stream:
            raise ValueError("Streaming is only wired for Ollama in this lab series.")
        return _anthropic_chat(messages)
    raise ValueError(f"Unknown LLM_PROVIDER={provider!r}. Use ollama, openai, or anthropic.")


def current_chat_model() -> str:
    if LLM_PROVIDER == "openai":
        return OPENAI_CHAT_MODEL
    if LLM_PROVIDER == "anthropic":
        return ANTHROPIC_CHAT_MODEL
    return OLLAMA_CHAT_MODEL


def _ollama_chat(messages: list[dict]) -> str:
    url = f"{OLLAMA_HOST}/api/chat"
    response = requests.post(
        url,
        json={
            "model": OLLAMA_CHAT_MODEL,
            "messages": messages,
            "stream": False,
            "think": False,
        },
        timeout=300,
    )
    response.raise_for_status()
    content = response.json().get("message", {}).get("content", "")
    return strip_think(content)


def _ollama_chat_stream(messages: list[dict]) -> Iterator[str]:
    url = f"{OLLAMA_HOST}/api/chat"
    with requests.post(
        url,
        json={
            "model": OLLAMA_CHAT_MODEL,
            "messages": messages,
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
                yield piece


def _openai_chat(messages: list[dict]) -> str:
    if not OPENAI_API_KEY:
        raise RuntimeError("LLM_PROVIDER=openai but OPENAI_API_KEY is empty in .env")
    from openai import OpenAI

    client = OpenAI(api_key=OPENAI_API_KEY)
    system = " ".join(m["content"] for m in messages if m["role"] == "system")
    chat_messages = [m for m in messages if m["role"] != "system"]
    if system:
        chat_messages = [{"role": "system", "content": system}, *chat_messages]
    result = client.chat.completions.create(
        model=OPENAI_CHAT_MODEL,
        messages=chat_messages,
    )
    return (result.choices[0].message.content or "").strip()


def _anthropic_chat(messages: list[dict]) -> str:
    if not ANTHROPIC_API_KEY:
        raise RuntimeError("LLM_PROVIDER=anthropic but ANTHROPIC_API_KEY is empty in .env")
    import anthropic

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    system = "\n".join(m["content"] for m in messages if m["role"] == "system")
    chat_messages = [
        {"role": m["role"], "content": m["content"]}
        for m in messages
        if m["role"] in ("user", "assistant")
    ]
    kwargs = {
        "model": ANTHROPIC_CHAT_MODEL,
        "max_tokens": 1024,
        "messages": chat_messages,
    }
    if system:
        kwargs["system"] = system
    result = client.messages.create(**kwargs)
    parts = [block.text for block in result.content if getattr(block, "type", "") == "text"]
    return "".join(parts).strip()
