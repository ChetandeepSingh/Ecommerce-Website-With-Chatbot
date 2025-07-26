import React, { useState, useEffect } from 'react';
import MessageList from './MessageList';
import UserInput from './UserInput';
import ConversationHistoryPanel from './ConversationHistoryPanel';
import { useChat } from '../context/ChatContext';

const MOBILE_BREAKPOINT = 900; // px

const ChatWindow = () => {
  const { messages, isLoading, addMessage, setLoading, addErrorMessage } = useChat();

  const [showHistory, setShowHistory] = useState(false);
  const [isMobile, setIsMobile] = useState(window.innerWidth <= MOBILE_BREAKPOINT);

  useEffect(() => {
    const handleResize = () => {
      const mobile = window.innerWidth <= MOBILE_BREAKPOINT;
      setIsMobile(mobile);
      if (!mobile) {
        setShowHistory(true); // always show on desktop
      } else {
        setShowHistory(false); // hidden by default on mobile
      }
    };
    window.addEventListener('resize', handleResize);
    handleResize();
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const toggleHistory = () => {
    setShowHistory(prev => !prev);
  };

  const sendMessage = async (text) => {
    if (!text.trim()) return;
    addMessage({ id: Date.now(), sender: 'user', text });
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text, user_id: 'anonymous' }),
      });
      if (!response.ok) throw new Error('Failed to get response');
      const data = await response.json();
      addMessage({ id: Date.now() + 1, sender: 'ai', text: data.response });
    } catch (error) {
      console.error('Error sending message:', error);
      addErrorMessage('Sorry, I\'m having trouble connecting right now. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  // Close history panel when clicking outside on mobile
  const handleBackdropClick = () => {
    if (isMobile) {
      setShowHistory(false);
    }
  };

  return (
    <div className="chat-container chat-with-history">
      {isMobile && (
        <>
          <button 
            className={`history-toggle-btn ${showHistory ? 'open' : ''}`} 
            onClick={toggleHistory}
            aria-label={showHistory ? 'Close conversation history' : 'Open conversation history'}
          >
            <span className="hamburger-icon"></span>
          </button>
          {showHistory && <div className="backdrop" onClick={handleBackdropClick}></div>}
        </>
      )}
      <ConversationHistoryPanel 
        className={isMobile ? (showHistory ? 'mobile-visible' : 'mobile-hidden') : ''} 
      />
      <div className="chat-main-panel">
        <MessageList messages={messages} isLoading={isLoading} />
        <UserInput onSend={sendMessage} disabled={isLoading} />
      </div>
    </div>
  );
};

export default ChatWindow; 