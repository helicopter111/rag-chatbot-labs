# Lab 6 — React chat UI

**Goal:** A browser chat page that calls Flask: type a question, see an answer and source snippets.

**Why this exists:** Full-stack here means the same split as work — React for the conversation, Flask for RAG. Vite is a small dev server (`npm run dev`) with a **proxy**: the browser thinks it is calling `/api/chat` on port 5173; Vite forwards that to Flask on port 5000. That avoids browser CORS headaches during development.

## What to run

Terminal 1 (venv on):

```powershell
python backend\app.py
```

Terminal 2:

```powershell
cd frontend
npm install
npm run dev
```

Open **http://127.0.0.1:5173**. Ask:

- What is the employee discount?
- When is last call on weekdays?
- Who do I call if the espresso machine is down?

## What to look at

- [frontend/src/App.jsx](../frontend/src/App.jsx) — message state, `fetch('/api/chat')`
- [frontend/vite.config.js](../frontend/vite.config.js) — proxy `/api` → Flask

## Checkpoint

You get an answer that matches the handbook, plus source cards under the assistant message. A second question still works (the page does not freeze after one reply).
