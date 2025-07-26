# 🚀 E-commerce Chatbot Backend

FastAPI backend for the E-commerce Website with Chatbot, featuring intelligent AI-powered customer support and comprehensive e-commerce analytics.

## 🏗️ Architecture

### **Core Components**
- **FastAPI Application**: RESTful API with auto-generated documentation
- **Supabase Database**: PostgreSQL with real-time capabilities
- **SQLAlchemy ORM**: Database models and relationships
- **Pydantic Schemas**: Request/response validation
- **Service Layer**: Modular business logic architecture

### **AI/LLM Integration**
- **Groq API**: High-performance LLM inference
- **Llama3-8b-8192**: Advanced language model
- **Query Parsing**: Natural language understanding
- **Response Generation**: Context-aware AI responses

## 📁 File Structure

```
backend/
├── main.py                    # FastAPI application and endpoints
├── database.py               # Database configuration and connection
├── models.py                 # SQLAlchemy ORM models
├── schemas.py                # Pydantic request/response schemas
├── requirements.txt          # Python dependencies
├── README.md                 # This documentation
├── test_supabase.py          # Database connection test
├── supabase_setup.py         # Database initialization
├── supabase_load_data.py     # Data loading from CSV files
└── services/                 # Business logic modules
    ├── __init__.py
    ├── conversation_service.py      # Chat session management
    ├── enhanced_chat_service.py     # Main chatbot orchestration
    ├── ecommerce_service.py         # E-commerce data queries
    ├── llm_service.py              # Groq API integration
    ├── query_parser.py             # Natural language parsing
    └── response_formatter.py       # Response formatting
```

## 🚀 Quick Start

### **1. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **2. Environment Setup**
```bash
# Copy environment template
cp env.example .env

# Edit .env with your credentials
DATABASE_URL=postgresql://user:password@host:port/database
GROQ_API_KEY=your_groq_api_key
```

### **3. Database Setup**
```bash
# Test connection
python test_supabase.py

# Create tables
python supabase_setup.py

# Load sample data
python supabase_load_data.py
```

### **4. Start Server**
```bash
uvicorn main:app --reload
```

### **5. Access API**
- **Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 🔧 Configuration

### **Environment Variables**
```env
# Required
DATABASE_URL=postgresql://user:password@host:port/database
GROQ_API_KEY=your_groq_api_key

# Optional (for Supabase features)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
```

### **Database Models**
- **DistributionCenter**: Warehouse locations
- **User**: Customer information and demographics
- **InventoryItem**: Product catalog and stock
- **Order**: Order details and status tracking
- **OrderItem**: Individual items in orders
- **ConversationSession**: Chat session management
- **ConversationMessage**: Individual chat messages

## 📋 API Endpoints

### **Core Chat Endpoints**
```http
POST /api/chat
Content-Type: application/json

{
  "message": "What are the top 5 products?",
  "conversation_id": "optional-session-id",
  "user_id": "optional-user-id"
}
```

### **Conversation Management**
- `GET /api/conversations/{user_id}` - Get user's chat history
- `GET /api/conversations/{session_id}/messages` - Get session messages
- `DELETE /api/conversations/{session_id}` - Close conversation

### **Analytics Endpoints**
- `GET /api/analytics/top-products?limit=5` - Best-selling products
- `GET /api/orders/{order_id}/status` - Order status lookup
- `GET /api/inventory/stock-levels?product_name=optional` - Stock levels
- `GET /api/analytics/sales` - Sales analytics
- `GET /api/stats` - Database statistics

### **System Endpoints**
- `GET /health` - Health check
- `GET /api/llm/status` - LLM service status

## 🤖 Chatbot Features

### **Natural Language Understanding**
The chatbot can understand queries like:
- "What are the top 5 most sold products?"
- "Show me orders for user 12345"
- "What's the status of order #67890?"
- "Which products are low in stock?"
- "Give me sales analytics for this month"

### **Intelligent Responses**
- **Data-Driven**: Queries actual database for real information
- **Context-Aware**: Maintains conversation history
- **Clarifying**: Asks for missing information when needed
- **Formatted**: Presents data in user-friendly format

### **LLM Enhancement**
- **Groq API**: High-speed inference
- **Llama3-8b-8192**: Advanced language model
- **Fallback Support**: Works without LLM for basic functionality
- **Error Handling**: Graceful degradation on API failures

## 🧪 Testing

### **Database Connection Test**
```bash
python test_supabase.py
```

### **API Testing**
1. Start the server: `uvicorn main:app --reload`
2. Open http://localhost:8000/docs
3. Use the interactive Swagger UI to test endpoints

### **Sample Chat Requests**
```bash
# Test chat endpoint
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "What are the top 3 products?"}'

# Test analytics
curl "http://localhost:8000/api/analytics/top-products?limit=3"

# Test health check
curl "http://localhost:8000/health"
```

## 🔍 Service Architecture

### **EnhancedChatService**
Main orchestrator that:
- Parses user queries
- Determines intent and required data
- Queries database through EcommerceService
- Formats responses
- Integrates with LLM for enhancement

### **QueryParser**
Natural language understanding:
- Identifies query types (products, orders, analytics)
- Extracts parameters (limits, IDs, filters)
- Handles missing information detection

### **EcommerceService**
Database query layer:
- Product analytics and inventory
- Order tracking and status
- User data and demographics
- Sales analytics and trends

### **LLMService**
AI integration:
- Groq API communication
- Response enhancement
- Clarifying question generation
- Fallback handling

## 🚀 Deployment

### **Local Development**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### **Production Considerations**
- Set `DATABASE_URL` to production Supabase instance
- Configure CORS for your frontend domain
- Set up monitoring and logging
- Use environment-specific settings
- Consider rate limiting for LLM API calls



## 🐛 Troubleshooting

### **Common Issues**

**Database Connection Failed**
- Check `DATABASE_URL` in `.env`
- Verify Supabase credentials
- Test with `python test_supabase.py`

**LLM API Errors**
- Verify `GROQ_API_KEY` is set
- Check API quota and limits
- Test with `GET /api/llm/status`

**Data Loading Issues**
- Ensure CSV files exist in `../dataset/archive/`
- Check foreign key constraints
- Review error messages in loading script

### **Logs and Debugging**
- Check FastAPI logs in terminal
- Use `/docs` for API testing
- Review Supabase dashboard for data issues

## 📚 Dependencies

### **Core Dependencies**
- `fastapi==0.104.1` - Web framework
- `uvicorn==0.24.0` - ASGI server
- `sqlalchemy==2.0.23` - ORM
- `psycopg2-binary==2.9.9` - PostgreSQL adapter
- `pandas==2.1.3` - Data processing
- `python-dotenv==1.0.0` - Environment management
- `pydantic==2.5.0` - Data validation
- `groq==0.4.2` - LLM API client

### **Development Dependencies**
- `alembic==1.12.1` - Database migrations
- `python-multipart==0.0.6` - File uploads

## 🤝 Contributing

1. Follow the existing code structure
2. Add type hints and docstrings
3. Test your changes thoroughly
4. Update documentation as needed
5. Use meaningful commit messages

---

**Built with FastAPI, Supabase, and Groq AI** 🚀 