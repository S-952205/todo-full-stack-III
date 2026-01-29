import os
import asyncio
import time
from typing import Dict, Any, List, Optional
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents import function_tool
from pydantic import BaseModel
from ..tools.mcp_tools import mcp_task_tools
from ..services.db_service import DatabaseService
from sqlmodel import Session
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from db import engine  # Import engine from the db module in the backend root directory
from contextlib import contextmanager
import logging


class AgentConfig(BaseModel):
    """Configuration for the AI agent."""
    model: str = "openrouter/auto"  # Use OpenRouter's auto-routing for best free model
    temperature: float = 0.7
    max_tokens: int = 1000


# Configure OpenRouter with free model
open_router_key = os.getenv('OPENROUTER_API_KEY')
if not open_router_key:
    logging.warning("OPENROUTER_API_KEY not found in environment variables")
    open_router_key = "sk-or-v1-dummy-key-for-testing"  # Use dummy key if not set

# Configure AsyncOpenAI for OpenRouter with required headers
client = AsyncOpenAI(
    api_key=open_router_key,
    base_url="https://openrouter.ai/api/v1",
    default_headers={
        "HTTP-Referer": os.getenv('NEXT_PUBLIC_BASE_URL', 'http://localhost:3000'),
        "X-Title": "AI Agent & ChatKit UI"
    }
)

model = OpenAIChatCompletionsModel(
    model='mistralai/mistral-small-3.1-24b-instruct:free',  # Using auto-routing to free models
    openai_client=client
)


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Define function tools that wrap our MCP tools with error handling
@function_tool
def create_conversation(title: str, user_id: str) -> str:
    """
    Create a new conversation.

    Args:
        title: Title for the conversation
        user_id: ID of the user creating the conversation
    """
    try:
        result = mcp_task_tools.create_conversation(title=title, user_id=user_id)
        return str(result.data) if result.success else f"Error: {result.error}"
    except Exception as e:
        logger.error(f"Error creating conversation: {str(e)}")
        return f"Error: {str(e)}"


@function_tool
def get_conversation(conversation_id: str) -> str:
    """
    Retrieve a conversation by its ID.

    Args:
        conversation_id: ID of the conversation to retrieve
    """
    try:
        result = mcp_task_tools.get_conversation(conversation_id=conversation_id)
        return str(result.data) if result.success else f"Error: {result.error}"
    except Exception as e:
        logger.error(f"Error getting conversation {conversation_id}: {str(e)}")
        return f"Error: {str(e)}"


@function_tool
def get_user_conversations(user_id: str) -> str:
    """
    Retrieve all conversations for a specific user.

    Args:
        user_id: ID of the user whose conversations to retrieve
    """
    try:
        result = mcp_task_tools.get_user_conversations(user_id=user_id)
        return str(result.data) if result.success else f"Error: {result.error}"
    except Exception as e:
        logger.error(f"Error getting conversations for user {user_id}: {str(e)}")
        return f"Error: {str(e)}"


@function_tool
def create_message(conversation_id: str, role: str, content: str, user_id: str) -> str:
    """
    Create a new message in a conversation.

    Args:
        conversation_id: ID of the conversation to add the message to
        role: Role of the message sender (user or assistant)
        content: Content of the message
        user_id: ID of the user sending the message
    """
    try:
        result = mcp_task_tools.create_message(
            conversation_id=conversation_id,
            role=role,
            content=content,
            user_id=user_id
        )
        return str(result.data) if result.success else f"Error: {result.error}"
    except Exception as e:
        logger.error(f"Error creating message in conversation {conversation_id}: {str(e)}")
        return f"Error: {str(e)}"


@function_tool
def get_conversation_messages(conversation_id: str) -> str:
    """
    Retrieve all messages for a specific conversation.

    Args:
        conversation_id: ID of the conversation to retrieve messages from
    """
    try:
        result = mcp_task_tools.get_conversation_messages(conversation_id=conversation_id)
        return str(result.data) if result.success else f"Error: {result.error}"
    except Exception as e:
        logger.error(f"Error getting messages for conversation {conversation_id}: {str(e)}")
        return f"Error: {str(e)}"


@function_tool
def get_conversation_history(conversation_id: str, limit: int = 10) -> str:
    """
    Get conversation history with optional limit.

    Args:
        conversation_id: ID of the conversation to get history for
        limit: Maximum number of messages to return (default: 10)
    """
    try:
        result = mcp_task_tools.get_conversation_history(conversation_id=conversation_id, limit=limit)
        return str(result.data) if result.success else f"Error: {result.error}"
    except Exception as e:
        logger.error(f"Error getting history for conversation {conversation_id}: {str(e)}")
        return f"Error: {str(e)}"


class AgentService:
    """Service class to handle AI agent interactions using OpenAI Agents SDK via OpenRouter."""

    def __init__(self, config: Optional[AgentConfig] = None):
        self.config = config or AgentConfig()

        # Create the main agent with instructions and tools
        self.agent = Agent(
            name="AI Assistant",
            instructions="""
            You are a helpful AI assistant that can interact with tools to help users manage conversations and tasks.
            Use the available tools to create conversations, add messages, and retrieve conversation history.
            Be concise and helpful in your responses.
            """,
            model=model,  # Use the configured OpenRouter model
            tools=[
                create_conversation,
                get_conversation,
                get_user_conversations,
                create_message,
                get_conversation_messages,
                get_conversation_history
            ]
        )

    async def _exponential_backoff(self, func, max_retries: int = 3, base_delay: float = 1.0):
        """
        Execute a function with exponential backoff retry logic.

        Args:
            func: The async function to execute
            max_retries: Maximum number of retries
            base_delay: Base delay in seconds between retries

        Returns:
            The result of the function if successful
        """
        for attempt in range(max_retries):
            try:
                return await func()
            except Exception as e:
                if attempt == max_retries - 1:  # Last attempt
                    logger.error(f"Function failed after {max_retries} attempts: {str(e)}")
                    raise e

                delay = base_delay * (2 ** attempt)  # Exponential backoff
                logger.warning(f"Attempt {attempt + 1} failed: {str(e)}, retrying in {delay}s...")
                await asyncio.sleep(delay)

    def _get_db_service(self) -> DatabaseService:
        """Helper method to get database service instance."""
        session = Session(engine)
        return DatabaseService(session)

    def process_request(self, user_input: str, conversation_id: str, user_id: str) -> Dict[str, Any]:
        """
        Process user input through the OpenAI Agent SDK and return response.

        Args:
            user_input: Natural language input from user
            conversation_id: ID of the conversation
            user_id: ID of the user making the request

        Returns:
            Dictionary with agent response and any tool execution results
        """
        start_time = time.time()

        try:
            # Validate inputs
            if not user_input or not conversation_id or not user_id:
                raise ValueError("Missing required parameters: user_input, conversation_id, or user_id")

            # Prepare context for the agent
            context = f"""
            User ID: {user_id}
            Conversation ID: {conversation_id}
            User Input: {user_input}

            Use the appropriate tools to handle this request.
            """

            # Save the user's message to the conversation
            user_msg_result = mcp_task_tools.create_message(
                conversation_id=conversation_id,
                role="user",
                content=user_input,
                user_id=user_id
            )

            if not user_msg_result.success:
                logger.warning(f"Failed to save user message: {user_msg_result.error}")

            # Run the agent with the user input
            result = Runner.run(
                agent=self.agent,
                input=context
            )

            response_text = result.final_output if hasattr(result, 'final_output') else str(result)

            # Save the AI's response to the conversation
            ai_msg_result = mcp_task_tools.create_message(
                conversation_id=conversation_id,
                role="assistant",
                content=response_text,
                user_id="system"  # AI responses are attributed to system
            )

            if not ai_msg_result.success:
                logger.warning(f"Failed to save AI response: {ai_msg_result.error}")

            # Log performance
            duration = time.time() - start_time
            logger.info(f"Request processed in {duration:.2f}s for conversation {conversation_id}")

            return {
                "success": True,
                "response": response_text,
                "tool_result": None,  # Tool results are handled within the agent
                "conversation_id": conversation_id,
                "processing_time": duration
            }

        except Exception as e:
            # Log the error for debugging
            error_msg = f"Error in process_request: {str(e)}"
            logger.error(error_msg, exc_info=True)

            # Attempt to save error message to the conversation
            try:
                mcp_task_tools.create_message(
                    conversation_id=conversation_id,
                    role="assistant",
                    content=f"I encountered an error: {str(e)}",
                    user_id="system"
                )
            except Exception as save_error:
                logger.error(f"Failed to save error message: {str(save_error)}")

            # Log performance even for failed requests
            duration = time.time() - start_time
            logger.info(f"Failed request processed in {duration:.2f}s for conversation {conversation_id}")

            return {
                "success": False,
                "error": str(e),
                "response": "Sorry, I encountered an error processing your request.",
                "conversation_id": conversation_id,
                "processing_time": duration
            }

    def chat(self, user_input: str, conversation_id: str, user_id: str) -> Dict[str, Any]:
        """
        Main chat interface method using OpenAI Agents SDK.

        Args:
            user_input: Natural language input from user
            conversation_id: ID of the conversation
            user_id: ID of the user making the request

        Returns:
            Dictionary with the AI response
        """
        return self.process_request(user_input, conversation_id, user_id)

    def process_chatkit_request(self, user_input: str, thread_id: str, user_id: str) -> Dict[str, Any]:
        """
        Process ChatKit-specific request format using OpenAI Agents SDK.

        Args:
            user_input: Natural language input from user
            thread_id: ID of the chat thread (equivalent to conversation_id)
            user_id: ID of the user making the request

        Returns:
            Dictionary with agent response formatted for ChatKit
        """
        # For ChatKit, we'll use the same processing logic
        return self.process_request(user_input, thread_id, user_id)