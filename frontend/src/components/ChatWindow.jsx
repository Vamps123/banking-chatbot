import { useState } from "react";
import MessageBubble from "./MessageBubble";

export default function ChatWindow({ messages, onSend, loading }) {
  const [draft, setDraft] = useState("");

  const handleSubmit = (event) => {
    event.preventDefault();
    onSend(draft);
    setDraft("");
  };

  return (
    <div className="chat-window">
      <div className="messages" aria-live="polite">
        {messages.map((message, index) => (
          <MessageBubble key={index} role={message.role} text={message.text} />
        ))}
        {loading && <div className="typing-indicator">Typing...</div>}
      </div>
      <form className="composer" onSubmit={handleSubmit}>
        <input
          value={draft}
          onChange={(event) => setDraft(event.target.value)}
          placeholder="Ask a banking question..."
          aria-label="Ask a banking question"
        />
        <button type="submit">Send</button>
      </form>
    </div>
  );
}
