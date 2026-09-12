"""Flask API: the React UI talks to these routes, not to Ollama or Postgres directly."""

from __future__ import annotations

import sys
from pathlib import Path

from flask import Flask, jsonify, request
from flask_cors import CORS

BACKEND_DIR = Path(__file__).resolve().parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from config import DATA_DIR, LLM_PROVIDER  # noqa: E402
from db import init_schema  # noqa: E402
from ingest import ingest_path  # noqa: E402
from models import current_chat_model  # noqa: E402
from rag import answer_question  # noqa: E402

app = Flask(__name__)
CORS(app, origins=["http://127.0.0.1:5173", "http://localhost:5173"])


@app.get("/api/health")
def health():
    try:
        init_schema()
        db_ok = True
        db_error = None
    except Exception as exc:  # noqa: BLE001 — health should never crash the process
        db_ok = False
        db_error = str(exc)
    return jsonify(
        {
            "ok": db_ok,
            "database": db_ok,
            "database_error": db_error,
            "provider": LLM_PROVIDER,
            "chat_model": current_chat_model(),
        }
    )


@app.post("/api/chat")
def chat_route():
    body = request.get_json(silent=True) or {}
    message = (body.get("message") or "").strip()
    if not message:
        return jsonify({"error": "message is required"}), 400
    result = answer_question(message)
    return jsonify(result)


@app.post("/api/ingest")
def ingest_route():
    body = request.get_json(silent=True) or {}
    raw_path = body.get("path")
    target = Path(raw_path) if raw_path else DATA_DIR
    if not target.exists():
        return jsonify({"error": f"path not found: {target}"}), 400
    init_schema()
    result = ingest_path(target)
    return jsonify(result)


if __name__ == "__main__":
    init_schema()
    app.run(host="127.0.0.1", port=5000, debug=True)
