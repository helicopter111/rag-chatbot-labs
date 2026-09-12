"""Lab 3: write chunks + embeddings into Postgres (pgvector)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

BACKEND = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND))

from config import DATA_DIR  # noqa: E402
from db import init_schema  # noqa: E402
from ingest import ingest_path  # noqa: E402


def main() -> None:
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else DATA_DIR
    init_schema()
    result = ingest_path(target)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
