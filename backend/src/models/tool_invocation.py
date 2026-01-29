from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import uuid
from enum import Enum


class ToolStatus(str, Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"


class ToolInvocationBase(SQLModel):
    """Base model for ToolInvocation with shared attributes."""
    message_id: str = Field(index=True)  # Indexed for performance
    tool_name: str = Field(max_length=255)
    parameters: Optional[str] = Field(default=None)  # JSON string
    status: ToolStatus = Field(default=ToolStatus.PENDING)
    result: Optional[str] = None


class ToolInvocation(ToolInvocationBase, table=True):
    """ToolInvocation model representing the database table."""
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None


class ToolInvocationCreate(ToolInvocationBase):
    """Model for creating a new tool invocation."""
    message_id: str
    tool_name: str = Field(max_length=255)
    parameters: Optional[str] = Field(default=None)  # JSON string
    status: ToolStatus = Field(default=ToolStatus.PENDING)


class ToolInvocationUpdate(SQLModel):
    """Model for updating an existing tool invocation."""
    status: Optional[ToolStatus] = Field(default=None)
    result: Optional[str] = Field(default=None)
    completed_at: Optional[datetime] = Field(default=None)


class ToolInvocationResponse(ToolInvocationBase):
    """Model for returning tool invocation data in API responses."""
    id: str
    created_at: datetime
    completed_at: Optional[datetime]