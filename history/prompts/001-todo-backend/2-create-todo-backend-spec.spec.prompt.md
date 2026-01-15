---
id: 2
title: Create Todo Backend Spec
stage: spec
date: 2026-01-10
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-todo-backend
branch: 001-todo-backend
user: Claude
command: /sp.specify
labels: [spec, backend, database, todo]
links:
  spec: specs/001-todo-backend/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-todo-backend/spec.md
  - specs/001-todo-backend/checklists/requirements.md
tests:
  - none
---

## Prompt

```text
Specification: Backend & Database (Phase 1)

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
- [ ] SQLModel models are correctly mapped to DB tables.
```

## Response snapshot

Created comprehensive specification for the Todo Backend & Database feature. The spec includes:

- User Stories prioritized by importance (P1-P3) covering core functionality: creating tasks, viewing tasks, updating tasks, toggling completion status, and deleting tasks
- Detailed acceptance scenarios for each user story with Given/When/Then format
- Identification of key edge cases such as unauthorized access attempts and malformed requests
- 12 functional requirements (FR-001 to FR-012) covering authentication, authorization, CRUD operations, and data integrity
- Two key entities (Task and User) with their relationships
- 7 measurable success criteria (SC-001 to SC-007) focusing on database connectivity, API functionality, security, and performance

Also created a quality checklist to validate the specification completeness.

## Outcome

- ✅ Impact: Complete specification created with all required sections and user scenarios
- 🧪 Tests: none
- 📁 Files: Created spec.md and requirements checklist in specs/001-todo-backend/
- 🔁 Next prompts: Ready to proceed with planning phase using /sp.plan
- 🧠 Reflection: Specification follows constitutional principles with clear user isolation and security requirements

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS - All specification requirements met
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed with implementation planning