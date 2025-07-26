import React from 'react';
import Message from './Message';

const MessageList = ({ messages, isLoading }) => {
  return (
    <div className="message-list">
      {messages.map((msg) => (
        <Message key={msg.id} message={msg} />
      ))}
      {isLoading && (
        <div className="typing-indicator">
          <span className="typing-text">AI is typing</span>
          <div className="typing-dots">
            <div className="typing-dot"></div>
            <div className="typing-dot"></div>
            <div className="typing-dot"></div>
          </div>
        </div>
      )}
    </div>
  );
};

export default MessageList; 