# AI Agent & ChatKit UI - API Documentation

## Overview
This document describes the API endpoints for the AI Agent & ChatKit UI feature. The system provides an intelligent chat interface that connects to OpenAI's agents via OpenRouter, with conversation persistence and tool integration.

## Authentication
All endpoints require JWT authentication in the Authorization header:
```
Authorization: Bearer <jwt_token>
```

## Endpoints

### Chat Endpoints

#### POST /api/chat
Process a chat message through the AI agent.

**Request Body:**
```json
{
  "message": "User's message content",
  "conversation_id": "ID of the conversation",
  "user_id": "ID of the user"
}
```

**Response:**
```json
{
  "success": true,
  "response": "AI agent's response",
  "conversation_id": "ID of the conversation",
  "tool_result": "Result of any tools executed",
  "processing_time": 1.23
}
```

#### POST /chatkit
ChatKit-compatible endpoint for OpenAI's ChatKit interface.

**Request Body:**
```json
{
  "message": "User's message content",
  "conversation_id": "ID of the conversation (thread)",
  "user_id": "ID of the user"
}
```

**Response:**
```json
{
  "success": true,
  "response": "AI agent's response",
  "conversation_id": "ID of the conversation",
  "tool_result": "Result of any tools executed"
}
```

### Conversation Management Endpoints

#### POST /api/conversations
Create a new conversation.

**Request Body:**
```json
{
  "title": "Title for the conversation",
  "user_id": "ID of the user"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "conversation_id",
    "title": "Conversation title",
    "user_id": "user_id",
    "status": "active",
    "created_at": "timestamp"
  }
}
```

#### GET /api/conversations/{user_id}
Get all conversations for a user.

**Response:**
```json
{
  "success": true,
  "data": {
    "conversations": [
      {
        "id": "conversation_id",
        "title": "Conversation title",
        "user_id": "user_id",
        "status": "active",
        "created_at": "timestamp",
        "updated_at": "timestamp"
      }
    ]
  }
}
```

#### GET /api/conversations/{conversation_id}/messages
Get all messages in a conversation.

**Response:**
```json
{
  "success": true,
  "data": {
    "messages": [
      {
        "id": "message_id",
        "conversation_id": "conversation_id",
        "role": "user|assistant",
        "content": "Message content",
        "user_id": "user_id",
        "timestamp": "timestamp",
        "tool_calls": "JSON string of tool calls",
        "tool_responses": "JSON string of tool responses"
      }
    ]
  }
}
```

#### GET /chatkit/history/{thread_id}
Get conversation history for ChatKit interface.

**Response:**
```json
{
  "success": true,
  "response": "Success message with count",
  "conversation_id": "thread_id",
  "tool_result": "Array of messages"
}
```

## Error Handling
All endpoints return appropriate HTTP status codes and error messages in the response body when applicable:
- 400 Bad Request: Invalid request parameters
- 401 Unauthorized: Missing or invalid authentication
- 404 Not Found: Resource not found
- 500 Internal Server Error: Unexpected server error

## Performance
- Target 95% of requests complete within 5 seconds
- Conversation history limited to 50 messages by default
- Rate limiting applied per user

## Tool Integration
The AI agent has access to the following MCP tools:
- create_conversation: Create new conversations
- get_conversation: Retrieve specific conversation
- get_user_conversations: List user's conversations
- create_message: Add messages to conversation
- get_conversation_messages: Retrieve messages from conversation
- get_conversation_history: Get conversation history with limit