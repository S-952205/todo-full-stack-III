from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import uuid


class MessageBase(SQLModel):
    """Base model for Message with shared attributes."""
    conversation_id: str = Field(index=True)  # Indexed for performance
    role: str = Field(regex=r'^(user|assistant)$')  # Updated to exclude 'system' for chatkit
    content: str = Field(min_length=1, max_length=10000)
    user_id: str = Field(index=True)  # Indexed for performance
    tool_calls: Optional[str] = Field(default=None)  # JSON string for tool calls
    tool_responses: Optional[str] = Field(default=None)  # JSON string for tool responses


class Message(MessageBase, table=True):
    """Message model representing the database table."""
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class MessageCreate(MessageBase):
    """Model for creating a new message."""
    conversation_id: str
    role: str = Field(regex=r'^(user|assistant)$')
    content: str = Field(min_length=1, max_length=10000)
    user_id: str


class MessageUpdate(SQLModel):
    """Model for updating an existing message."""
    content: Optional[str] = Field(default=None, min_length=1, max_length=10000)
    tool_calls: Optional[str] = Field(default=None)
    tool_responses: Optional[str] = Field(default=None)


class MessageResponse(MessageBase):
    """Model for returning message data in API responses."""
    id: str
    timestamp: datetime