# Lab 4 — RAG loop

**Goal:** Answer a question using retrieved handbook chunks, and print citations.

**Why this exists:** RAG = **retrieve** the nearest chunks, then **generate** an answer from a prompt that includes those chunks. The model is still the same HTTP call from Lab 1. The difference is the prompt now contains evidence.

## The loop

1. Embed the question (same embedding model as ingest).
2. SQL: `ORDER BY embedding <=> query LIMIT k`.
3. Build a prompt: instructions + numbered sources + question.
4. Call the chat model. Ask it not to invent policy.

Distance (`<=>`) is cosine **distance**. Lower is better (the opposite of Lab 2’s cosine similarity).

## What to run

```powershell
python backend\scripts\04_rag_cli.py
python backend\scripts\04_rag_cli.py "Who do I call if the espresso machine is down?"
python backend\scripts\04_rag_cli.py "What is the staff Wi-Fi password?"
```

The last question is a negative check: the handbook says staff passwords live in the manager binder, not in the chatbot. A good answer refuses to invent a password.

## What to look at

[backend/rag.py](../backend/rag.py) — `retrieve()`, `_build_messages()`, `answer_question()`.

## Checkpoint

For the employee-discount question, the answer mentions **40%** (or 40 percent) and lists `sample-handbook.md` in sources. If you see “no retrieved sources,” run Lab 3 ingest again.
