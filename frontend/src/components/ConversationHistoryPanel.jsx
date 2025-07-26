import React, { useEffect } from 'react';
import { useChat } from '../context/ChatContext';

const ConversationHistoryPanel = ({ userId = 'anonymous', className }) => {
  const {
    sessions,
    sessionsLoading,
    sessionsError,
    currentSessionId,
    fetchSessions,
    loadSessionMessages
  } = useChat();

  useEffect(() => {
    fetchSessions(userId);
    // eslint-disable-next-line
  }, [userId]);

  return (
    <div className={`history-panel ${className || ''}`}>
      <div className="history-header">Past Conversations</div>
      {sessionsLoading && <div className="history-loading">Loading...</div>}
      {sessionsError && <div className="history-error">{sessionsError}</div>}
      <ul className="history-list">
        {sessions && sessions.length === 0 && !sessionsLoading && (
          <li className="history-empty">No past conversations</li>
        )}
        {sessions && sessions.map(session => (
          <li
            key={session.session_id}
            className={`history-item${currentSessionId === session.session_id ? ' active' : ''}`}
            onClick={() => loadSessionMessages(session.session_id)}
            tabIndex={0}
            title={`Started: ${new Date(session.created_at).toLocaleString()}`}
          >
            <div className="history-session-id">Session {session.session_id.slice(-6)}</div>
            <div className="history-date">{new Date(session.created_at).toLocaleDateString()} {new Date(session.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ConversationHistoryPanel; 