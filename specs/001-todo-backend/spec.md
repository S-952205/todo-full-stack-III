# Feature Specification: Todo Backend & Database (Phase 1)

**Feature Branch**: `001-todo-backend`
**Created**: 2026-01-10
**Status**: Draft
**Input**: User description: "Specification: Backend & Database (Phase 1)

## 1. Objective
Build a secure FastAPI backend that manages Todo tasks and integrates with a Neon PostgreSQL database using SQLModel.

## 2. Database Schema (Neon PostgreSQL)
We need a `tasks` table with the following fields:
- `id`: Integer (Primary Key)
- `user_id`: String (Indexed) - This will store the Better Auth User ID.
- `title`: String (Required, max 200 chars)
- `description`: Text (Optional)
- `completed`: Boolean (Default: False)
- `created_at`: DateTime (Auto-now)

## 3. API Endpoints (FastAPI)
All endpoints must be under the `/api/v1` prefix.
- `GET /tasks`: Fetch all tasks for the authenticated user.
- `POST /tasks`: Create a new task.
- `GET /tasks/{id}`: Get details of a specific task.
- `PUT /tasks/{id}`: Update task content.
- `PATCH /tasks/{id}/complete`: Toggle completion status.
- `DELETE /tasks/{id}`: Remove a task.

## 4. Security & Authentication (The JWT Bridge)
- **Middleware:** A JWT verification middleware must be implemented.
- **Verification:** Every request must have an `Authorization: Bearer <token>` header.
- **Secret:** Use `BETTER_AUTH_SECRET` from environment variables to verify the JWT signature.
- **Isolation:** The `user_id` extracted from the JWT MUST match the `user_id` in the database query. A user should NEVER be able to see another user's tasks.

## 5. Success Criteria
- [ ] Database connection to Neon is successful.
- [ ] CRUD operations work via Swagger UI (`/docs`).
- [ ] Unauthorized requests (no token) return 401.
- [ ] SQLModel models are correctly mapped to DB tables."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create New Todo Task (Priority: P1)

As an authenticated user, I want to create a new todo task so that I can track my responsibilities and goals.

**Why this priority**: This is the core functionality that enables the entire todo system - without the ability to create tasks, the system has no value.

**Independent Test**: The system can accept new task creation requests with proper authentication and store them in the database, delivering immediate value to users who need to track tasks.

**Acceptance Scenarios**:

1. **Given** user is authenticated with a valid JWT token, **When** user submits a POST request to `/api/v1/tasks` with a title and optional description, **Then** the system creates a new task associated with the user's ID and returns the created task details.

2. **Given** user is not authenticated or has invalid JWT token, **When** user attempts to create a task, **Then** the system returns a 401 Unauthorized response without creating any task.

---

### User Story 2 - View My Todo Tasks (Priority: P1)

As an authenticated user, I want to view all my todo tasks so that I can see what I need to do and track my progress.

**Why this priority**: This is essential for the user to derive value from the system by seeing their created tasks.

**Independent Test**: The system can return a list of tasks belonging to the authenticated user, providing immediate utility for task management.

**Acceptance Scenarios**:

1. **Given** user is authenticated with a valid JWT token, **When** user sends a GET request to `/api/v1/tasks`, **Then** the system returns only the tasks associated with the user's ID.

2. **Given** user is authenticated but has no tasks, **When** user sends a GET request to `/api/v1/tasks`, **Then** the system returns an empty list without errors.

---

### User Story 3 - Update Task Details (Priority: P2)

As an authenticated user, I want to update my task details so that I can modify the content or status of my tasks.

**Why this priority**: This provides flexibility to modify existing tasks without recreating them, improving user experience.

**Independent Test**: The system allows authenticated users to modify their own tasks while preventing unauthorized access to others' tasks.

**Acceptance Scenarios**:

1. **Given** user is authenticated with a valid JWT token, **When** user sends a PUT request to `/api/v1/tasks/{id}` with updated task data, **Then** the system updates only the task that belongs to the user and returns the updated task details.

2. **Given** user is authenticated but attempts to update another user's task, **When** user sends a PUT request to `/api/v1/tasks/{id}`, **Then** the system returns a 403 Forbidden response or 404 Not Found.

---

### User Story 4 - Toggle Task Completion Status (Priority: P2)

As an authenticated user, I want to mark tasks as completed so that I can track my progress and organize my tasks.

**Why this priority**: This is a core functionality for task management that allows users to mark completed work.

**Independent Test**: The system can toggle the completion status of a user's task while maintaining proper authentication and authorization.

**Acceptance Scenarios**:

1. **Given** user is authenticated with a valid JWT token, **When** user sends a PATCH request to `/api/v1/tasks/{id}/complete`, **Then** the system toggles the completion status of the user's task and returns the updated task.

2. **Given** user is authenticated but attempts to update another user's task completion status, **When** user sends a PATCH request to `/api/v1/tasks/{id}/complete`, **Then** the system returns a 403 Forbidden response or 404 Not Found.

---

### User Story 5 - Delete Tasks (Priority: P3)

As an authenticated user, I want to delete tasks that I no longer need so that I can keep my task list organized.

**Why this priority**: This allows users to clean up their task list and remove completed or irrelevant tasks.

**Independent Test**: The system can remove a user's task from the database while preventing unauthorized deletions.

**Acceptance Scenarios**:

1. **Given** user is authenticated with a valid JWT token, **When** user sends a DELETE request to `/api/v1/tasks/{id}`, **Then** the system deletes only the task that belongs to the user and confirms deletion.

2. **Given** user is authenticated but attempts to delete another user's task, **When** user sends a DELETE request to `/api/v1/tasks/{id}`, **Then** the system returns a 403 Forbidden response or 404 Not Found.

---

### Edge Cases

- What happens when a user attempts to access a task ID that doesn't exist?
- How does the system handle malformed JWT tokens?
- What happens when the database connection fails during operations?
- How does the system handle requests with missing required fields (like title)?
- What happens when a user exceeds the character limit for task titles?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST authenticate all API requests using JWT tokens in the Authorization header
- **FR-002**: System MUST verify JWT tokens using the BETTER_AUTH_SECRET from environment variables
- **FR-003**: Users MUST be able to create tasks with a title (max 200 chars), optional description, and default completed status of false
- **FR-004**: System MUST associate each task with the authenticated user's ID from the JWT token
- **FR-005**: Users MUST be able to retrieve all tasks that belong to them via GET /api/v1/tasks
- **FR-006**: Users MUST be able to retrieve a specific task by ID via GET /api/v1/tasks/{id}
- **FR-007**: Users MUST be able to update task details via PUT /api/v1/tasks/{id}
- **FR-008**: Users MUST be able to toggle task completion status via PATCH /api/v1/tasks/{id}/complete
- **FR-009**: Users MUST be able to delete their tasks via DELETE /api/v1/tasks/{id}
- **FR-010**: System MUST enforce user isolation by verifying that the user's ID from JWT matches the task's user_id before allowing access
- **FR-011**: System MUST store tasks in a Neon PostgreSQL database using SQLModel
- **FR-012**: System MUST return appropriate HTTP status codes (200, 201, 401, 403, 404, etc.)

### Key Entities *(include if feature involves data)*

- **Task**: Represents a user's todo item with id, user_id, title, description, completion status, and creation timestamp
- **User**: Identified by user_id from Better Auth JWT, owns zero or more tasks

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Database connection to Neon PostgreSQL is established successfully and remains stable during operation
- **SC-002**: All CRUD operations are accessible and functional through the Swagger UI (/docs) interface
- **SC-003**: Unauthorized requests without valid JWT tokens return HTTP 401 status code consistently
- **SC-004**: SQLModel models are correctly mapped to database tables with proper relationships and constraints
- **SC-005**: Users can only access tasks that belong to their user ID, preventing cross-user data access
- **SC-006**: API endpoints respond within acceptable time limits (under 2 seconds for typical operations)
- **SC-007**: All API endpoints follow the /api/v1 prefix convention as specified