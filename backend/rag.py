"""Retrieve similar chunks, then ask the chat model to answer with citations."""

from __future__ import annotations

from pgvector import Vector

from config import LLM_PROVIDER, TOP_K
from db import get_conn
from models import chat, current_chat_model, embed_query


def retrieve(question: str, k: int | None = None) -> list[dict]:
    k = TOP_K if k is None else k
    query_vec = Vector(embed_query(question))
    with get_conn() as conn:
        rows = conn.execute(
            """
            SELECT
                c.content,
                d.source_path,
                c.chunk_index,
                (c.embedding <=> %s) AS distance
            FROM chunks c
            JOIN documents d ON d.id = c.document_id
            WHERE c.embedding IS NOT NULL
            ORDER BY c.embedding <=> %s
            LIMIT %s
            """,
            (query_vec, query_vec, k),
        ).fetchall()
    return [
        {
            "content": row[0],
            "source_path": row[1],
            "chunk_index": row[2],
            "distance": float(row[3]),
        }
        for row in rows
    ]


def _build_messages(question: str, sources: list[dict]) -> list[dict]:
    if not sources:
        return [
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant. There were no retrieved sources. "
                    "Say you do not have that information in the knowledge base."
                ),
            },
            {"role": "user", "content": question},
        ]

    blocks = []
    for i, src in enumerate(sources, start=1):
        blocks.append(
            f"[{i}] {src['source_path']} (chunk {src['chunk_index']})\n{src['content']}"
        )
    joined = "\n\n".join(blocks)
    system = (
        "You answer questions using only the numbered sources below. "
        "If the sources do not contain the answer, say you do not know. "
        "Cite sources like [1] or [2]. Do not invent policies or numbers."
    )
    user = f"Sources:\n{joined}\n\nQuestion: {question}"
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]


def answer_question(question: str, k: int | None = None) -> dict:
    sources = retrieve(question, k=k)
    messages = _build_messages(question, sources)
    answer = chat(messages)
    return {
        "answer": answer,
        "sources": sources,
        "model": current_chat_model(),
        "provider": LLM_PROVIDER,
    }
