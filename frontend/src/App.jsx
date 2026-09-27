import { useState } from "react";

import ChatWindow from "./components/ChatWindow";
import { uploadScreenshot } from "./services/chatApi";
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
  const [loading, setLoading] = useState(false);

  const handleSend = async (message, fileOverride = null) => {
    const file = fileOverride || selectedFile;

    if (!message.trim() && !file) {
      return;
    }

    const newMessage = {
      id: Date.now(),
      role: "user",
      content: message.trim(),
      file,
    };

    setMessages((current) => [...current, newMessage]);
    setSelectedFile(null);

    if (!file) {
      return;
    }

    setLoading(true);

    try {
      const result = await uploadScreenshot(file);

      const information = result.extracted_information;
      const knowledgeResults = result.knowledge_results || [];

      let content =
        `Detected error: ${information.error_code || "Unknown"}\n\n` +
        `${information.error_message || "No error message detected."}`;

      if (knowledgeResults.length > 0) {
        const bestResult = knowledgeResults[0].entity;

        content +=
          `\n\nPossible solution:\n${bestResult.content}`;
      } else {
        content +=
          "\n\nNo relevant solution was found in the knowledge base.";
      }

      setMessages((current) => [
        ...current,
        {
          id: Date.now() + 1,
          role: "assistant",
          content,
        },
      ]);
    } catch (error) {
      setMessages((current) => [
        ...current,
        {
          id: Date.now() + 1,
          role: "assistant",
          content:
            `Sorry, I could not process the screenshot.\n\n${error.message}`,
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <ChatWindow
        messages={messages}
        selectedFile={selectedFile}
        onFileSelect={setSelectedFile}
        onSend={handleSend}
        onUpload={(file) => handleSend("", file)}
        loading={loading}
      />
    </div>
  );
}

export default App;