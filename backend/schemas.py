from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

# Chat API Schemas
class MessageType(str, Enum):
    USER = "user"
    AI = "ai"

class ChatRequest(BaseModel):
    message: str = Field(..., description="User's message")
    conversation_id: Optional[str] = Field(None, description="Optional conversation ID to continue existing session")
    user_id: Optional[str] = Field(None, description="User identifier")

class ChatResponse(BaseModel):
    response: str = Field(..., description="AI's response")
    conversation_id: str = Field(..., description="Conversation session ID")
    message_id: int = Field(..., description="Message ID")

class ConversationMessage(BaseModel):
    id: int
    message_type: MessageType
    content: str
    timestamp: datetime
    
    class Config:
        from_attributes = True

class ConversationSession(BaseModel):
    id: int
    user_id: str
    session_id: str
    created_at: datetime
    updated_at: datetime
    is_active: bool
    messages: List[ConversationMessage] = []
    
    class Config:
        from_attributes = True

# E-commerce Data Schemas (for API responses)
class DistributionCenterResponse(BaseModel):
    id: int
    name: str
    latitude: float
    longitude: float
    
    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    age: Optional[int] = None
    gender: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class InventoryItemResponse(BaseModel):
    id: int
    product_id: int
    product_name: str
    product_category: str
    product_brand: str
    product_retail_price: float
    product_department: str
    product_sku: str
    cost: float
    sold_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class OrderResponse(BaseModel):
    order_id: int
    user_id: Optional[int] = None
    status: str
    gender: Optional[str] = None
    created_at: Optional[datetime] = None
    shipped_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    returned_at: Optional[datetime] = None
    num_of_item: int
    
    class Config:
        from_attributes = True

class OrderItemResponse(BaseModel):
    id: int
    order_id: int
    user_id: Optional[int] = None
    product_id: int
    inventory_item_id: Optional[int] = None
    status: str
    created_at: Optional[datetime] = None
    shipped_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    returned_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Analytics Response Schemas
class TopProductResponse(BaseModel):
    product_name: str
    total_sold: int
    revenue: float

class OrderStatusResponse(BaseModel):
    order_id: int
    status: str
    user_name: Optional[str] = None
    items_count: int
    created_at: Optional[datetime] = None
    shipped_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None

class StockLevelResponse(BaseModel):
    product_name: str
    available_stock: int
    total_inventory: int
    product_category: str
    product_brand: str 