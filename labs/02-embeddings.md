# Lab 2 — Embeddings and similarity

**Goal:** Split the sample handbook into chunks, turn each chunk into a vector, and rank chunks by cosine similarity to a question.

**Why this exists:** “Retrieval” is search over vectors, not magic. An **embedding model** maps text to a list of numbers. Two pieces of text with similar meaning have vectors that point in a similar direction. **Cosine similarity** measures that. Lab 3 stores the same vectors in Postgres; this lab does it in memory so you can see the math.

## Terms

- **Chunk** — a slice of a document small enough to retrieve and stuff into a prompt.
- **Overlap** — repeating a little text at chunk boundaries so a sentence is not cut in half and lost.
- **Embedding** — the vector for a chunk (here: 768 numbers from `nomic-embed-text`).
- **Cosine similarity** — `1` means “same direction,” `0` means “unrelated.” Higher is better.

## What to run

```powershell
python backend\scripts\02_embeddings_demo.py
python backend\scripts\02_embeddings_demo.py "When is last call?"
```

## What to look at

- [backend/chunking.py](../backend/chunking.py) — how windows and overlap work
- [backend/scripts/02_embeddings_demo.py](../backend/scripts/02_embeddings_demo.py) — embed + rank, no database
- [backend/models.py](../backend/models.py) — `embed_texts()` calls Ollama `/api/embed`

## Checkpoint

The top-ranked chunk for “What is the employee discount?” mentions **40 percent**. If every score is `0.000`, Ollama did not return embeddings — confirm `nomic-embed-text` with `ollama list`.
