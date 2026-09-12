# Lab 5 — Flask backend

**Goal:** Expose RAG as HTTP routes the UI (and you, via curl) can call.

**Why this exists:** The React app should not talk to Ollama or Postgres. Flask is the same split you use at work: the browser calls JSON endpoints; the server owns retrieval and generation.

## Routes

| Method | Path | Body | Job |
| --- | --- | --- | --- |
| GET | `/api/health` | — | Database + current model |
| POST | `/api/chat` | `{"message": "..."}` | RAG answer + sources |
| POST | `/api/ingest` | `{"path": "data"}` optional | Re-run ingest |

CORS is enabled for the Vite origin `http://127.0.0.1:5173` so Lab 6 can call these routes during development. JSON only — no token streaming yet (that can be a later stretch).

## What to run

```powershell
python backend\app.py
```

Leave that terminal running. In another terminal (venv activated):

```powershell
curl http://127.0.0.1:5000/api/health
curl -H "Content-Type: application/json" -d "{\"message\":\"What is the employee discount?\"}" http://127.0.0.1:5000/api/chat
```

PowerShell equivalent:

```powershell
Invoke-RestMethod http://127.0.0.1:5000/api/health
Invoke-RestMethod http://127.0.0.1:5000/api/chat -Method POST -ContentType "application/json" -Body '{"message":"What is the employee discount?"}'
```

## What to look at

[backend/app.py](../backend/app.py)

## Checkpoint

`/api/health` has `"ok": true` and a `chat_model`. `/api/chat` returns `answer` and `sources`.
