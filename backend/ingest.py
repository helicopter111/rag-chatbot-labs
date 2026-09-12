"""Read files, chunk them, embed them, store them in Postgres."""

from __future__ import annotations

from pathlib import Path

from pgvector import Vector

from chunking import chunk_text
from config import CHUNK_OVERLAP, CHUNK_SIZE, DATA_DIR, REPO_ROOT
from db import get_conn
from models import embed_texts


def _read_file(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        from pypdf import PdfReader

        reader = PdfReader(str(path))
        pages = [page.extract_text() or "" for page in reader.pages]
        return "\n\n".join(pages)
    return path.read_text(encoding="utf-8")


def iter_source_files(root: Path) -> list[Path]:
    if root.is_file():
        return [root]
    files: list[Path] = []
    for path in sorted(root.rglob("*")):
        if path.suffix.lower() in {".md", ".txt", ".pdf"} and path.is_file():
            files.append(path)
    return files


def ingest_path(root: Path | None = None) -> dict:
    """Insert or replace all chunks for each file under root."""
    root = root or DATA_DIR
    files = iter_source_files(root)
    if not files:
        return {"files": 0, "chunks": 0, "paths": []}

    total_chunks = 0
    stored_paths: list[str] = []
    with get_conn() as conn:
        for path in files:
            text = _read_file(path)
            pieces = chunk_text(text, CHUNK_SIZE, CHUNK_OVERLAP)
            if not pieces:
                continue
            vectors = embed_texts(pieces)
            try:
                rel = str(path.resolve().relative_to(REPO_ROOT)).replace("\\", "/")
            except ValueError:
                rel = str(path).replace("\\", "/")
            document_id = conn.execute(
                """
                INSERT INTO documents (source_path)
                VALUES (%s)
                ON CONFLICT (source_path) DO UPDATE SET created_at = now()
                RETURNING id
                """,
                (rel,),
            ).fetchone()[0]
            conn.execute("DELETE FROM chunks WHERE document_id = %s", (document_id,))
            for index, (content, vector) in enumerate(zip(pieces, vectors, strict=True)):
                conn.execute(
                    """
                    INSERT INTO chunks (document_id, chunk_index, content, embedding)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (document_id, index, content, Vector(vector)),
                )
            total_chunks += len(pieces)
            stored_paths.append(rel)
        conn.commit()
    return {"files": len(stored_paths), "chunks": total_chunks, "paths": stored_paths}
