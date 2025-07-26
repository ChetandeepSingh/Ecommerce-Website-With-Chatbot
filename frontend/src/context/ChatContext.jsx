import React, { createContext, useContext, useReducer } from 'react';

// Initial state
const initialState = {
  messages: [
    { id: 1, sender: 'ai', text: 'Hello! How can I help you today?' }
  ],
  isLoading: false,
  userInput: ''
};

// Action types
const ACTIONS = {
  ADD_MESSAGE: 'ADD_MESSAGE',
  SET_LOADING: 'SET_LOADING',
  SET_USER_INPUT: 'SET_USER_INPUT',
  CLEAR_INPUT: 'CLEAR_INPUT',
  ADD_ERROR_MESSAGE: 'ADD_ERROR_MESSAGE'
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
    
    default:
      return state;
  }
};

// Create context
const ChatContext = createContext();

// Provider component
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

  const value = {
    ...state,
    addMessage,
    setLoading,
    setUserInput,
    clearInput,
    addErrorMessage
  };

  return (
    <ChatContext.Provider value={value}>
      {children}
    </ChatContext.Provider>
  );
};

// Custom hook to use the chat context
export const useChat = () => {
  const context = useContext(ChatContext);
  if (!context) {
    throw new Error('useChat must be used within a ChatProvider');
  }
  return context;
}; 