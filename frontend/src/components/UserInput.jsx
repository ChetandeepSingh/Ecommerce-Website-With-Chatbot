import React from 'react';
import { useChat } from '../context/ChatContext';

const UserInput = ({ onSend, disabled = false }) => {
  const { userInput, setUserInput, clearInput } = useChat();

  const handleSubmit = (e) => {
    e.preventDefault();
    if (userInput.trim() && !disabled) {
      onSend(userInput);
      clearInput();
    }
  };

  return (
    <div className="user-input-container">
      <form onSubmit={handleSubmit} className="user-input-form">
        <input
          type="text"
          placeholder="Type your message..."
          value={userInput}
          onChange={(e) => setUserInput(e.target.value)}
          disabled={disabled}
          className="user-input-field"
        />
        <button 
          type="submit" 
          disabled={disabled}
          className="send-button"
        >
          {disabled ? 'Sending...' : (
            <>
              Send
              <span className="send-icon">→</span>
            </>
          )}
        </button>
      </form>
    </div>
  );
};

export default UserInput; 