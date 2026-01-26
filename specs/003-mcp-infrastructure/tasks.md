# Implementation Tasks: MCP Infrastructure Foundation

## Phase 1: Setup
- [X] T001 Add FastMCP dependency to requirements.txt using uv
- [X] T002 Create backend/src/models/conversation.py with Conversation SQLModel
- [X] T003 Create backend/src/models/message.py with Message SQLModel

## Phase 2: Foundational
- [X] T004 Create backend/src/services/mcp_server.py with MCP server implementation
- [X] T005 Implement user_id validation utility function in backend/src/services/auth.py

## Phase 3: User Story 1 - AI Agent Access to Task Operations (P1)
- [X] T006 [US1] Register add_task MCP tool in backend/src/services/mcp_server.py
- [X] T007 [US1] Register list_tasks MCP tool in backend/src/services/mcp_server.py
- [X] T008 [US1] Register update_task MCP tool in backend/src/services/mcp_server.py
- [X] T009 [US1] Register complete_task MCP tool in backend/src/services/mcp_server.py
- [X] T010 [US1] Register delete_task MCP tool in backend/src/services/mcp_server.py

## Phase 4: User Story 2 - Persistent Chat History Storage (P2)
- [X] T011 [US2] Implement Conversation CRUD operations in backend/src/services/database.py
- [X] T012 [US2] Implement Message CRUD operations in backend/src/services/database.py
- [X] T013 [US2] Create database migration for Conversation and Message tables

## Phase 5: User Story 3 - Secure Multi-Tenant Isolation (P3)
- [X] T014 [US3] Add user_id validation to all MCP tools for proper isolation
- [ ] T015 [US3] Test user isolation with multiple user scenarios

## Phase 6: Integration & Polish
- [X] T016 Update backend/main.py to start MCP server on daemon thread with lifespan manager
- [X] T017 Test all MCP tools with proper user authentication and isolation
- [X] T018 Document MCP server usage in README