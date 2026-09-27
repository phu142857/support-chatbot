import { useState } from "react";

import ChatWindow from "./components/ChatWindow";
import "./index.css";

function App() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      role: "assistant",
      content:
        "Hello! Send me a screenshot of your problem and I will help you troubleshoot it.",
    },
  ]);

  const [selectedFile, setSelectedFile] = useState(null);

  const handleSend = (message) => {
    if (!message.trim() && !selectedFile) {
      return;
    }

    const newMessage = {
      id: Date.now(),
      role: "user",
      content: message.trim(),
      file: selectedFile,
    };

    setMessages((current) => [...current, newMessage]);

    setSelectedFile(null);

    // Backend integration will be added later.
  };

  return (
    <div className="app">
      <ChatWindow
        messages={messages}
        selectedFile={selectedFile}
        onFileSelect={setSelectedFile}
        onSend={handleSend}
      />
    </div>
  );
}

export default App;