from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import os

from database import get_db, engine
from models import Base
from schemas import (
    ChatRequest, ChatResponse, ConversationSession as ConversationSessionSchema,
    ConversationMessage as ConversationMessageSchema, MessageType
)
from services.conversation_service import ConversationService
from services.ecommerce_service import EcommerceService
from services.query_parser import QueryParser, QueryType
from services.response_formatter import ResponseFormatter

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="E-commerce Chatbot API",
    description="Backend API for E-commerce Customer Support Chatbot",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "E-commerce Chatbot API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

# Conversation endpoints
@app.post("/api/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    """
    Primary chat endpoint that accepts user messages and returns AI responses.
    Enhanced with business logic for e-commerce queries.
    """
    # Get or create conversation session
    user_id = request.user_id or "anonymous"
    conversation_service = ConversationService(db)
    session = conversation_service.get_or_create_session(user_id, request.conversation_id)
    
    # Store user message
    user_message = conversation_service.add_message(
        session.session_id, 
        MessageType.USER, 
        request.message
    )
    
    # Initialize services
    ecommerce_service = EcommerceService(db)
    query_parser = QueryParser()
    response_formatter = ResponseFormatter()
    
    try:
        # Parse the user's query
        parsed_query = query_parser.parse_query(request.message)
        query_type = parsed_query["query_type"]
        parameters = parsed_query["parameters"]
        
        # Generate response based on query type
        ai_response_text = ""
        
        if query_type == QueryType.TOP_PRODUCTS:
            limit = parameters.get("limit", 5)
            products = ecommerce_service.get_top_products(limit)
            ai_response_text = response_formatter.format_top_products_response(products)
            
        elif query_type == QueryType.ORDER_STATUS:
            order_id = parameters.get("order_id")
            order_status = ecommerce_service.get_order_status(order_id)
            ai_response_text = response_formatter.format_order_status_response(order_status)
            
        elif query_type == QueryType.STOCK_LEVELS:
            product_name = parameters.get("product_name")
            stock_levels = ecommerce_service.get_stock_levels(product_name)
            ai_response_text = response_formatter.format_stock_levels_response(stock_levels)
            
        elif query_type == QueryType.USER_ORDERS:
            user_id_param = parameters.get("user_id")
            if user_id_param:
                orders = ecommerce_service.get_user_orders(user_id_param)
                ai_response_text = response_formatter.format_user_orders_response(orders)
            else:
                ai_response_text = "Please provide a user ID to check orders."
                
        elif query_type == QueryType.PRODUCT_DETAILS:
            product_name = parameters.get("product_name")
            products = ecommerce_service.get_product_details(product_name)
            ai_response_text = response_formatter.format_product_details_response(products)
            
        elif query_type == QueryType.SALES_ANALYTICS:
            analytics = ecommerce_service.get_sales_analytics()
            ai_response_text = response_formatter.format_sales_analytics_response(analytics)
            
        else:  # QueryType.GENERAL
            message = parameters.get("message", request.message)
            ai_response_text = response_formatter.format_general_response(message)
        
    except Exception as e:
        # Handle errors gracefully
        ai_response_text = response_formatter.format_error_response("database_error", str(e))
    
    # Store AI response
    ai_message = conversation_service.add_message(
        session.session_id, 
        MessageType.AI, 
        ai_response_text
    )
    
    return ChatResponse(
        response=ai_response_text,
        conversation_id=session.session_id,
        message_id=ai_message.id
    )

@app.get("/api/conversations/{user_id}", response_model=List[ConversationSessionSchema])
async def get_user_conversations(
    user_id: str,
    db: Session = Depends(get_db)
):
    """Get all conversation sessions for a user"""
    conversation_service = ConversationService(db)
    sessions = conversation_service.get_user_sessions(user_id)
    return sessions

@app.get("/api/conversations/{session_id}/messages", response_model=List[ConversationMessageSchema])
async def get_conversation_messages(
    session_id: str,
    db: Session = Depends(get_db)
):
    """Get all messages for a specific conversation session"""
    conversation_service = ConversationService(db)
    session = conversation_service.get_session(session_id)
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation session not found"
        )
    
    messages = conversation_service.get_session_messages(session_id)
    return messages

@app.delete("/api/conversations/{session_id}")
async def close_conversation(
    session_id: str,
    db: Session = Depends(get_db)
):
    """Close a conversation session"""
    conversation_service = ConversationService(db)
    success = conversation_service.close_session(session_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation session not found"
        )
    
    return {"message": "Conversation session closed successfully"}

# Data endpoints (for testing and verification)
@app.get("/api/stats")
async def get_database_stats(db: Session = Depends(get_db)):
    """Get basic database statistics"""
    from models import User, Order, InventoryItem, ConversationSession
    
    stats = {
        "users": db.query(User).count(),
        "orders": db.query(Order).count(),
        "inventory_items": db.query(InventoryItem).count(),
        "conversation_sessions": db.query(ConversationSession).count()
    }
    
    return stats

# Business Logic Testing Endpoints
@app.get("/api/analytics/top-products")
async def get_top_products(limit: int = 5, db: Session = Depends(get_db)):
    """Get top selling products"""
    ecommerce_service = EcommerceService(db)
    return ecommerce_service.get_top_products(limit)

@app.get("/api/orders/{order_id}/status")
async def get_order_status(order_id: int, db: Session = Depends(get_db)):
    """Get order status by ID"""
    ecommerce_service = EcommerceService(db)
    order_status = ecommerce_service.get_order_status(order_id)
    if not order_status:
        raise HTTPException(status_code=404, detail="Order not found")
    return order_status

@app.get("/api/inventory/stock-levels")
async def get_stock_levels(product_name: str = None, db: Session = Depends(get_db)):
    """Get stock levels for products"""
    ecommerce_service = EcommerceService(db)
    return ecommerce_service.get_stock_levels(product_name)

@app.get("/api/analytics/sales")
async def get_sales_analytics(db: Session = Depends(get_db)):
    """Get overall sales analytics"""
    ecommerce_service = EcommerceService(db)
    return ecommerce_service.get_sales_analytics()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 