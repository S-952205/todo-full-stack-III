# Implementation Plan: MCP Infrastructure Foundation

**Branch**: `003-mcp-infrastructure` | **Date**: 2026-01-26 | **Spec**: [specs/003-mcp-infrastructure/spec.md](../spec.md)
**Input**: Feature specification from `/specs/003-mcp-infrastructure/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of MCP (Model Context Protocol) infrastructure foundation to establish data persistence layer for chat history and create MCP server that exposes task operations as AI-callable tools. This includes implementing Conversation and Message data models, creating an MCP server with FastMCP, and registering 5 task CRUD operations as MCP tools with strict user isolation.

## Technical Context

**Language/Version**: Python 3.13+ (as per constitution and existing backend)
**Primary Dependencies**: FastAPI, SQLModel, FastMCP, Neon PostgreSQL, Better Auth + JWT
**Storage**: Neon Serverless PostgreSQL via SQLModel ORM
**Testing**: pytest for backend testing
**Target Platform**: Linux server (cloud deployment)
**Project Type**: web (existing backend + new MCP integration)
**Performance Goals**: <2 second response time for 95% of MCP tool calls under normal load
**Constraints**: User isolation must be 100% accurate, MCP server must run on background thread with stdio transport
**Scale/Scope**: Support 10k+ users with proper data isolation

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

1. **Agentic Workflow**: ✅ All development tasks executed through Claude Code agents
2. **Spec-First Development**: ✅ Following the feature specification from spec.md
3. **Strict User Isolation**: ✅ All MCP tools will validate user_id to ensure data isolation
4. **Statelessness**: ✅ MCP tools will fetch/store data directly in Neon DB using user_id
5. **MCP Integration**: ✅ All app logic (task CRUD operations) exposed as MCP Tools
6. **Conversation Persistence**: ✅ Every chat turn logged in Conversation and Message tables

## Project Structure

### Documentation (this feature)

```text
specs/003-mcp-infrastructure/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── user.py
│   │   ├── task.py
│   │   ├── conversation.py        # NEW: Conversation model
│   │   └── message.py             # NEW: Message model
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── database.py
│   │   ├── tasks.py
│   │   └── mcp_server.py          # NEW: MCP server implementation
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py
│   │   ├── auth.py
│   │   └── tasks.py
│   └── main.py                   # Updated: lifespan manager for MCP server
├── requirements.txt
├── alembic/
│   └── versions/                 # Database migrations
└── tests/
    ├── __init__.py
    ├── conftest.py
    ├── test_auth.py
    ├── test_tasks.py
    └── test_mcp.py               # NEW: MCP server tests

frontend/
├── src/
│   ├── app/
│   ├── components/
│   ├── lib/
│   └── types/
├── public/
├── package.json
└── tailwind.config.ts
```

**Structure Decision**: Web application structure selected as the feature extends the existing backend with MCP server integration. New Conversation and Message models added to the existing backend/models directory, and mcp_server.py created in services to handle the MCP server implementation.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| MCP Protocol Implementation | Required by feature specification to expose task operations as AI-callable tools | Standard REST APIs don't meet the MCP requirement specified in the feature |
