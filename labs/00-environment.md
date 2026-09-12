# Lab 0 — Environment

**Goal:** Get a Python virtual environment, Node, Docker (Postgres), and Ollama ready, and understand what Cursor and git are doing.

**Why this exists:** The rest of the labs assume these tools. If something later fails, come back here and re-run the checkpoint.

## What each tool is

| Tool | Plain-language job |
| --- | --- |
| **Cursor** | VS Code plus an AI agent in the sidebar. Terminal, files, and debugger work the same. |
| **Git** | A local history of snapshots. A **commit** is one snapshot you can roll back to. |
| **GitHub** | An online copy of those snapshots. Not public unless you choose that. We are not creating it in this lab. |
| **`.venv`** | A private Python folder for *this* project. Packages stay out of your global Python. |
| **Docker Compose** | A recipe that starts Postgres with pgvector already installed. You do not install Postgres into Windows. |
| **Ollama** | A local model server at `http://127.0.0.1:11434`. Chat and embeddings are HTTP calls. |
| **Node / npm** | JavaScript tooling. Lab 6 uses it for the React (Vite) app. We only *check* it here. |
| **`.env`** | Local settings. Copied from `.env.example`. Git ignores `.env` so keys never get uploaded. |

## Commands

From the project folder in PowerShell:

```powershell
python --version
node --version
npm --version
docker --version
ollama --version

python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

copy .env.example .env

docker compose up -d
```

If PowerShell blocks scripts, run this once as yourself (not as admin tricks — just your user):

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Then activate `.venv` again.

Start Ollama from the Start menu if `ollama list` fails. Pull the embedding model (one-time, ~274 MB):

```powershell
ollama pull nomic-embed-text
ollama list
```

This machine already had chat models installed (for example `qwen3.5`). `.env` defaults `OLLAMA_CHAT_MODEL` to `qwen3.5`. To try another local model later (Lab 7):

```powershell
ollama pull llama3.2
```

## Checkpoint — you are done when

- `python --version` prints 3.11 or newer
- `.venv` exists and `pip show flask` works after activate
- `node --version` and `npm --version` print versions
- `docker compose up -d` leaves a container named `rag-postgres` running
- `ollama list` shows `nomic-embed-text` and at least one chat model

If Docker says the engine is not running, start **Docker Desktop** from the Start menu and wait until it says it is running, then retry `docker compose up -d`.

## What we will not do yet

- We will not `git commit` unless you ask.
- We will not create a GitHub (or Cursor) remote until you confirm you want an online backup.
