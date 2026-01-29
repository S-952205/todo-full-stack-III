from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from typing import Optional
from ..services.agent_service import AgentService, AgentConfig
from uuid import UUID
import os


router = APIRouter()


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str
    conversation_id: str
    user_id: str


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    success: bool
    response: str
    conversation_id: str
    tool_result: Optional[str] = None
    error: Optional[str] = None


@router.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest) -> ChatResponse:
    """
    Chat endpoint that processes user input through the AI agent.

    Args:
        request: Chat request containing message, conversation_id, and user_id

    Returns:
        ChatResponse with AI agent's response
    """
    try:
        # Initialize the agent service
        agent_config = AgentConfig()
        agent_service = AgentService(config=agent_config)

        # Process the chat request
        result = agent_service.chat(
            user_input=request.message,
            conversation_id=request.conversation_id,
            user_id=request.user_id
        )

        if result["success"]:
            return ChatResponse(
                success=True,
                response=result["response"],
                conversation_id=result["conversation_id"],
                tool_result=str(result.get("tool_result", None))
            )
        else:
            raise HTTPException(status_code=500, detail=result.get("error", "Unknown error occurred"))

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


# Additional endpoints to support ChatKit functionality
@router.post("/chatkit", response_model=ChatResponse)
async def chatkit_endpoint(request: ChatRequest) -> ChatResponse:
    """
    ChatKit-compatible endpoint that processes user input through the AI agent.

    This endpoint is designed to work with OpenAI's ChatKit interface.

    Args:
        request: Chat request containing message, conversation_id, and user_id

    Returns:
        ChatResponse with AI agent's response
    """
    try:
        # Initialize the agent service
        agent_config = AgentConfig()
        agent_service = AgentService(config=agent_config)

        # Process the chat request using ChatKit-specific handler
        result = agent_service.process_chatkit_request(
            user_input=request.message,
            thread_id=request.conversation_id,
            user_id=request.user_id
        )

        if result["success"]:
            return ChatResponse(
                success=True,
                response=result["response"],
                conversation_id=result["conversation_id"],
                tool_result=str(result.get("tool_result", None))
            )
        else:
            raise HTTPException(status_code=500, detail=result.get("error", "Unknown error occurred"))

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


# ChatKit thread history endpoint
@router.get("/chatkit/history/{thread_id}", response_model=ChatResponse)
async def get_chatkit_thread_history(thread_id: str) -> ChatResponse:
    """
    Get conversation history for a specific ChatKit thread.

    Args:
        thread_id: ID of the thread to get history for

    Returns:
        ChatResponse with list of messages in the thread
    """
    try:
        from ..tools.mcp_tools import mcp_task_tools

        result = mcp_task_tools.get_conversation_history(conversation_id=thread_id, limit=50)

        if result.success:
            return ChatResponse(
                success=True,
                response=f"Conversation history retrieved successfully. {len(result.data)} messages found.",
                conversation_id=thread_id,
                tool_result=str(result.data)
            )
        else:
            raise HTTPException(status_code=400, detail=result.error)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


class ConversationRequest(BaseModel):
    """Request model for creating a new conversation."""
    title: str
    user_id: str


class ConversationResponse(BaseModel):
    """Response model for conversation operations."""
    success: bool
    data: Optional[dict] = None
    error: Optional[str] = None


@router.post("/api/conversations", response_model=ConversationResponse)
async def create_conversation_endpoint(request: ConversationRequest) -> ConversationResponse:
    """
    Endpoint to create a new conversation.

    Args:
        request: Request containing title and user_id

    Returns:
        ConversationResponse with conversation details
    """
    try:
        from ..tools.mcp_tools import mcp_task_tools

        result = mcp_task_tools.create_conversation(
            title=request.title,
            user_id=request.user_id
        )

        if result.success:
            return ConversationResponse(
                success=True,
                data=result.data
            )
        else:
            raise HTTPException(status_code=400, detail=result.error)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/api/conversations/{user_id}", response_model=ConversationResponse)
async def get_user_conversations_endpoint(user_id: str) -> ConversationResponse:
    """
    Endpoint to get all conversations for a user.

    Args:
        user_id: ID of the user

    Returns:
        ConversationResponse with list of conversations
    """
    try:
        from ..tools.mcp_tools import mcp_task_tools

        result = mcp_task_tools.get_user_conversations(user_id=user_id)

        if result.success:
            return ConversationResponse(
                success=True,
                data={"conversations": result.data}
            )
        else:
            raise HTTPException(status_code=400, detail=result.error)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/api/conversations/{conversation_id}/messages", response_model=ConversationResponse)
async def get_conversation_messages_endpoint(conversation_id: str) -> ConversationResponse:
    """
    Endpoint to get all messages in a conversation.

    Args:
        conversation_id: ID of the conversation

    Returns:
        ConversationResponse with list of messages
    """
    try:
        from ..tools.mcp_tools import mcp_task_tools

        result = mcp_task_tools.get_conversation_messages(conversation_id=conversation_id)

        if result.success:
            return ConversationResponse(
                success=True,
                data={"messages": result.data}
            )
        else:
            raise HTTPException(status_code=400, detail=result.error)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


