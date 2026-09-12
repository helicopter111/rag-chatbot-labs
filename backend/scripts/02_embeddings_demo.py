"""Lab 2: chunk a document, embed the chunks, rank them by cosine similarity.

Retrieval is not a special database feature — it is "find the vectors closest
to the question vector." Postgres/pgvector (Lab 3) just stores those vectors.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

BACKEND = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND))

from chunking import chunk_text  # noqa: E402
from config import CHUNK_OVERLAP, CHUNK_SIZE, DATA_DIR  # noqa: E402
from models import embed_texts  # noqa: E402

QUESTION = " ".join(sys.argv[1:]) or "What is the employee discount?"


def cosine(a: np.ndarray, b: np.ndarray) -> float:
    denom = float(np.linalg.norm(a) * np.linalg.norm(b))
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)


def main() -> None:
    handbook = DATA_DIR / "sample-handbook.md"
    text = handbook.read_text(encoding="utf-8")
    chunks = chunk_text(text, CHUNK_SIZE, CHUNK_OVERLAP)
    print(f"File: {handbook}")
    print(f"Question: {QUESTION}")
    print(f"Chunks: {len(chunks)} (size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})\n")

    vectors = embed_texts([QUESTION, *chunks])
    query_vec = np.array(vectors[0], dtype=float)
    ranked = []
    for chunk, vector in zip(chunks, vectors[1:], strict=True):
        score = cosine(query_vec, np.array(vector, dtype=float))
        ranked.append((score, chunk))
    ranked.sort(reverse=True)

    for i, (score, chunk) in enumerate(ranked[:5], start=1):
        preview = chunk.replace("\n", " ")[:220]
        print(f"{i}. cosine={score:.3f}")
        print(f"   {preview}\n")


if __name__ == "__main__":
    main()
