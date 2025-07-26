# 🎨 E-commerce Chatbot Frontend

A modern, responsive React frontend for the E-commerce Chatbot with intelligent AI-powered customer support interface.

## 🚀 Features

### **🎯 Milestone 7: Client-Side State Management**
- **React Context API**: Centralized state management using Context API and useReducer
- **State Management**: Handles message list, loading status, and user input value
- **Predictable State Updates**: Reducer pattern for consistent state changes
- **Global State Access**: Easy access to chat state throughout the component tree

### **🎨 Modern UI/UX Design**
- **Gradient Backgrounds**: Beautiful purple-blue gradient theme
- **Glass Morphism**: Backdrop blur effects and transparency
- **Smooth Animations**: Message slide-in, typing indicators, and hover effects
- **Responsive Design**: Mobile-first approach with breakpoints
- **Modern Typography**: Clean, readable font stack
- **Interactive Elements**: Hover states, focus indicators, and transitions

### **💬 Chat Interface**
- **Real-time Messaging**: Instant message display and typing indicators
- **Message Bubbles**: Distinct styling for user and AI messages
- **Auto-scroll**: Automatic scrolling to latest messages
- **Loading States**: Visual feedback during API calls
- **Error Handling**: Graceful error messages and fallbacks

## 🏗️ Architecture

### **State Management (Context API)**
```javascript
// State Structure
{
  messages: [],        // Chat message history
  isLoading: false,    // Loading status indicator
  userInput: ''        // Current user input value
}

// Actions
- ADD_MESSAGE         // Add new message to chat
- SET_LOADING         // Update loading status
- SET_USER_INPUT      // Update input field value
- CLEAR_INPUT         // Clear input field
- ADD_ERROR_MESSAGE   // Add error message
```

### **Component Structure**
```
src/
├── context/
│   └── ChatContext.jsx          # State management context
├── components/
│   ├── ChatWindow.jsx           # Main chat container
│   ├── MessageList.jsx          # Message display area
│   ├── Message.jsx              # Individual message component
│   └── UserInput.jsx            # Input form component
├── App.js                       # Main application component
├── App.css                      # Modern styling
└── index.js                     # Application entry point
```

## 🎨 Design System

### **Color Palette**
- **Primary Gradient**: `#667eea` to `#764ba2`
- **Background**: Linear gradient with purple-blue theme
- **Text**: `#333` for primary, `#666` for secondary
- **Borders**: `#e2e8f0` for subtle separators

### **Typography**
- **Font Family**: System fonts (San Francisco, Segoe UI, etc.)
- **Headings**: Bold weights with gradient text effects
- **Body Text**: Clean, readable sans-serif

### **Spacing & Layout**
- **Container**: Max-width 800px for optimal readability
- **Padding**: Consistent 1rem-1.5rem spacing
- **Border Radius**: 18px for messages, 25px for inputs
- **Shadows**: Subtle depth with rgba shadows

## 🚀 Quick Start

### **Prerequisites**
- Node.js 14+ and npm
- Backend server running on `http://localhost:8000`

### **Installation**
```bash
# Install dependencies
npm install

# Start development server
npm start
```

### **Build for Production**
```bash
npm run build
```

## 📱 Responsive Design

### **Breakpoints**
- **Desktop**: 1200px+ (Full layout)
- **Tablet**: 768px-1199px (Adjusted spacing)
- **Mobile**: 480px-767px (Compact layout)
- **Small Mobile**: <480px (Minimal spacing)

### **Mobile Optimizations**
- Touch-friendly button sizes
- Optimized input fields for mobile keyboards
- Reduced padding and margins
- Simplified animations for performance

## 🔧 Configuration

### **Environment Variables**
Create a `.env` file in the frontend directory:
```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_ENVIRONMENT=development
```

### **API Integration**
The frontend connects to the FastAPI backend at:
- **Chat Endpoint**: `POST /api/chat`
- **CORS**: Configured for local development
- **Error Handling**: Graceful fallbacks for connection issues

## 🎯 State Management Details

### **Context Provider**
```javascript
// Wraps the entire app
<ChatProvider>
  <App />
</ChatProvider>
```

### **Custom Hook**
```javascript
// Easy access to state and actions
const { messages, isLoading, userInput, addMessage, setLoading } = useChat();
```

### **Reducer Pattern**
- **Predictable**: All state changes go through the reducer
- **Debuggable**: Easy to track state changes
- **Testable**: Pure functions for state updates
- **Scalable**: Easy to add new actions and state properties

## 🧪 Testing

### **Component Testing**
```bash
npm test
```

### **Manual Testing**
1. Start the backend server
2. Start the frontend development server
3. Test chat functionality with various queries
4. Verify responsive design on different screen sizes
5. Test error handling by disconnecting backend

## 🚀 Performance Features

### **Optimizations**
- **CSS-in-JS**: Efficient styling with CSS classes
- **Lazy Loading**: Components load as needed
- **Memoization**: React.memo for performance
- **Debounced Input**: Smooth typing experience

### **Accessibility**
- **ARIA Labels**: Screen reader support
- **Keyboard Navigation**: Full keyboard accessibility
- **Focus Management**: Proper focus indicators
- **Color Contrast**: WCAG compliant color ratios

## 🎨 Customization

### **Theming**
Modify `App.css` to customize:
- Color gradients and palettes
- Typography and spacing
- Animation timings and effects
- Border radius and shadows

### **Adding Features**
- New message types with custom styling
- Additional state properties in Context
- Enhanced animations and transitions
- Integration with external services

## 📚 Dependencies

### **Core Dependencies**
- `react`: ^19.1.0 - UI library
- `react-dom`: ^19.1.0 - DOM rendering
- `react-scripts`: 5.0.1 - Build tools

### **Development Dependencies**
- `@testing-library/react`: ^16.3.0 - Testing utilities
- `@testing-library/jest-dom`: ^6.6.3 - DOM testing
- `web-vitals`: ^2.1.4 - Performance monitoring

## 🤝 Contributing

1. Follow the existing code structure
2. Use the Context API for state management
3. Maintain responsive design principles
4. Add appropriate CSS classes for styling
5. Test on multiple screen sizes

---

**Built with React, Context API, and modern CSS** 🎨
