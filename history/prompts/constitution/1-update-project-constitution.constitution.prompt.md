---
id: 1
title: Update Project Constitution
stage: constitution
date: 2026-01-10
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: Claude
command: /sp.constitution
labels: [constitution, setup, governance]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - none
---

## Prompt

```text
AI-Native Full-Stack Todo Web App

## Core Principles
- **Agentic Workflow:** 100% implementation via Claude Code. No manual edits.
- **Spec-First:** Mandatory reading of `/specs` before any code generation.
- **Strict User Isolation:** Task ownership must be verified via JWT on every request.

## Technology Stack
- **Frontend:** Next.js 16+ (App Router, TypeScript, Tailwind)
- **Backend:** Python FastAPI + SQLModel (ORM)
- **Database:** Neon Serverless PostgreSQL
- **Auth:** Better Auth + JWT Plugin

## Key Standards
- **Monorepo Layout:** Separate `/frontend` and `/backend` directories.
- **Security:** Use `.env` files for all secrets (DATABASE_URL, BETTER_AUTH_SECRET).
- **API Convention:** Use `Authorization: Bearer <token>` for all protected routes.
- **Validation:** Use Pydantic models for request/response validation in FastAPI.

## Constraints
- **Zero Hardcoding:** No sensitive data in source code.
- **No Manual Coding:** All logic must be derived from specifications.

## Success Criteria
- Secure multi-user Todo App with persistent Neon DB storage.
- Seamless JWT integration between Better Auth and FastAPI.
- Clean, type-safe, and well-documented code across the stack.
```

## Response snapshot

Created the project constitution file with all the specified principles and requirements. The constitution includes:

Core Principles:
- Agentic Workflow: 100% implementation via Claude Code
- Spec-First Development: Mandatory reading of specs before code generation
- Strict User Isolation: JWT verification on every request
- Zero Hardcoding Policy: No sensitive data in source code
- No Manual Coding Rule: All logic from specifications
- Clean Code Standards: Type-safe and well-documented code

Technology Stack sections covering frontend, backend, database, and authentication requirements.

Development Workflow with monorepo layout, API conventions, and validation standards.

Security Requirements for secret management, API security, and data protection.

Governance section establishing the authority of the constitution.

## Outcome

- ✅ Impact: Created complete project constitution file with all specified principles
- 🧪 Tests: none
- 📁 Files: Updated .specify/memory/constitution.md with comprehensive governance document
- 🔁 Next prompts: Ready to proceed with spec-first development approach
- 🧠 Reflection: Constitution establishes strong foundation for agentic development workflow

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS - All specified principles implemented
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin spec-first development