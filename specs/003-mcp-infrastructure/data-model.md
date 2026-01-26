# Data Model: MCP Infrastructure Foundation

## Entity: Conversation

Represents a logical grouping of messages between a user and an AI agent.

### Fields
- `id`: UUID (Primary Key) - Unique identifier for the conversation
- `title`: String - Descriptive title for the conversation
- `user_id`: UUID (Foreign Key) - Reference to the user who owns this conversation
- `created_at`: DateTime - Timestamp when the conversation was initiated
- `updated_at`: DateTime - Timestamp when the conversation was last modified
- `is_active`: Boolean - Flag indicating if the conversation is currently active

### Relationships
- One-to-Many: A conversation has many messages
- Many-to-One: A conversation belongs to one user

## Entity: Message

Represents an individual message within a conversation.

### Fields
- `id`: UUID (Primary Key) - Unique identifier for the message
- `conversation_id`: UUID (Foreign Key) - Reference to the conversation this message belongs to
- `role`: String (Enum: "user", "assistant", "system") - Defines the sender type
- `content`: Text - The actual content of the message
- `timestamp`: DateTime - When the message was sent/received
- `metadata`: JSON - Additional metadata about the message (optional)

### Relationships
- Many-to-One: A message belongs to one conversation
- Many-to-One: A message belongs to one user (through conversation)

## Entity: Task (Existing)

Represents a user's task with additional user isolation.

### Fields
- `id`: UUID (Primary Key) - Unique identifier for the task
- `title`: String - Title of the task
- `description`: Text - Detailed description of the task (optional)
- `is_completed`: Boolean - Status of the task
- `user_id`: UUID (Foreign Key) - Reference to the user who owns this task
- `created_at`: DateTime - When the task was created
- `updated_at`: DateTime - When the task was last updated

### Relationships
- Many-to-One: A task belongs to one user
- One-to-Many: A user has many tasks

## Validation Rules

1. **User Isolation**: All entities must validate that the requesting user has access rights
2. **Required Fields**:
   - Conversation: user_id, title
   - Message: conversation_id, role, content
   - Task: user_id, title
3. **Role Validation**: Message roles must be one of "user", "assistant", or "system"
4. **Ownership Verification**: All operations must verify user_id matches the authenticated user

## Indexes

- Conversation.user_id: For efficient user-based queries
- Message.conversation_id: For efficient conversation-based queries
- Message.timestamp: For chronological ordering
- Task.user_id: For efficient user-based queries