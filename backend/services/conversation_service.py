from sqlalchemy.orm import Session
from sqlalchemy import and_
from models import ConversationSession, ConversationMessage
from schemas import MessageType
import uuid
from datetime import datetime
from typing import Optional, List

class ConversationService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_session(self, user_id: str) -> ConversationSession:
        """Create a new conversation session"""
        session_id = str(uuid.uuid4())
        session = ConversationSession(
            user_id=user_id,
            session_id=session_id,
            is_active=True
        )
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session
    
    def get_session(self, session_id: str) -> Optional[ConversationSession]:
        """Get an existing conversation session"""
        return self.db.query(ConversationSession).filter(
            ConversationSession.session_id == session_id,
            ConversationSession.is_active == True
        ).first()
    
    def get_user_sessions(self, user_id: str) -> List[ConversationSession]:
        """Get all active sessions for a user"""
        return self.db.query(ConversationSession).filter(
            ConversationSession.user_id == user_id,
            ConversationSession.is_active == True
        ).order_by(ConversationSession.updated_at.desc()).all()
    
    def add_message(self, session_id: str, message_type: MessageType, content: str) -> ConversationMessage:
        """Add a message to a conversation session"""
        message = ConversationMessage(
            session_id=session_id,
            message_type=message_type.value,
            content=content
        )
        self.db.add(message)
        
        # Update session's updated_at timestamp
        session = self.get_session(session_id)
        if session:
            session.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(message)
        return message
    
    def get_session_messages(self, session_id: str) -> List[ConversationMessage]:
        """Get all messages for a conversation session"""
        return self.db.query(ConversationMessage).filter(
            ConversationMessage.session_id == session_id
        ).order_by(ConversationMessage.timestamp.asc()).all()
    
    def close_session(self, session_id: str) -> bool:
        """Close a conversation session"""
        session = self.get_session(session_id)
        if session:
            session.is_active = False
            self.db.commit()
            return True
        return False
    
    def get_or_create_session(self, user_id: str, conversation_id: Optional[str] = None) -> ConversationSession:
        """Get existing session or create new one"""
        if conversation_id:
            session = self.get_session(conversation_id)
            if session and session.user_id == user_id:
                return session
        
        # Create new session
        return self.create_session(user_id) 