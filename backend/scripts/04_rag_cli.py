"""Lab 4: retrieve from Postgres, then generate an answer with citations."""

from __future__ import annotations

import sys
from pathlib import Path

BACKEND = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND))

from rag import answer_question  # noqa: E402


def main() -> None:
    question = " ".join(sys.argv[1:]) or "What is the employee discount at Harbor & Pine?"
    result = answer_question(question)
    print(f"Provider: {result['provider']}")
    print(f"Model:    {result['model']}")
    print(f"Question: {question}\n")
    print("Answer:")
    print(result["answer"])
    print("\nSources:")
    for i, src in enumerate(result["sources"], start=1):
        preview = src["content"].replace("\n", " ")[:180]
        print(f"  [{i}] dist={src['distance']:.3f} {src['source_path']}#{src['chunk_index']}")
        print(f"      {preview}\n")


if __name__ == "__main__":
    main()
