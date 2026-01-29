from sqlmodel import Session, select
from typing import List, Optional
from ..models import (
    Conversation,
    Message,
    ToolInvocation,
    ConversationCreate,
    MessageCreate,
    ToolInvocationCreate,
    ConversationUpdate,
    MessageUpdate,
    ToolInvocationUpdate
)
from uuid import UUID
import json


class DatabaseService:
    """Service class to handle all database operations for the AI Agent & ChatKit UI."""

    def __init__(self, session: Session):
        self.session = session

    # Conversation CRUD operations
    def create_conversation(self, conversation_data: ConversationCreate) -> Conversation:
        """Create a new conversation."""
        conversation = Conversation(
            title=conversation_data.title,
            user_id=conversation_data.user_id,
            status=conversation_data.status
        )
        self.session.add(conversation)
        self.session.commit()
        self.session.refresh(conversation)
        return conversation

    def get_conversation_by_id(self, conversation_id: str) -> Optional[Conversation]:
        """Retrieve a conversation by its ID."""
        statement = select(Conversation).where(Conversation.id == conversation_id)
        return self.session.exec(statement).first()

    def get_conversations_by_user(self, user_id: str) -> List[Conversation]:
        """Retrieve all conversations for a specific user."""
        statement = select(Conversation).where(Conversation.user_id == user_id)
        return self.session.exec(statement).all()

    def update_conversation(self, conversation_id: str, update_data: ConversationUpdate) -> Optional[Conversation]:
        """Update an existing conversation."""
        conversation = self.get_conversation_by_id(conversation_id)
        if not conversation:
            return None

        update_dict = update_data.dict(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(conversation, field, value)

        self.session.add(conversation)
        self.session.commit()
        self.session.refresh(conversation)
        return conversation

    def delete_conversation(self, conversation_id: str) -> bool:
        """Soft delete a conversation by marking it as deleted."""
        conversation = self.update_conversation(conversation_id, ConversationUpdate(status="deleted"))
        return conversation is not None

    # Message CRUD operations
    def create_message(self, message_data: MessageCreate) -> Message:
        """Create a new message."""
        message = Message(
            conversation_id=message_data.conversation_id,
            role=message_data.role,
            content=message_data.content,
            user_id=message_data.user_id,
            tool_calls=message_data.tool_calls,
            tool_responses=message_data.tool_responses
        )
        self.session.add(message)
        self.session.commit()
        self.session.refresh(message)
        return message

    def get_messages_by_conversation(self, conversation_id: str) -> List[Message]:
        """Retrieve all messages for a specific conversation."""
        statement = select(Message).where(Message.conversation_id == conversation_id).order_by(Message.timestamp)
        return self.session.exec(statement).all()

    def get_message_by_id(self, message_id: str) -> Optional[Message]:
        """Retrieve a message by its ID."""
        statement = select(Message).where(Message.id == message_id)
        return self.session.exec(statement).first()

    def update_message(self, message_id: str, update_data: MessageUpdate) -> Optional[Message]:
        """Update an existing message."""
        message = self.get_message_by_id(message_id)
        if not message:
            return None

        update_dict = update_data.dict(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(message, field, value)

        self.session.add(message)
        self.session.commit()
        self.session.refresh(message)
        return message

    # Tool Invocation CRUD operations
    def create_tool_invocation(self, tool_invocation_data: ToolInvocationCreate) -> ToolInvocation:
        """Create a new tool invocation record."""
        tool_invocation = ToolInvocation(
            message_id=tool_invocation_data.message_id,
            tool_name=tool_invocation_data.tool_name,
            parameters=tool_invocation_data.parameters,
            status=tool_invocation_data.status,
            result=tool_invocation_data.result
        )
        self.session.add(tool_invocation)
        self.session.commit()
        self.session.refresh(tool_invocation)
        return tool_invocation

    def get_tool_invocations_by_message(self, message_id: str) -> List[ToolInvocation]:
        """Retrieve all tool invocations for a specific message."""
        statement = select(ToolInvocation).where(ToolInvocation.message_id == message_id)
        return self.session.exec(statement).all()

    def get_tool_invocation_by_id(self, tool_invocation_id: str) -> Optional[ToolInvocation]:
        """Retrieve a tool invocation by its ID."""
        statement = select(ToolInvocation).where(ToolInvocation.id == tool_invocation_id)
        return self.session.exec(statement).first()

    def update_tool_invocation(self, tool_invocation_id: str, update_data: ToolInvocationUpdate) -> Optional[ToolInvocation]:
        """Update an existing tool invocation."""
        tool_invocation = self.get_tool_invocation_by_id(tool_invocation_id)
        if not tool_invocation:
            return None

        update_dict = update_data.dict(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(tool_invocation, field, value)

        self.session.add(tool_invocation)
        self.session.commit()
        self.session.refresh(tool_invocation)
        return tool_invocation

    def get_conversation_history(self, conversation_id: str, limit: int = 50) -> List[Message]:
        """Get conversation history with optional limit."""
        statement = select(Message).where(
            Message.conversation_id == conversation_id
        ).order_by(Message.timestamp.desc()).limit(limit)
        messages = self.session.exec(statement).all()
        return list(reversed(messages))  # Return in chronological order