# Implementation Plan: AI Agent & ChatKit UI

**Branch**: `001-ai-agent-chatkit` | **Date**: 2026-01-28 | **Spec**: [AI Agent & ChatKit UI Implementation](./spec.md)
**Input**: Feature specification from `/specs/001-ai-agent-chatkit/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of an AI Agent using OpenAI Agents SDK connected to OpenRouter free models with a ChatKit UI in Next.js. The system follows a stateless request-response flow where the UI sends prompts with conversation_id to a FastAPI backend that initializes the OpenAI Agent runner with OpenRouter as the provider. The agent fetches DB history, calls MCP tools, saves responses, and returns JSON. Includes individual user authentication with data isolation and conversation persistence.

## Technical Context

**Language/Version**: Python 3.13+ (backend), TypeScript 5.0+/JavaScript ES2022 (frontend)
**Primary Dependencies**: FastAPI, OpenAI Agents SDK, OpenRouter API, Next.js 16+, Better Auth, Neon Serverless PostgreSQL
**Storage**: Neon Serverless PostgreSQL (SQLModel ORM)
**Testing**: pytest (backend), Jest/React Testing Library (frontend)
**Target Platform**: Web application (server-side rendering + client-side interactivity)
**Project Type**: Web application (frontend + backend)
**Performance Goals**: 95% of requests complete within 5 seconds, support for 1000+ concurrent users
**Constraints**: Use free models from OpenRouter, maintain stateless operation, ensure user data isolation
**Scale/Scope**: Support 10k+ users with indefinite conversation retention

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- ✅ Agentic Workflow: Implementation will be executed via Claude Code agents and tools
- ✅ Spec-First Development: Following the documented specifications with clear acceptance criteria
- ✅ Strict User Isolation: Task & Chat ownership will be verified via JWT/user_id on every request
- ✅ Statelessness: Servers will hold no session state; all context will persist in Neon DB
- ✅ MCP Integration: All app logic (CRUD) will be exposed as MCP Tools
- ✅ Conversation Persistence: Every chat turn will be logged in Conversation and Message tables
- ✅ Zero Hardcoding: Secrets (OPENROUTER_API_KEY, DATABASE_URL) will be stored in .env

## Project Structure

### Documentation (this feature)

```text
specs/001-ai-agent-chatkit/
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
│   │   ├── conversation.py
│   │   └── message.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── agent_service.py
│   │   ├── db_service.py
│   │   └── openrouter_service.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── chat_api.py
│   ├── tools/
│   │   ├── __init__.py
│   │   └── mcp_tools.py
│   └── main.py
└── tests/
    ├── unit/
    ├── integration/
    └── contract/

frontend/
├── src/
│   ├── components/
│   │   ├── ChatWindow.tsx
│   │   ├── MessageInput.tsx
│   │   └── StatusIndicator.tsx
│   ├── pages/
│   │   └── chat.tsx
│   ├── services/
│   │   └── apiService.ts
│   ├── utils/
│   │   └── authUtils.ts
│   └── types/
│       └── chatTypes.ts
├── public/
└── tests/
    ├── unit/
    └── integration/
```

**Structure Decision**: Web application with separate backend (FastAPI) and frontend (Next.js) following the architecture sketch provided. The backend handles the AI agent logic and database operations, while the frontend provides the ChatKit UI experience with proper authentication and status indicators.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [None] | [No violations identified] | [All constitutional principles satisfied] |
