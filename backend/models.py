from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, Boolean, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

# E-commerce Data Models
class DistributionCenter(Base):
    __tablename__ = "distribution_centers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    
    # Relationships
    inventory_items = relationship("InventoryItem", back_populates="distribution_center")

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    age = Column(Integer)
    gender = Column(String(20))
    state = Column(String(100))
    street_address = Column(String(255))
    postal_code = Column(String(20))
    city = Column(String(100))
    country = Column(String(100))
    latitude = Column(Float)
    longitude = Column(Float)
    traffic_source = Column(String(100))
    created_at = Column(DateTime, default=func.now(), index=True)
    
    # Relationships
    orders = relationship("Order", back_populates="user")
    order_items = relationship("OrderItem", back_populates="user")

class InventoryItem(Base):
    __tablename__ = "inventory_items"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, nullable=False, index=True)
    created_at = Column(DateTime, default=func.now(), index=True)
    sold_at = Column(DateTime, nullable=True, index=True)
    cost = Column(Float, nullable=False)
    product_category = Column(String(100), nullable=False, index=True)
    product_name = Column(String(255), nullable=False, index=True)
    product_brand = Column(String(100), nullable=True)  # Fixed: Allow null values
    product_retail_price = Column(Float, nullable=False)
    product_department = Column(String(100), nullable=False, index=True)
    product_sku = Column(String(100), nullable=False, unique=True, index=True)
    product_distribution_center_id = Column(Integer, ForeignKey("distribution_centers.id"), index=True)
    
    # Relationships
    distribution_center = relationship("DistributionCenter", back_populates="inventory_items")
    order_items = relationship("OrderItem", back_populates="inventory_item")
    
    # Composite index for common queries
    __table_args__ = (
        Index('idx_product_category_brand', 'product_category', 'product_brand'),
        Index('idx_product_name_category', 'product_name', 'product_category'),
    )

class Order(Base):
    __tablename__ = "orders"
    
    order_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    status = Column(String(50), nullable=False, index=True)
    gender = Column(String(20))
    created_at = Column(DateTime, default=func.now(), index=True)
    returned_at = Column(DateTime, nullable=True)
    shipped_at = Column(DateTime, nullable=True, index=True)
    delivered_at = Column(DateTime, nullable=True, index=True)
    num_of_item = Column(Integer, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    
    # Composite index for status queries
    __table_args__ = (
        Index('idx_user_status', 'user_id', 'status'),
        Index('idx_created_status', 'created_at', 'status'),
    )

class OrderItem(Base):
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.order_id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    product_id = Column(Integer, nullable=False, index=True)
    inventory_item_id = Column(Integer, ForeignKey("inventory_items.id"), index=True)
    status = Column(String(50), nullable=False, index=True)
    created_at = Column(DateTime, default=func.now(), index=True)
    shipped_at = Column(DateTime, nullable=True)
    delivered_at = Column(DateTime, nullable=True)
    returned_at = Column(DateTime, nullable=True)
    
    # Relationships
    order = relationship("Order", back_populates="order_items")
    user = relationship("User", back_populates="order_items")
    inventory_item = relationship("InventoryItem", back_populates="order_items")
    
    # Composite index for order queries
    __table_args__ = (
        Index('idx_order_product', 'order_id', 'product_id'),
        Index('idx_user_product', 'user_id', 'product_id'),
    )

# Conversation History Models
class ConversationSession(Base):
    __tablename__ = "conversation_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100), nullable=False, index=True)  # Using string for flexibility
    session_id = Column(String(255), unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=func.now(), index=True)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), index=True)
    is_active = Column(Boolean, default=True, index=True)
    
    # Relationship to messages
    messages = relationship("ConversationMessage", back_populates="session", cascade="all, delete-orphan")
    
    # Composite index for user sessions
    __table_args__ = (
        Index('idx_user_active', 'user_id', 'is_active'),
    )

class ConversationMessage(Base):
    __tablename__ = "conversation_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(255), ForeignKey("conversation_sessions.session_id"), nullable=False, index=True)
    message_type = Column(String(20), nullable=False, index=True)  # 'user' or 'ai'
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=func.now(), index=True)
    
    # Relationship to session
    session = relationship("ConversationSession", back_populates="messages")
    
    # Composite index for session messages
    __table_args__ = (
        Index('idx_session_timestamp', 'session_id', 'timestamp'),
    ) 