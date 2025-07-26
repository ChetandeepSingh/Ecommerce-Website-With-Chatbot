import React from 'react';
import ReactMarkdown from 'react-markdown';

const Message = ({ message }) => {
  const isUser = message.sender === 'user';
  return (
    <div className={isUser ? 'message user-message' : 'message ai-message'}>
      {isUser ? (
        message.text
      ) : (
        <ReactMarkdown>{message.text}</ReactMarkdown>
      )}
    </div>
  );
};

export default Message; 