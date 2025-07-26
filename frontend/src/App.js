import './App.css';
import ChatWindow from './components/ChatWindow';
import { ChatProvider } from './context/ChatContext';

function App() {
  return (
    <ChatProvider>
      <div className="App">
        <div className="app-header">
          <div className="header-content">
            <div className="logo">
              <span className="logo-icon">🤖</span>
              <h1>E-commerce Chatbot</h1>
            </div>
            <p className="subtitle">Your AI-powered shopping assistant</p>
          </div>
        </div>
        <div className="app-main">
          <ChatWindow />
        </div>
      </div>
    </ChatProvider>
  );
}

export default App;
