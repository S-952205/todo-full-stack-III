from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from ..models import ConversationCreate, MessageCreate, ToolInvocationCreate
from ..services.db_service import DatabaseService
from sqlmodel import Session
from contextlib import contextmanager
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from db import engine  # Import engine from the db module in the backend root directory


class ToolResult(BaseModel):
    """Standard result format for all MCP tools."""
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    message: Optional[str] = None


def get_db_session():
    """Context manager to get database session."""
    with Session(engine) as session:
        yield session


class MCPTaskTools:
    """MCP Tools for basic CRUD operations on tasks and related entities."""

    def __init__(self):
        pass

    def _get_db_service(self) -> DatabaseService:
        """Helper method to get database service instance."""
        session_gen = get_db_session()
        session = next(session_gen)
        return DatabaseService(session)

    def create_conversation(self, title: str, user_id: str, status: Optional[str] = "active") -> ToolResult:
        """
        Create a new conversation.

        Args:
            title: Title for the conversation
            user_id: ID of the user creating the conversation
            status: Status of the conversation (default: active)
        """
        try:
            db_service = self._get_db_service()

            conversation_data = ConversationCreate(
                title=title,
                user_id=user_id,
                status=status
            )

            conversation = db_service.create_conversation(conversation_data)

            return ToolResult(
                success=True,
                data={
                    "id": str(conversation.id),
                    "title": conversation.title,
                    "user_id": conversation.user_id,
                    "status": conversation.status.value,
                    "created_at": conversation.created_at.isoformat()
                },
                message="Conversation created successfully"
            )
        except Exception as e:
            return ToolResult(
                success=False,
                error=str(e),
                message="Failed to create conversation"
            )

    def get_conversation(self, conversation_id: str) -> ToolResult:
        """
        Retrieve a conversation by its ID.

        Args:
            conversation_id: ID of the conversation to retrieve
        """
        try:
            db_service = self._get_db_service()
            conversation = db_service.get_conversation_by_id(conversation_id)

            if not conversation:
                return ToolResult(
                    success=False,
                    error="Conversation not found",
                    message="No conversation found with the provided ID"
                )

            return ToolResult(
                success=True,
                data={
                    "id": str(conversation.id),
                    "title": conversation.title,
                    "user_id": conversation.user_id,
                    "status": conversation.status.value,
                    "created_at": conversation.created_at.isoformat(),
                    "updated_at": conversation.updated_at.isoformat()
                },
                message="Conversation retrieved successfully"
            )
        except Exception as e:
            return ToolResult(
                success=False,
                error=str(e),
                message="Failed to retrieve conversation"
            )

    def get_user_conversations(self, user_id: str) -> ToolResult:
        """
        Retrieve all conversations for a specific user.

        Args:
            user_id: ID of the user whose conversations to retrieve
        """
        try:
            db_service = self._get_db_service()
            conversations = db_service.get_conversations_by_user(user_id)

            conversations_data = []
            for conv in conversations:
                conversations_data.append({
                    "id": str(conv.id),
                    "title": conv.title,
                    "user_id": conv.user_id,
                    "status": conv.status.value,
                    "created_at": conv.created_at.isoformat(),
                    "updated_at": conv.updated_at.isoformat()
                })

            return ToolResult(
                success=True,
                data=conversations_data,
                message=f"Retrieved {len(conversations_data)} conversations for user"
            )
        except Exception as e:
            return ToolResult(
                success=False,
                error=str(e),
                message="Failed to retrieve user conversations"
            )

    def create_message(self, conversation_id: str, role: str, content: str, user_id: str,
                      tool_calls: Optional[str] = None, tool_responses: Optional[str] = None) -> ToolResult:
        """
        Create a new message in a conversation.

        Args:
            conversation_id: ID of the conversation to add the message to
            role: Role of the message sender (user or assistant)
            content: Content of the message
            user_id: ID of the user sending the message
            tool_calls: JSON string of tool calls made during the message
            tool_responses: JSON string of responses from tools
        """
        try:
            db_service = self._get_db_service()

            message_data = MessageCreate(
                conversation_id=conversation_id,
                role=role,
                content=content,
                user_id=user_id,
                tool_calls=tool_calls,
                tool_responses=tool_responses
            )

            message = db_service.create_message(message_data)

            return ToolResult(
                success=True,
                data={
                    "id": str(message.id),
                    "conversation_id": message.conversation_id,
                    "role": message.role,
                    "content": message.content,
                    "user_id": message.user_id,
                    "timestamp": message.timestamp.isoformat(),
                    "tool_calls": message.tool_calls,
                    "tool_responses": message.tool_responses
                },
                message="Message created successfully"
            )
        except Exception as e:
            return ToolResult(
                success=False,
                error=str(e),
                message="Failed to create message"
            )

    def get_conversation_messages(self, conversation_id: str) -> ToolResult:
        """
        Retrieve all messages for a specific conversation.

        Args:
            conversation_id: ID of the conversation to retrieve messages from
        """
        try:
            db_service = self._get_db_service()
            messages = db_service.get_messages_by_conversation(conversation_id)

            messages_data = []
            for msg in messages:
                messages_data.append({
                    "id": str(msg.id),
                    "conversation_id": msg.conversation_id,
                    "role": msg.role,
                    "content": msg.content,
                    "user_id": msg.user_id,
                    "timestamp": msg.timestamp.isoformat(),
                    "tool_calls": msg.tool_calls,
                    "tool_responses": msg.tool_responses
                })

            return ToolResult(
                success=True,
                data=messages_data,
                message=f"Retrieved {len(messages_data)} messages for conversation"
            )
        except Exception as e:
            return ToolResult(
                success=False,
                error=str(e),
                message="Failed to retrieve conversation messages"
            )

    def create_tool_invocation(self, message_id: str, tool_name: str,
                              parameters: Optional[str] = None,
                              result: Optional[str] = None) -> ToolResult:
        """
        Create a record of a tool invocation.

        Args:
            message_id: ID of the message that triggered the tool invocation
            tool_name: Name of the tool that was invoked
            parameters: JSON string of parameters passed to the tool
            result: Result of the tool invocation
        """
        try:
            db_service = self._get_db_service()

            tool_invocation_data = ToolInvocationCreate(
                message_id=message_id,
                tool_name=tool_name,
                parameters=parameters,
                result=result
            )

            tool_invocation = db_service.create_tool_invocation(tool_invocation_data)

            return ToolResult(
                success=True,
                data={
                    "id": str(tool_invocation.id),
                    "message_id": tool_invocation.message_id,
                    "tool_name": tool_invocation.tool_name,
                    "parameters": tool_invocation.parameters,
                    "status": tool_invocation.status.value,
                    "result": tool_invocation.result,
                    "created_at": tool_invocation.created_at.isoformat()
                },
                message="Tool invocation recorded successfully"
            )
        except Exception as e:
            return ToolResult(
                success=False,
                error=str(e),
                message="Failed to record tool invocation"
            )

    def get_conversation_history(self, conversation_id: str, limit: int = 50) -> ToolResult:
        """
        Get conversation history with optional limit.

        Args:
            conversation_id: ID of the conversation to get history for
            limit: Maximum number of messages to return (default: 50)
        """
        try:
            db_service = self._get_db_service()
            messages = db_service.get_conversation_history(conversation_id, limit)

            messages_data = []
            for msg in messages:
                messages_data.append({
                    "id": str(msg.id),
                    "conversation_id": msg.conversation_id,
                    "role": msg.role,
                    "content": msg.content,
                    "user_id": msg.user_id,
                    "timestamp": msg.timestamp.isoformat(),
                    "tool_calls": msg.tool_calls,
                    "tool_responses": msg.tool_responses
                })

            return ToolResult(
                success=True,
                data=messages_data,
                message=f"Retrieved {len(messages_data)} messages for conversation history"
            )
        except Exception as e:
            return ToolResult(
                success=False,
                error=str(e),
                message="Failed to retrieve conversation history"
            )


# Global instance of MCP tools
mcp_task_tools = MCPTaskTools()