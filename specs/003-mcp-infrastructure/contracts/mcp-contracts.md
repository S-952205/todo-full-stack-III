# API Contracts: MCP Infrastructure Foundation

## MCP Tool Contracts

### add_task
- **Purpose**: Create a new task for the authenticated user
- **Input Parameters**:
  - `title` (string, required): Title of the task
  - `description` (string, optional): Detailed description of the task
  - `user_id` (UUID, required): ID of the user creating the task
- **Output**: Task object with ID, title, description, completion status, timestamps
- **Error Conditions**: Invalid user_id, missing required fields, database errors

### list_tasks
- **Purpose**: Retrieve all tasks for the authenticated user
- **Input Parameters**:
  - `user_id` (UUID, required): ID of the user whose tasks to retrieve
- **Output**: Array of Task objects
- **Error Conditions**: Invalid user_id, database errors

### update_task
- **Purpose**: Modify an existing task
- **Input Parameters**:
  - `task_id` (UUID, required): ID of the task to update
  - `user_id` (UUID, required): ID of the user requesting the update
  - `title` (string, optional): New title for the task
  - `description` (string, optional): New description for the task
- **Output**: Updated Task object
- **Error Conditions**: Invalid user_id/task_id, user not authorized to modify task, database errors

### complete_task
- **Purpose**: Mark a task as completed
- **Input Parameters**:
  - `task_id` (UUID, required): ID of the task to mark as completed
  - `user_id` (UUID, required): ID of the user requesting the update
  - `completed` (boolean, required): True to mark as completed, False to unmark
- **Output**: Updated Task object
- **Error Conditions**: Invalid user_id/task_id, user not authorized to modify task, database errors

### delete_task
- **Purpose**: Remove a task
- **Input Parameters**:
  - `task_id` (UUID, required): ID of the task to delete
  - `user_id` (UUID, required): ID of the user requesting the deletion
- **Output**: Confirmation of deletion
- **Error Conditions**: Invalid user_id/task_id, user not authorized to delete task, database errors

## Data Models

### Task
- `id` (UUID): Unique identifier
- `title` (string): Task title
- `description` (string): Task description
- `is_completed` (boolean): Completion status
- `user_id` (UUID): Owner of the task
- `created_at` (datetime): Creation timestamp
- `updated_at` (datetime): Last update timestamp

### Conversation
- `id` (UUID): Unique identifier
- `title` (string): Conversation title
- `user_id` (UUID): Owner of the conversation
- `created_at` (datetime): Creation timestamp
- `updated_at` (datetime): Last update timestamp
- `is_active` (boolean): Active status

### Message
- `id` (UUID): Unique identifier
- `conversation_id` (UUID): Associated conversation
- `role` (string): Sender type ("user", "assistant", "system")
- `content` (string): Message content
- `timestamp` (datetime): When message was sent
- `metadata` (JSON): Additional metadata