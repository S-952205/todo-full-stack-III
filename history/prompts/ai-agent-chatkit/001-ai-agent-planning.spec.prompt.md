---
id: 001
title: "AI Agent & ChatKit UI Implementation - Planning Phase"
stage: plan
date_iso: "2026-01-28"
surface: "agent"
model: "Haiku 4.5"
feature: "ai-agent-chatkit"
branch: "001-ai-agent-chatkit"
user: "user"
command: "sp.plan"
labels:
  - "planning"
  - "architecture"
  - "api-design"
  - "data-model"
  - "contracts"
links:
  spec: "./spec.md"
  ticket: "null"
  adr: "null"
  pr: "null"
files_yaml: |
  - specs/001-ai-agent-chatkit/plan.md
  - specs/001-ai-agent-chatkit/research.md
  - specs/001-ai-agent-chatkit/data-model.md
  - specs/001-ai-agent-chatkit/quickstart.md
  - specs/001-ai-agent-chatkit/contracts/chat-api.yaml
tests_yaml: |
  - "Architecture design review"
  - "Data model validation"
  - "API contract verification"
---

# AI Agent & ChatKit UI Implementation - Planning Phase

## Original Prompt

```
AI Agent & ChatKit UI

## 1. Architecture Sketch
A stateless request-response flow:
* **UI**: ChatKit (Next.js) sends prompt + `conversation_id`.
* **Agent Service**: FastAPI initializes **OpenAI Agents SDK** runner with **OpenRouter** as the provider.
* **Execution**: Agent fetches DB history → Calls MCP Tools → Saves response → Returns JSON.



## 2. Implementation Steps

### **Step 1: Agent & OpenRouter (Backend)**
* Configure the OpenAI client in `agent.py` to point to OpenRouter.
* Define the `Agent` using the **OpenAI Agents SDK**, passing MCP tools into the `tools` parameter.
* Implement the logic to fetch the last 10-15 messages from the `Message` table for context.

### **Step 2: Chat API**
* Create `POST /api/chat` to receive user messages.
* Logic: Save User Message → Run Agent → Save Assistant Response → Return JSON.

### **Step 3: ChatKit UI (Frontend)**
* Build the `ChatWindow` and `MessageInput` using Tailwind CSS.
* Integrate with the backend API, passing the JWT token in the Autho
```

## Response Summary

Successfully completed the planning phase for the AI Agent & ChatKit UI Implementation feature. The following artifacts were created:

1. **Implementation Plan** (plan.md): Comprehensive architecture and technical approach for implementing the AI agent with OpenAI Agents SDK connected to OpenRouter, featuring a stateless request-response flow with Next.js ChatKit UI frontend and FastAPI backend.

2. **Research Document** (research.md): Detailed research findings on technology decisions including OpenAI Agents SDK integration with OpenRouter, state management architecture, authentication strategy, database schema design, error handling, and frontend architecture.

3. **Data Model** (data-model.md): Complete database schema definition with three main entities: Conversation (storing conversation metadata), Message (individual communications), and Tool Invocation (tracking tool calls). Includes proper relationships, validation rules, and PostgreSQL schema.

4. **Quickstart Guide** (quickstart.md): Step-by-step setup instructions for both backend and frontend components, including environment configuration, dependencies installation, and running the application.

5. **API Contracts** (contracts/chat-api.yaml): Detailed API specification with endpoints for chat functionality, conversation management, and tool invocation, including request/response schemas and error handling.

All artifacts align with the constitutional principles of the project, ensuring agentic workflow, spec-first development, strict user isolation, statelessness, MCP integration, conversation persistence, and zero hardcoding.

## Outcome

The planning phase is complete with all required artifacts created. The implementation can now proceed based on these specifications, with clear guidance on architecture, data models, API contracts, and setup procedures. The next phase would be task breakdown and implementation.