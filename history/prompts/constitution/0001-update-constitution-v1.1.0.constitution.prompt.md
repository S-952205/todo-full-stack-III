---
id: 1
title: Update constitution v1.1.0
stage: constitution
date: 2026-01-26
surface: agent
model: claude-haiku-4-5-20251001
feature: none
branch: main
user: Syed Sufyan
command: /sp.phr
labels: ["constitution", "governance", "policy"]
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

update existing constitution with this # AI-Native Full-Stack Todo Web App Constitution (v1.1.0)

## Core Principles
- **Agentic Workflow:** 100% implementation via Claude Code. No manual edits.
- **Spec-First Development:** Mandatory reading of `/specs` before generation.
- **Strict User Isolation:** Task & Chat ownership verified via JWT/user_id on every request.
- **Statelessness:** Servers must hold no session state; all context must persist in Neon DB.

## Technology Stack
- **Frontend:** Next.js 16+ (App Router), OpenAI ChatKit UI.
- **Backend:** Python FastAPI, OpenAI Agents SDK, Official MCP SDK.
- **Database:** Neon Serverless PostgreSQL (SQLModel ORM).
- **Auth:** Better Auth + JWT.

## Development Workflow
- **MCP Integration:** All app logic (CRUD) must be exposed as MCP Tools.
- **Conversation Persistence:** Every chat turn must be logged in `Conversation` and `Message` tables.
- **Zero Hardcoding:** Secrets (OPENAI_API_KEY, DATABASE_URL) strictly in `.env`.

**Version**: 1.1.0 | **Last Amended**: 2026-01-26

## Response snapshot

Updated the constitution file with the new content, including the new Statelessness principle and Conversation Persistence requirement, and updated the version to 1.1.0.

## Outcome

- ✅ Impact: Constitution updated to v1.1.0 with new principles and requirements
- 🧪 Tests: none
- 📁 Files: .specify/memory/constitution.md
- 🔁 Next prompts: none
- 🧠 Reflection: The constitution now includes important statelessness and MCP integration requirements

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A