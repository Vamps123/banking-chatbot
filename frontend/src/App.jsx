import { useEffect, useState } from "react";
import ChatWindow from "./components/ChatWindow";
import UploadPanel from "./components/UploadPanel";
import { sendMessage, uploadDocument, getHealth } from "./services/api";

const initialMessages = [
  { role: "assistant", text: "Welcome to GenAI Banking Support. Ask me about loans, cards, accounts, or banking policies." },
];

export default function App() {
  const [sessionId] = useState(() => `session-${Math.random().toString(36).slice(2, 10)}`);
  const [messages, setMessages] = useState(initialMessages);
  const [loading, setLoading] = useState(false);
  const [health, setHealth] = useState(null);

  useEffect(() => {
    getHealth().then(setHealth).catch(() => setHealth(null));
  }, []);

  const handleSend = async (text) => {
    if (!text.trim()) return;
    const userMessage = { role: "user", text };
    setMessages((prev) => [...prev, userMessage]);
    setLoading(true);

    try {
      // Streamed response (SSE-like via POST) if supported by backend
      let assistantText = "";
      setMessages((prev) => [...prev, { role: "assistant", text: "" }]);

      await sendMessageStream({ session_id: sessionId, message: text }, (_event, data) => {
        if (data.type === "delta") {
          assistantText += data.text;
          setMessages((prev) => {
            const next = [...prev];
            // Update the last assistant bubble
            const lastIdx = next.length - 1;
            next[lastIdx] = { ...next[lastIdx], text: assistantText };
            return next;
          });
        }
      });

      // done
    } catch (err) {
      // fallback to non-stream mode
      const response = await sendMessage({ session_id: sessionId, message: text });
      setMessages((prev) => {
        // replace last assistant placeholder with final response
        const next = [...prev];
        const lastIdx = next.length - 1;
        next[lastIdx] = { role: "assistant", text: response.response };
        return next;
      });
    } finally {
      setLoading(false);
    }

  };

  const handleUpload = async (file) => {
    const result = await uploadDocument(file);
    setMessages((prev) => [...prev, { role: "assistant", text: `Uploaded ${result.filename} and indexed ${result.chunks_added} chunks.` }]);
  };

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <h1>GenAI Banking Support</h1>
        <p>Session ID: {sessionId}</p>
        <small>{health ? `Backend ready: ${health.status}` : "Connecting..."}</small>
        <UploadPanel onUpload={handleUpload} />
      </aside>
      <main className="chat-pane">
        <ChatWindow messages={messages} onSend={handleSend} loading={loading} />
      </main>
    </div>
  );
}
