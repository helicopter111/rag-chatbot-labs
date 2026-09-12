# Lab 1 — Talk to a model (no RAG)

**Goal:** Send a prompt to Ollama and see the reply stream in the terminal.

**Why this exists:** A large language model on your PC is not a special Python object. It is a **server**. Your code posts JSON to `http://127.0.0.1:11434/api/chat` and reads tokens back. RAG (later labs) is just: build a better prompt, then do this same call.

## What to run

Activate the venv, then:

```powershell
python backend\scripts\01_chat_ollama.py
```

Or pass your own prompt:

```powershell
python backend\scripts\01_chat_ollama.py "What is a vector embedding in one sentence?"
```

## What to look at

Open [backend/scripts/01_chat_ollama.py](../backend/scripts/01_chat_ollama.py). Notice:

- `stream: True` — Ollama sends one JSON object per line as it generates
- The model name comes from `.env` (`OLLAMA_CHAT_MODEL`)
- There is **no** database and **no** document lookup

## Checkpoint

You see a multi-word answer printed token by token. If you get a connection error, start the Ollama app. If you get "model not found", run `ollama list` and set `OLLAMA_CHAT_MODEL` in `.env` to a name you actually have.
