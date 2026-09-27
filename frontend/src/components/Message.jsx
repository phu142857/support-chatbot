function Message({ message }) {
  const isUser = message.role === "user";

  return (
    <div
      className={`message-row ${
        isUser ? "message-user" : "message-assistant"
      }`}
    >
      <div className="message">
        {!isUser && (
          <div className="message-name">
            Support Assistant
          </div>
        )}

        {message.content && (
          <div className="message-content">
            {message.content}
          </div>
        )}

        {message.file && (
          <div className="message-file">
            <span>📎</span>
            {message.file.name}
          </div>
        )}
      </div>
    </div>
  );
}

export default Message;