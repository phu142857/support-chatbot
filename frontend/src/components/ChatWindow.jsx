import { useState } from "react";

import Message from "./Message";
import ScreenshotUpload from "./ScreenshotUpload";

function ChatWindow({
  messages,
  selectedFile,
  onFileSelect,
  onSend,
}) {
  const [input, setInput] = useState("");

  const handleSubmit = (event) => {
    event.preventDefault();

    if (!input.trim() && !selectedFile) {
      return;
    }

    onSend(input);
    setInput("");
  };

  return (
    <div className="chat-container">
      <header className="chat-header">
        <div>
          <h1>Support Assistant</h1>
          <p>Screenshot-based technical support</p>
        </div>

        <span className="status">
          <span className="status-dot" />
          Online
        </span>
      </header>

      <main className="chat-messages">
        {messages.map((message) => (
          <Message
            key={message.id}
            message={message}
          />
        ))}
      </main>

      {selectedFile && (
        <div className="selected-file">
          <span>{selectedFile.name}</span>

          <button
            type="button"
            onClick={() => onFileSelect(null)}
          >
            ×
          </button>
        </div>
      )}

      <form
        className="chat-input-area"
        onSubmit={handleSubmit}
      >
        <ScreenshotUpload
          onFileSelect={onFileSelect}
        />

        <input
          type="text"
          value={input}
          onChange={(event) => setInput(event.target.value)}
          placeholder="Describe your problem..."
        />

        <button
          className="send-button"
          type="submit"
        >
          Send
        </button>
      </form>
    </div>
  );
}

export default ChatWindow;