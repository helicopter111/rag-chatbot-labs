# RAG chatbot labs

A from-scratch, full-stack **retrieval-augmented generation (RAG)** chatbot you can run on a home PC.

You already know Python, Flask, and React from work. These labs rebuild that pattern locally:

- **Ollama** — chat and embedding models running on your machine
- **Flask** — API (`/api/chat`, `/api/ingest`, `/api/health`)
- **React (Vite)** — chat UI
- **Postgres + pgvector** — the same *kind* of vector store as work (not a copy of work’s data)

Each lab is a short write-up plus working code. Read the lab file, run the command, then look at the Python it executed.

## Lab map

| Lab | File | What you learn |
| --- | --- | --- |
| 0 | [labs/00-environment.md](labs/00-environment.md) | Cursor, git, venv, Docker, Ollama |
| 1 | [labs/01-talk-to-a-model.md](labs/01-talk-to-a-model.md) | An LLM is an HTTP call |
| 2 | [labs/02-embeddings.md](labs/02-embeddings.md) | Chunking, vectors, cosine similarity |
| 3 | [labs/03-vector-store.md](labs/03-vector-store.md) | Store embeddings in Postgres/pgvector |
| 4 | [labs/04-rag-loop.md](labs/04-rag-loop.md) | Retrieve, then generate, with citations |
| 5 | [labs/05-backend-api.md](labs/05-backend-api.md) | Flask wraps the RAG loop |
| 6 | [labs/06-chat-ui.md](labs/06-chat-ui.md) | React chat page |
| 7 | [labs/07-swap-models.md](labs/07-swap-models.md) | Change models in `.env`, not in code |

## Quick start (after Lab 0)

In PowerShell from this folder:

```powershell
.\.venv\Scripts\Activate.ps1
docker compose up -d
python backend\scripts\03_ingest.py
python backend\app.py
```

In a second terminal:

```powershell
cd frontend
npm run dev
```

Open http://127.0.0.1:5173 and ask: **What is the employee discount?**

## How the pieces connect

```
React chat UI  -->  Flask  -->  RAG pipeline  -->  Postgres (pgvector)
                                      |
                                      +-->  chat model (Ollama, or OpenAI/Anthropic)
                                      +-->  embedding model (Ollama nomic-embed-text)
```

## Vocabulary (plain language)

- **Repo** — this project folder plus its history of snapshots (commits).
- **Virtual environment (`.venv`)** — a private Python install so this project’s packages do not mix with other projects.
- **`.env`** — local settings and API keys. Git ignores it so keys stay on your PC.
- **Docker Compose** — a recipe that starts Postgres in a container (“a database in a box”).
- **Ollama** — a local server that runs models. Same idea as calling an API, but the model lives on your machine.
- **Embedding** — a list of numbers that represents the *meaning* of a piece of text.
- **RAG** — search your documents for relevant chunks, then send those chunks plus the question to a chat model.

## GitHub

This folder is already a git repo. We have not created an online copy yet. When you want a backup on GitHub (or Cursor), ask in chat — a commit is a snapshot; GitHub is the online copy of those snapshots. It is not public unless you choose that.
