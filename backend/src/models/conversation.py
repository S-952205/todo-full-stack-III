from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import uuid


class ConversationBase(SQLModel):
    """Base model for Conversation with shared attributes."""
    title: str = Field(min_length=1, max_length=200)
    user_id: str = Field(index=True)  # Indexed for performance
    is_active: bool = Field(default=True)


class Conversation(ConversationBase, table=True):
    """Conversation model representing the database table."""
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ConversationCreate(ConversationBase):
    """Model for creating a new conversation."""
    title: str = Field(min_length=1, max_length=200)
    user_id: str


class ConversationUpdate(SQLModel):
    """Model for updating an existing conversation."""
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    is_active: Optional[bool] = Field(default=None)


class ConversationResponse(ConversationBase):
    """Model for returning conversation data in API responses."""
    id: str
    created_at: datetime
    updated_at: datetime