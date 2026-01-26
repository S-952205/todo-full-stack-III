from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import uuid


class MessageBase(SQLModel):
    """Base model for Message with shared attributes."""
    conversation_id: str = Field(index=True)  # Indexed for performance
    role: str = Field(regex=r'^(user|assistant|system)$')  # Role validation
    content: str = Field(min_length=1, max_length=10000)
    user_id: str = Field(index=True)  # Indexed for performance


class Message(MessageBase, table=True):
    """Message model representing the database table."""
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata_json: Optional[str] = Field(default=None, max_length=1000)  # Store as JSON string


class MessageCreate(MessageBase):
    """Model for creating a new message."""
    conversation_id: str
    role: str = Field(regex=r'^(user|assistant|system)$')
    content: str = Field(min_length=1, max_length=10000)
    user_id: str


class MessageUpdate(SQLModel):
    """Model for updating an existing message."""
    content: Optional[str] = Field(default=None, min_length=1, max_length=10000)
    metadata_json: Optional[str] = Field(default=None, max_length=1000)


class MessageResponse(MessageBase):
    """Model for returning message data in API responses."""
    id: str
    timestamp: datetime