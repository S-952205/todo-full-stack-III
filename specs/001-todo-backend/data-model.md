# Data Model: Todo Backend & Database (Phase 1)

## Task Entity

### Fields
- `id`: Integer (Primary Key, Auto-increment)
- `user_id`: String (Indexed, Required) - Stores the Better Auth User ID
- `title`: String (Required, Max 200 characters)
- `description`: Text (Optional)
- `completed`: Boolean (Default: False)
- `created_at`: DateTime (Auto-populated with current timestamp)

### Relationships
- The `user_id` field creates a logical relationship with Better Auth users
- Each task belongs to exactly one user
- A user can own zero or more tasks

### Validation Rules
- `title` must be between 1 and 200 characters
- `user_id` must be a valid string (as provided by Better Auth)
- `completed` defaults to False when creating new tasks
- `created_at` is automatically set to the current time when creating tasks

### State Transitions
- `completed` field can transition from False to True or True to False via PATCH requests
- All other fields can be modified via PUT requests (except id and created_at which are immutable)

## API Request/Response Models

### TaskCreate
- `title`: String (Required, Max 200 characters)
- `description`: Text (Optional)
- `completed`: Boolean (Optional, Default: False)

### TaskUpdate
- `title`: String (Optional, Max 200 characters)
- `description`: Text (Optional)
- `completed`: Boolean (Optional)

### TaskResponse
- `id`: Integer (Read-only)
- `user_id`: String (Read-only, for internal validation)
- `title`: String
- `description`: Text (Optional)
- `completed`: Boolean
- `created_at`: DateTime