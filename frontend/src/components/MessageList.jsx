import React from 'react';
import Message from './Message';

const MessageList = ({ messages, isLoading }) => {
  return (
    <div style={{ flex: 1, overflowY: 'auto', padding: '16px' }}>
      {messages.map((msg) => (
        <Message key={msg.id} message={msg} />
      ))}
      {isLoading && (
        <div className="message ai-message">
          <div style={{ display: 'flex', alignItems: 'center' }}>
            <span>AI is typing</span>
            <div style={{ marginLeft: '8px', display: 'flex', gap: '2px' }}>
              <div style={{ width: '4px', height: '4px', background: '#666', borderRadius: '50%', animation: 'typing 1.4s infinite' }}></div>
              <div style={{ width: '4px', height: '4px', background: '#666', borderRadius: '50%', animation: 'typing 1.4s infinite 0.2s' }}></div>
              <div style={{ width: '4px', height: '4px', background: '#666', borderRadius: '50%', animation: 'typing 1.4s infinite 0.4s' }}></div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default MessageList; 