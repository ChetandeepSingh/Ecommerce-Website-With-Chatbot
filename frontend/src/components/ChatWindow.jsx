import React, { useState } from 'react';
import MessageList from './MessageList';
import UserInput from './UserInput';

const ChatWindow = () => {
  const [messages, setMessages] = useState([
    { id: 1, sender: 'ai', text: 'Hello! How can I help you today?' }
  ]);
  const [isLoading, setIsLoading] = useState(false);

  const sendMessage = async (text) => {
    if (!text.trim()) return;
    
    // Add user message immediately
    const userMessage = { id: Date.now(), sender: 'user', text };
    setMessages(prev => [...prev, userMessage]);
    
    setIsLoading(true);
    
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
      setMessages(prev => [...prev, aiMessage]);
      
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = { 
        id: Date.now() + 1, 
        sender: 'ai', 
        text: 'Sorry, I\'m having trouble connecting right now. Please try again later.' 
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
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