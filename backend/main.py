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
    This is a placeholder implementation for Milestone 3.
    The actual LLM integration will be added in Milestone 5.
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
    
    # Placeholder AI response (will be replaced with LLM in Milestone 5)
    ai_response_text = f"I received your message: '{request.message}'. This is a placeholder response. LLM integration will be added in the next milestone."
    
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 