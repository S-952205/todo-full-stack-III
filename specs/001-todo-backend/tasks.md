# Task Implementation Plan: Todo Backend & Database (Phase 1)

**Feature**: `001-todo-backend` | **Date**: 2026-01-11 | **Spec**: spec.md | **Plan**: plan.md

## Overview
Implementation plan for a secure FastAPI backend that manages Todo tasks and integrates with a Neon PostgreSQL database using SQLModel. The implementation includes JWT-based authentication and authorization to ensure strict user isolation.

## Dependencies
- Python 3.13+
- FastAPI
- SQLModel
- psycopg2-binary
- python-jose
- Better Auth
- Neon Serverless PostgreSQL

---

## Phase 1: Setup & Project Initialization

- [X] T001 Create project directory structure in backend/
- [X] T002 Initialize requirements.txt with Python dependencies (FastAPI, SQLModel, psycopg2-binary, python-jose)
- [X] T003 Create .env.example file with DATABASE_URL and BETTER_AUTH_SECRET placeholders
- [X] T004 Set up basic project configuration and environment variable loading
- [X] T005 Create initial test directory structure (backend/tests/)

## Phase 2: Foundational Components

- [X] T006 [P] Create database connection module (backend/db.py) with Neon PostgreSQL integration
- [X] T007 [P] Create SQLModel models for Task entity (backend/models.py) with all required fields
- [X] T008 [P] Create JWT authentication module (backend/auth.py) with token verification logic
- [X] T009 Set up main application entry point (backend/main.py) with middleware configuration
- [X] T010 Configure CORS settings and API versioning for /api/v1 prefix

## Phase 3: [US1] User Story 1 - Create New Todo Task (Priority: P1)

**Goal**: Enable authenticated users to create new todo tasks and store them in the database.

**Independent Test Criteria**: The system can accept new task creation requests with proper authentication and store them in the database, delivering immediate value to users who need to track tasks.

**Tasks**:

- [X] T011 [P] [US1] Define TaskCreate Pydantic model for POST request body validation
- [X] T012 [P] [US1] Define TaskResponse Pydantic model for response validation
- [X] T013 [US1] Implement POST /api/v1/tasks endpoint with JWT verification
- [X] T014 [US1] Add task creation logic with user_id extraction from JWT
- [X] T015 [US1] Validate title length (max 200 chars) and required fields
- [X] T016 [US1] Test POST /api/v1/tasks endpoint with valid JWT and task data
- [X] T017 [US1] Test POST /api/v1/tasks endpoint with invalid/missing JWT (should return 401)

## Phase 4: [US2] User Story 2 - View My Todo Tasks (Priority: P1)

**Goal**: Allow authenticated users to view all their own todo tasks.

**Independent Test Criteria**: The system can return a list of tasks belonging to the authenticated user, providing immediate utility for task management.

**Tasks**:

- [X] T018 [P] [US2] Implement GET /api/v1/tasks endpoint with JWT verification
- [X] T019 [US2] Add user_id filtering to ensure users only see their own tasks
- [X] T020 [US2] Return properly formatted list of TaskResponse objects
- [X] T021 [US2] Handle case where user has no tasks (return empty list)
- [X] T022 [US2] Test GET /api/v1/tasks with valid JWT (should return user's tasks)
- [X] T023 [US2] Test GET /api/v1/tasks with invalid/missing JWT (should return 401)

## Phase 5: [US3] User Story 3 - Update Task Details (Priority: P2)

**Goal**: Allow authenticated users to update their own task details while preventing access to others' tasks.

**Independent Test Criteria**: The system allows authenticated users to modify their own tasks while preventing unauthorized access to others' tasks.

**Tasks**:

- [X] T024 [P] [US3] Define TaskUpdate Pydantic model for PUT request body validation
- [X] T025 [US3] Implement GET /api/v1/tasks/{id} endpoint with user isolation
- [X] T026 [US3] Implement PUT /api/v1/tasks/{id} endpoint with user verification
- [X] T027 [US3] Add logic to verify task belongs to authenticated user before update
- [X] T028 [US3] Update task fields while preserving immutable fields (id, created_at)
- [X] T029 [US3] Test GET /api/v1/tasks/{id} with valid JWT and owned task
- [X] T030 [US3] Test GET /api/v1/tasks/{id} with valid JWT and other user's task (should return 403/404)
- [X] T031 [US3] Test PUT /api/v1/tasks/{id} with valid JWT and owned task
- [X] T032 [US3] Test PUT /api/v1/tasks/{id} with valid JWT and other user's task (should return 403/404)

## Phase 6: [US4] User Story 4 - Toggle Task Completion Status (Priority: P2)

**Goal**: Allow authenticated users to toggle the completion status of their own tasks.

**Independent Test Criteria**: The system can toggle the completion status of a user's task while maintaining proper authentication and authorization.

**Tasks**:

- [X] T033 [US4] Implement PATCH /api/v1/tasks/{id}/complete endpoint with user verification
- [X] T034 [US4] Add logic to toggle completion status of the task
- [X] T035 [US4] Verify task belongs to authenticated user before toggling
- [X] T036 [US4] Return updated task with new completion status
- [X] T037 [US4] Test PATCH /api/v1/tasks/{id}/complete with valid JWT and owned task
- [X] T038 [US4] Test PATCH /api/v1/tasks/{id}/complete with valid JWT and other user's task (should return 403/404)

## Phase 7: [US5] User Story 5 - Delete Tasks (Priority: P3)

**Goal**: Allow authenticated users to delete their own tasks while preventing deletion of others' tasks.

**Independent Test Criteria**: The system can remove a user's task from the database while preventing unauthorized deletions.

**Tasks**:

- [X] T039 [US5] Implement DELETE /api/v1/tasks/{id} endpoint with user verification
- [X] T040 [US5] Add logic to verify task belongs to authenticated user before deletion
- [X] T041 [US5] Delete task from database and return 204 No Content
- [X] T042 [US5] Test DELETE /api/v1/tasks/{id} with valid JWT and owned task
- [X] T043 [US5] Test DELETE /api/v1/tasks/{id} with valid JWT and other user's task (should return 403/404)

## Phase 8: Polish & Cross-Cutting Concerns

- [X] T044 Add comprehensive error handling with proper HTTP status codes
- [X] T045 Implement validation for all request bodies and path parameters
- [X] T046 Add logging for authentication failures and important operations
- [X] T047 Create integration tests covering all user stories
- [X] T048 Add input sanitization and security measures
- [X] T049 Document all endpoints with proper OpenAPI/Swagger annotations
- [X] T050 Run all tests to ensure everything works together
- [X] T051 Perform final integration test with all endpoints working together

---

## Dependencies Between User Stories

1. **US2 depends on US1**: Need to be able to create tasks before viewing them
2. **US3 depends on US1**: Need to have tasks created to update them
3. **US4 depends on US1**: Need to have tasks created to toggle completion
4. **US5 depends on US1**: Need to have tasks created to delete them

## Parallel Execution Opportunities

- Tasks T006-T008 can run in parallel (foundational components)
- Tasks T011-T012 can run in parallel with T018 (models and endpoints)
- Tasks T024 can run in parallel with other US3 tasks
- Tasks within different user stories can run in parallel if they don't share components

## Implementation Strategy

1. **MVP Scope**: Complete Phase 1 (Setup), Phase 2 (Foundational), and Phase 3 (US1 - Create Tasks) for minimal viable product
2. **Incremental Delivery**: After MVP, implement US2 (View tasks), then US3-US5 in priority order
3. **Testing**: Each user story should be independently testable before moving to the next
4. **Security First**: Ensure JWT authentication and user isolation are working before feature completion

## Success Criteria

- [ ] Database connection to Neon is successful
- [ ] CRUD operations work via Swagger UI (/docs)
- [ ] Unauthorized requests (no token) return 401
- [ ] SQLModel models are correctly mapped to DB tables
- [ ] Users can only access tasks that belong to their user ID
- [ ] All API endpoints follow the /api/v1 prefix convention
- [ ] All endpoints require valid JWT tokens for access
- [ ] Proper error responses are returned for invalid requests