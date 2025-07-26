import React, { createContext, useContext, useReducer } from 'react';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Initial state
const initialState = {
  messages: [
    { id: 1, sender: 'ai', text: 'Hello! How can I help you today?' }
  ],
  isLoading: false,
  userInput: '',
  sessions: [], // Conversation history
  currentSessionId: null,
  sessionsLoading: false,
  sessionsError: null
};

// Action types
const ACTIONS = {
  ADD_MESSAGE: 'ADD_MESSAGE',
  SET_LOADING: 'SET_LOADING',
  SET_USER_INPUT: 'SET_USER_INPUT',
  CLEAR_INPUT: 'CLEAR_INPUT',
  ADD_ERROR_MESSAGE: 'ADD_ERROR_MESSAGE',
  SET_SESSIONS: 'SET_SESSIONS',
  SET_SESSIONS_LOADING: 'SET_SESSIONS_LOADING',
  SET_SESSIONS_ERROR: 'SET_SESSIONS_ERROR',
  SET_MESSAGES: 'SET_MESSAGES',
  SET_CURRENT_SESSION: 'SET_CURRENT_SESSION'
};

// Reducer function
const chatReducer = (state, action) => {
  switch (action.type) {
    case ACTIONS.ADD_MESSAGE:
      return {
        ...state,
        messages: [...state.messages, action.payload]
      };
    case ACTIONS.SET_LOADING:
      return {
        ...state,
        isLoading: action.payload
      };
    case ACTIONS.SET_USER_INPUT:
      return {
        ...state,
        userInput: action.payload
      };
    case ACTIONS.CLEAR_INPUT:
      return {
        ...state,
        userInput: ''
      };
    case ACTIONS.ADD_ERROR_MESSAGE:
      return {
        ...state,
        messages: [...state.messages, action.payload]
      };
    case ACTIONS.SET_SESSIONS:
      return {
        ...state,
        sessions: action.payload,
        sessionsLoading: false,
        sessionsError: null
      };
    case ACTIONS.SET_SESSIONS_LOADING:
      return {
        ...state,
        sessionsLoading: action.payload
      };
    case ACTIONS.SET_SESSIONS_ERROR:
      return {
        ...state,
        sessionsError: action.payload,
        sessionsLoading: false
      };
    case ACTIONS.SET_MESSAGES:
      return {
        ...state,
        messages: action.payload
      };
    case ACTIONS.SET_CURRENT_SESSION:
      return {
        ...state,
        currentSessionId: action.payload
      };
    default:
      return state;
  }
};

const ChatContext = createContext();

export const ChatProvider = ({ children }) => {
  const [state, dispatch] = useReducer(chatReducer, initialState);

  const addMessage = (message) => {
    dispatch({ type: ACTIONS.ADD_MESSAGE, payload: message });
  };

  const setLoading = (loading) => {
    dispatch({ type: ACTIONS.SET_LOADING, payload: loading });
  };

  const setUserInput = (input) => {
    dispatch({ type: ACTIONS.SET_USER_INPUT, payload: input });
  };

  const clearInput = () => {
    dispatch({ type: ACTIONS.CLEAR_INPUT });
  };

  const addErrorMessage = (errorText) => {
    const errorMessage = {
      id: Date.now(),
      sender: 'ai',
      text: errorText
    };
    dispatch({ type: ACTIONS.ADD_ERROR_MESSAGE, payload: errorMessage });
  };

  // Conversation history actions
  const fetchSessions = async (userId = 'anonymous') => {
    dispatch({ type: ACTIONS.SET_SESSIONS_LOADING, payload: true });
    try {
      const res = await fetch(`${API_URL}/api/conversations/${userId}`);
      if (!res.ok) throw new Error('Failed to fetch sessions');
      const data = await res.json();
      dispatch({ type: ACTIONS.SET_SESSIONS, payload: data });
    } catch (err) {
      dispatch({ type: ACTIONS.SET_SESSIONS_ERROR, payload: err.message });
    }
  };

  const loadSessionMessages = async (sessionId) => {
    dispatch({ type: ACTIONS.SET_LOADING, payload: true });
    try {
      const res = await fetch(`${API_URL}/api/conversations/${sessionId}/messages`);
      if (!res.ok) throw new Error('Failed to fetch messages');
      const data = await res.json();
      // Convert backend message format to frontend format
      const formatted = data.map(msg => ({
        id: msg.id,
        sender: msg.message_type,
        text: msg.content,
        timestamp: msg.timestamp
      }));
      dispatch({ type: ACTIONS.SET_MESSAGES, payload: formatted });
      dispatch({ type: ACTIONS.SET_CURRENT_SESSION, payload: sessionId });
    } catch (err) {
      addErrorMessage('Failed to load conversation history.');
    } finally {
      dispatch({ type: ACTIONS.SET_LOADING, payload: false });
    }
  };

  const value = {
    ...state,
    addMessage,
    setLoading,
    setUserInput,
    clearInput,
    addErrorMessage,
    fetchSessions,
    loadSessionMessages,
    setCurrentSession: (id) => dispatch({ type: ACTIONS.SET_CURRENT_SESSION, payload: id })
  };

  return (
    <ChatContext.Provider value={value}>
      {children}
    </ChatContext.Provider>
  );
};

export const useChat = () => {
  const context = useContext(ChatContext);
  if (!context) {
    throw new Error('useChat must be used within a ChatProvider');
  }
  return context;
}; 