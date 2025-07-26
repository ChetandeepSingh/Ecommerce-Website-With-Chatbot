import React from 'react';

const Message = ({ message }) => {
  const isUser = message.sender === 'user';
  return (
    <div className={isUser ? 'message user-message' : 'message ai-message'}>
      {message.text}
    </div>
  );
};

export default Message; 