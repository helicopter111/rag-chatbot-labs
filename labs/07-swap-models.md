# Lab 7 — Swap models

**Goal:** Change the chat model (and optionally the cloud provider) without rewriting the RAG pipeline.

**Why this exists:** Experimenting is the point of a home lab. [backend/models.py](../backend/models.py) is a **model adapter**: one function, `chat(messages)`, with several backends. Retrieval always uses Ollama embeddings so the Postgres `vector(768)` column stays valid.

## Swap a local Ollama model

1. See what you have: `ollama list`
2. Optional: `ollama pull llama3.2` (or any other chat model)
3. Edit `.env`:

```
LLM_PROVIDER=ollama
OLLAMA_CHAT_MODEL=llama3.2
```

4. Restart Flask (`python backend\app.py`) so it reloads `.env`.
5. Ask the same handbook question again and compare tone and accuracy.

This machine already has several chat models (`qwen3.5`, `gemma4`, `dolphin-mistral`, …). Changing the name in `.env` is enough.

## Optional: cloud chat APIs

Embeddings stay on `nomic-embed-text`. Only the **generator** changes.

```
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
OPENAI_CHAT_MODEL=gpt-4o-mini
```

or

```
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_CHAT_MODEL=claude-3-5-haiku-latest
```

Restart Flask. Do not commit `.env`.

## Do not casually swap the embedding model

`chunks.embedding` is `vector(768)`. `nomic-embed-text` produces 768 dimensions. A different embedding size will fail inserts until you change `EMBEDDING_DIM`, update [backend/schema.sql](../backend/schema.sql), drop the tables, and re-ingest.

```powershell
docker exec -it rag-postgres psql -U rag -d rag -c "DROP TABLE IF EXISTS chunks, documents;"
python backend\scripts\03_ingest.py
```

## Checkpoint

After changing `OLLAMA_CHAT_MODEL` (or `LLM_PROVIDER`) and restarting Flask, `/api/health` shows the new `chat_model` / `provider`, and a chat answer still cites the handbook.
