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
from services.enhanced_chat_service import EnhancedChatService

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
    Enhanced with LLM integration and intelligent business logic.
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
    
    # Initialize enhanced chat service
    enhanced_chat_service = EnhancedChatService(db)
    
    try:
        # Get conversation history for context
        conversation_history = conversation_service.get_session_messages(session.session_id)
        history_context = [
            {"role": msg.message_type, "content": msg.content}
            for msg in conversation_history[-5:]  # Last 5 messages for context
        ]
        
        # Process message with enhanced service
        ai_response_text, needs_clarification, missing_info = enhanced_chat_service.process_message(
            request.message, history_context
        )
        
    except Exception as e:
        # Handle errors gracefully
        ai_response_text = f"I'm having trouble processing your request right now. Please try again later. Error: {str(e)}"
    
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
    from services.ecommerce_service import EcommerceService
    ecommerce_service = EcommerceService(db)
    return ecommerce_service.get_top_products(limit)

@app.get("/api/orders/{order_id}/status")
async def get_order_status(order_id: int, db: Session = Depends(get_db)):
    """Get order status by ID"""
    from services.ecommerce_service import EcommerceService
    ecommerce_service = EcommerceService(db)
    order_status = ecommerce_service.get_order_status(order_id)
    if not order_status:
        raise HTTPException(status_code=404, detail="Order not found")
    return order_status

@app.get("/api/inventory/stock-levels")
async def get_stock_levels(product_name: str = None, db: Session = Depends(get_db)):
    """Get stock levels for products"""
    from services.ecommerce_service import EcommerceService
    ecommerce_service = EcommerceService(db)
    return ecommerce_service.get_stock_levels(product_name)

@app.get("/api/analytics/sales")
async def get_sales_analytics(db: Session = Depends(get_db)):
    """Get overall sales analytics"""
    from services.ecommerce_service import EcommerceService
    ecommerce_service = EcommerceService(db)
    return ecommerce_service.get_sales_analytics()

@app.get("/api/llm/status")
async def get_llm_status(db: Session = Depends(get_db)):
    """Get LLM service status"""
    enhanced_chat_service = EnhancedChatService(db)
    return enhanced_chat_service.get_llm_status()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 