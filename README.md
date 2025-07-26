# 🛒 E-commerce Website with Chatbot

A modern e-commerce platform with an intelligent AI chatbot for customer support, built with Python FastAPI backend and Supabase database.

## 🚀 Features

### **🤖 Intelligent Chatbot**
- **LLM Integration**: Powered by Groq API with Llama3-8b-8192 model
- **Natural Language Processing**: Understands customer queries in plain English
- **E-commerce Analytics**: Provides insights on products, orders, and sales
- **Clarifying Questions**: Asks for missing information when needed
- **Conversation History**: Maintains context across chat sessions

### **📊 E-commerce Analytics**
- **Top Products**: Best-selling items analysis
- **Order Tracking**: Real-time order status updates
- **Stock Management**: Inventory level monitoring
- **Sales Analytics**: Revenue and performance insights
- **Customer Data**: User behavior and demographics

### **🛠️ Technical Stack**
- **Backend**: Python FastAPI
- **Database**: Supabase (PostgreSQL)
- **AI/LLM**: Groq API
- **ORM**: SQLAlchemy
- **Data Processing**: Pandas
- **API Documentation**: Auto-generated Swagger UI

## 📁 Project Structure

```
Ecommerce Website with Chatbot/
├── backend/                 # FastAPI backend application
│   ├── main.py             # FastAPI app and API endpoints
│   ├── database.py         # Database configuration
│   ├── models.py           # SQLAlchemy models
│   ├── schemas.py          # Pydantic schemas
│   ├── services/           # Business logic modules
│   └── requirements.txt    # Python dependencies
├── dataset/                # E-commerce sample data
│   └── archive/           # CSV files for testing
├── frontend/              # Frontend application (coming soon)
└── README.md              # This file
```

## 🚀 Quick Start

### **Prerequisites**
- Python 3.8+
- Supabase account
- Groq API key

### **Backend Setup**
```bash
# Clone the repository
git clone <repository-url>
cd Ecommerce-Website-with-Chatbot

# Install dependencies
cd backend
pip install -r requirements.txt

# Set up environment variables
cp env.example .env
# Edit .env with your Supabase and Groq credentials

# Set up database
python supabase_setup.py

# Load sample data
python supabase_load_data.py

# Start the server
uvicorn main:app --reload
```

### **Access the API**
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Chat Endpoint**: POST http://localhost:8000/api/chat

## 📋 API Endpoints

### **Chat & Conversation**
- `POST /api/chat` - Main chatbot endpoint
- `GET /api/conversations/{user_id}` - Get user conversations
- `GET /api/conversations/{session_id}/messages` - Get conversation messages
- `DELETE /api/conversations/{session_id}` - Close conversation

### **Analytics & Data**
- `GET /api/analytics/top-products` - Get best-selling products
- `GET /api/orders/{order_id}/status` - Get order status
- `GET /api/inventory/stock-levels` - Get inventory levels
- `GET /api/analytics/sales` - Get sales analytics
- `GET /api/stats` - Get database statistics

### **System**
- `GET /health` - Health check
- `GET /api/llm/status` - LLM service status

## 🤖 Chatbot Examples

### **Product Queries**
```
User: "What are the top 5 most sold products?"
Bot: "Based on our data, the top 5 most sold products are..."

User: "Show me products in the Electronics category"
Bot: "Here are the Electronics products in our inventory..."
```

### **Order Queries**
```
User: "What's the status of order #12345?"
Bot: "Order #12345 is currently 'Shipped' and expected to arrive..."

User: "How many orders do I have?"
Bot: "You have 3 orders in your account..."
```

### **Analytics Queries**
```
User: "What are our sales trends?"
Bot: "Our sales have increased by 15% this month..."

User: "Which products are low in stock?"
Bot: "The following products are running low on inventory..."
```

## 🔧 Configuration

### **Environment Variables**
```env
# Database
DATABASE_URL=postgresql://user:password@host:port/database

# AI/LLM
GROQ_API_KEY=your_groq_api_key

# Supabase (optional)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
```

## 📊 Database Schema

### **Core Tables**
- **users** - Customer information
- **orders** - Order details and status
- **order_items** - Individual items in orders
- **inventory_items** - Product inventory
- **distribution_centers** - Warehouse locations
- **conversation_sessions** - Chat sessions
- **conversation_messages** - Chat messages

## 🧪 Testing

### **Test Database Connection**
```bash
python test_supabase.py
```

### **Test API Endpoints**
1. Open http://localhost:8000/docs
2. Try the interactive API documentation
3. Test chat endpoint with sample queries

## 🚀 Deployment

### **Local Development**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### **Production**
- Deploy to cloud platforms (Heroku, AWS, etc.)
- Set up environment variables
- Configure CORS for your domain
- Set up monitoring and logging

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Check the API documentation at `/docs`
- Review the backend README for technical details
- Open an issue for bugs or feature requests

---

**Built with ❤️ using FastAPI, Supabase, and Groq AI** 