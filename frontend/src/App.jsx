import { useEffect, useRef, useState } from "react";
import "./App.css";

export default function App() {
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      text: "Ask about the Harbor & Pine handbook. Try: What is the employee discount?",
      sources: [],
    },
  ]);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const [health, setHealth] = useState(null);
  const [error, setError] = useState("");
  const bottom = useRef(null);

  useEffect(() => {
    fetch("/api/health")
      .then((res) => res.json())
      .then(setHealth)
      .catch(() => setError("Cannot reach Flask. Start it with: python backend\\app.py"));
  }, []);

  useEffect(() => {
    bottom.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, busy]);

  async function onSubmit(event) {
    event.preventDefault();
    const text = input.trim();
    if (!text || busy) return;
    setInput("");
    setError("");
    setMessages((prev) => [...prev, { role: "user", text, sources: [] }]);
    setBusy(true);
    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || res.statusText);
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text: data.answer,
          sources: data.sources || [],
          model: data.model,
        },
      ]);
    } catch (err) {
      setError(err.message || String(err));
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text: "The request failed. Confirm Flask, Postgres, and Ollama are running.",
          sources: [],
        },
      ]);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="shell">
      <header className="header">
        <h1>Harbor & Pine handbook chat</h1>
        <p>
          RAG lab UI — answers come from retrieved chunks, not from the model’s
          memory alone.
        </p>
        {health && (
          <p className="status">
            {health.ok ? "API connected" : "API reported a database problem"} ·{" "}
            {health.provider}/{health.chat_model}
          </p>
        )}
        {error && <p className="status error">{error}</p>}
      </header>

      <div className="thread">
        {messages.map((msg, i) => (
          <div className={`bubble ${msg.role}`} key={i}>
            <div className="meta">
              {msg.role === "user" ? "You" : msg.model || "Assistant"}
            </div>
            <div className="body">
              {msg.text}
              {msg.sources?.length > 0 && (
                <div className="sources">
                  {msg.sources.map((src, j) => (
                    <div className="source" key={j}>
                      <strong>
                        [{j + 1}] {src.source_path} · distance {src.distance?.toFixed(3)}
                      </strong>
                      {src.content}
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}
        {busy && (
          <div className="bubble assistant">
            <div className="meta">Assistant</div>
            <div className="body">Retrieving and generating…</div>
          </div>
        )}
        <div ref={bottom} />
      </div>

      <form className="composer" onSubmit={onSubmit}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask a handbook question"
          disabled={busy}
        />
        <button type="submit" disabled={busy}>
          Send
        </button>
      </form>
    </div>
  );
}
