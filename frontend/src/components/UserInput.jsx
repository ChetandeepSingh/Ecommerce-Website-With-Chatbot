import React, { useState } from 'react';

const UserInput = ({ onSend, disabled = false }) => {
  const [input, setInput] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim() && !disabled) {
      onSend(input);
      setInput('');
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ display: 'flex', padding: '16px', borderTop: '1px solid #eee' }}>
      <input
        type="text"
        placeholder="Type your message..."
        value={input}
        onChange={(e) => setInput(e.target.value)}
        disabled={disabled}
        style={{ 
          flex: 1, 
          padding: '10px', 
          fontSize: '1rem', 
          borderRadius: '6px', 
          border: '1px solid #ccc',
          opacity: disabled ? 0.6 : 1
        }}
      />
      <button 
        type="submit" 
        disabled={disabled}
        style={{ 
          marginLeft: '8px', 
          padding: '10px 18px', 
          fontSize: '1rem', 
          borderRadius: '6px', 
          background: disabled ? '#ccc' : '#007bff', 
          color: '#fff', 
          border: 'none',
          cursor: disabled ? 'not-allowed' : 'pointer'
        }}
      >
        {disabled ? 'Sending...' : 'Send'}
      </button>
    </form>
  );
};

export default UserInput; 