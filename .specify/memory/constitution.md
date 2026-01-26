<!-- SYNC IMPACT REPORT
Version change: 1.0.0 -> 1.1.0
Modified principles: Agentic Workflow (updated), Spec-First Development (updated), Strict User Isolation (expanded), Statelessness (added)
Added sections: Statelessness principle, Conversation Persistence requirement
Removed sections: Zero Hardcoding Policy, No Manual Coding Rule, Clean Code Standards (merged into other principles)
Templates requiring updates: ⚠ pending
- .specify/templates/plan-template.md: Needs alignment with new principles
- .specify/templates/spec-template.md: Needs alignment with new constraints
- .specify/templates/tasks-template.md: Needs alignment with new workflow
Follow-up TODOs: None
-->
# AI-Native Full-Stack Todo Web App Constitution (v1.1.0)

## Core Principles

### Agentic Workflow
100% implementation via Claude Code. No manual edits. All development tasks must be executed through Claude Code agents and tools.

### Spec-First Development
Mandatory reading of `/specs` before generation. All implementation work must be based on documented specifications with clear acceptance criteria.

### Strict User Isolation
Task & Chat ownership verified via JWT/user_id on every request. No data leakage between users is acceptable under any circumstances.

### Statelessness
Servers must hold no session state; all context must persist in Neon DB. This ensures scalability and reliability across distributed deployments.

## Technology Stack

### Frontend
Next.js 16+ (App Router), OpenAI ChatKit UI. All frontend components must leverage modern Next.js features with proper TypeScript typing and responsive Tailwind styling.

### Backend
Python FastAPI, OpenAI Agents SDK, Official MCP SDK. All backend services must use FastAPI for API creation with proper request/response validation and error handling.

### Database
Neon Serverless PostgreSQL (SQLModel ORM). All data persistence must use Neon's serverless PostgreSQL with proper connection pooling and transaction management.

### Auth
Better Auth + JWT. All authentication must be handled through Better Auth with JWT tokens for secure API communication.

## Development Workflow

### MCP Integration
All app logic (CRUD) must be exposed as MCP Tools. This enables programmatic access to all core functionality through standardized interfaces.

### Conversation Persistence
Every chat turn must be logged in `Conversation` and `Message` tables. This ensures auditability and continuity of user interactions.

### Zero Hardcoding
Secrets (OPENAI_API_KEY, DATABASE_URL) strictly in `.env`. No sensitive data in source code. All secrets must be stored in `.env` files and accessed through environment variables.

## Governance

All implementations must adhere to these constitutional principles. Any deviation from these principles requires explicit approval and documentation of the exception. The constitution serves as the ultimate authority for development practices in this project.

Amendments to this constitution must be documented with clear justification and approved by project stakeholders before implementation. All team members must acknowledge and comply with these principles before contributing to the project.

All PRs and reviews must verify constitutional compliance. Code that violates these principles will not be accepted.

**Version**: 1.1.0 | **Last Amended**: 2026-01-26