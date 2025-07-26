import React from 'react';
import MessageList from './MessageList';
import UserInput from './UserInput';
import { useChat } from '../context/ChatContext';

const ChatWindow = () => {
  const { messages, isLoading, addMessage, setLoading, addErrorMessage } = useChat();

  const sendMessage = async (text) => {
    if (!text.trim()) return;
    
    // Add user message immediately
    const userMessage = { id: Date.now(), sender: 'user', text };
    addMessage(userMessage);
    
    setLoading(true);
    
    try {
      const response = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: text,
          user_id: 'anonymous'
        }),
      });
      
      if (!response.ok) {
        throw new Error('Failed to get response');
      }
      
      const data = await response.json();
      
      // Add AI response
      const aiMessage = { 
        id: Date.now() + 1, 
        sender: 'ai', 
        text: data.response 
      };
      addMessage(aiMessage);
      
    } catch (error) {
      console.error('Error sending message:', error);
      addErrorMessage('Sorry, I\'m having trouble connecting right now. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <MessageList messages={messages} isLoading={isLoading} />
      <UserInput onSend={sendMessage} disabled={isLoading} />
    </div>
  );
};

export default ChatWindow; 