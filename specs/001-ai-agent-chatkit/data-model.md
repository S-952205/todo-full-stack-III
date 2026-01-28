# Data Model: AI Agent & ChatKit UI Implementation

## Overview
This document defines the database schema and data relationships for the AI Agent & ChatKit UI feature, based on the key entities identified in the specification.

## Entity Definitions

### Conversation
Represents a series of interactions between user and AI agent, containing messages and metadata.

**Fields**:
- `id`: UUID (Primary Key) - Unique identifier for the conversation
- `user_id`: UUID (Foreign Key) - Reference to the user who owns this conversation
- `title`: String (255 chars) - Auto-generated title based on conversation content
- `created_at`: DateTime - Timestamp when conversation was created
- `updated_at`: DateTime - Timestamp when conversation was last updated
- `status`: Enum (active, archived, deleted) - Current state of the conversation

**Relationships**:
- One-to-many with Message (one conversation has many messages)
- Belongs to User (one user owns many conversations)

**Validation Rules**:
- `user_id` must reference an existing user
- `title` must not be empty
- `status` must be one of the allowed enum values

### Message
Individual communication in the conversation, either from user or AI agent.

**Fields**:
- `id`: UUID (Primary Key) - Unique identifier for the message
- `conversation_id`: UUID (Foreign Key) - Reference to the conversation this message belongs to
- `user_id`: UUID (Foreign Key) - Reference to the user who sent this message
- `role`: Enum (user, assistant) - Specifies whether message is from user or AI assistant
- `content`: Text - The actual message content
- `timestamp`: DateTime - When the message was sent
- `tool_calls`: JSON (optional) - Details of any tools called during this message
- `tool_responses`: JSON (optional) - Responses from tools called

**Relationships**:
- Belongs to Conversation (many messages belong to one conversation)
- Belongs to User (messages are associated with the sending user)

**Validation Rules**:
- `conversation_id` must reference an existing conversation
- `user_id` must reference an existing user
- `role` must be either 'user' or 'assistant'
- `content` must not be empty
- `timestamp` must not be in the future

### Tool Invocation
Request to execute a specific MCP tool with parameters extracted from user intent.

**Fields**:
- `id`: UUID (Primary Key) - Unique identifier for the tool invocation
- `message_id`: UUID (Foreign Key) - Reference to the message that triggered this tool call
- `tool_name`: String (255 chars) - Name of the tool being invoked
- `parameters`: JSON - Parameters passed to the tool
- `status`: Enum (pending, success, failed) - Execution status
- `result`: Text (optional) - Result of the tool execution
- `created_at`: DateTime - When the tool invocation was initiated
- `completed_at`: DateTime (optional) - When the tool invocation completed

**Relationships**:
- Belongs to Message (one message can trigger many tool invocations)

**Validation Rules**:
- `message_id` must reference an existing message
- `tool_name` must not be empty
- `status` must be one of the allowed enum values

## Database Schema (SQLModel)

```sql
-- Conversation table
CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    title VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    status VARCHAR(20) DEFAULT 'active' NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Messages table
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID NOT NULL,
    user_id UUID NOT NULL,
    role VARCHAR(20) NOT NULL,
    content TEXT NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    tool_calls JSONB,
    tool_responses JSONB,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Tool invocations table
CREATE TABLE tool_invocations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    message_id UUID NOT NULL,
    tool_name VARCHAR(255) NOT NULL,
    parameters JSONB,
    status VARCHAR(20) NOT NULL,
    result TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    completed_at TIMESTAMP WITH TIME ZONE,
    FOREIGN KEY (message_id) REFERENCES messages(id)
);
```

## Indexes
- Index on `conversations.user_id` for efficient user-based queries
- Index on `messages.conversation_id` for efficient conversation history retrieval
- Index on `messages.timestamp` for chronological ordering
- Composite index on `tool_invocations.message_id` and `tool_invocations.status` for monitoring tool execution

## Constraints
- Referential integrity enforced through foreign key constraints
- User data isolation ensured by requiring `user_id` for all records
- Audit trail maintained through timestamps
- Conversation context preserved through proper relationships