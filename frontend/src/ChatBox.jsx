import React, { useState } from "react";
import { generateCode } from "./apiurll";

export default function ChatBox() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  async function handleSubmit(e) {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMessage = { role: "user", content: input.trim() };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);
    setError(null);

    try {
      const res = await generateCode({ prompt: userMessage.content });
      const assistantText =
        typeof res === "string"
          ? res
          : res.output || res.message || JSON.stringify(res);

      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: assistantText },
      ]);
    } catch (err) {
      console.error("Chat error", err);
      setError("Request failed. Check backend and console.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div
      style={{
        height: "220px",
        borderTop: "1px solid #333",
        background: "#1e1e1e",
        display: "flex",
        flexDirection: "column",
      }}
    >
      <div
        style={{
          flex: 1,
          overflowY: "auto",
          padding: "8px 12px",
          fontSize: "13px",
        }}
      >
        {messages.map((m, idx) => (
          <div key={idx} style={{ marginBottom: 6 }}>
            <strong style={{ color: "#9cdcfe" }}>
              {m.role === "user" ? "You" : "Assistant"}:
            </strong>{" "}
            <span style={{ whiteSpace: "pre-wrap" }}>{m.content}</span>
          </div>
        ))}
        {error && (
          <div style={{ color: "#f48771", marginTop: 4 }}>{error}</div>
        )}
      </div>

      <form
        onSubmit={handleSubmit}
        style={{
          borderTop: "1px solid #333",
          padding: "6px 8px",
          display: "flex",
          gap: 8,
        }}
      >
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask the AI to generate or modify code..."
          style={{
            flex: 1,
            background: "#252526",
            border: "1px solid #3c3c3c",
            color: "#fff",
            padding: "4px 8px",
            fontSize: "13px",
          }}
        />
        <button
          type="submit"
          disabled={loading}
          style={{
            background: loading ? "#3c3c3c" : "#0e639c",
            border: "none",
            color: "#fff",
            padding: "4px 10px",
            fontSize: "13px",
            cursor: loading ? "default" : "pointer",
          }}
        >
          {loading ? "Sending..." : "Send"}
        </button>
      </form>
    </div>
  );
}
