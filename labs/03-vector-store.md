# Lab 3 — Vector store (Postgres + pgvector)

**Goal:** Save chunks and embeddings in PostgreSQL so they survive after the Python process exits.

**Why this exists:** Lab 2 kept vectors in RAM. Work uses Postgres. Plain Postgres stores rows and text; it does **not** do “find the 5 most similar chunks” efficiently. The **pgvector** extension adds:

- a `vector` column type
- distance operators such as `<=>` (cosine distance — **smaller** means closer)
- indexes (we use **HNSW**) so search stays fast as the corpus grows

This is the same *kind* of database as work. It is not a copy of work’s data.

## Schema

See [backend/schema.sql](../backend/schema.sql):

- `documents` — one row per file
- `chunks` — one row per chunk, with `embedding vector(768)`
- Re-ingesting a file deletes its old chunks and writes new ones

768 matches `nomic-embed-text`. If you change the embedding model, you must change `EMBEDDING_DIM` and recreate the table (Lab 7 explains this).

## What to run

Postgres must already be up (`docker compose up -d` from Lab 0).

```powershell
python backend\scripts\03_ingest.py
```

Ingest a specific file or folder:

```powershell
python backend\scripts\03_ingest.py data\sample-handbook.md
```

## What to look at

- [docker-compose.yml](../docker-compose.yml) — the database box
- [backend/ingest.py](../backend/ingest.py) — read, chunk, embed, `INSERT`
- [backend/db.py](../backend/db.py) — connection + `init_schema()`

Optional peek inside the database (Docker exec):

```powershell
docker exec -it rag-postgres psql -U rag -d rag -c "SELECT id, source_path FROM documents;"
docker exec -it rag-postgres psql -U rag -d rag -c "SELECT id, chunk_index, left(content, 80) FROM chunks;"
```

## Checkpoint

The script prints JSON like `"files": 1, "chunks": N` with `N` greater than 0. A second run still succeeds (it replaces chunks for the same path).
