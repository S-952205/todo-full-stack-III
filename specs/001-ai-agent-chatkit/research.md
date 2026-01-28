# Research: AI Agent & ChatKit UI Implementation

## Overview
This document captures research findings for implementing the AI Agent & ChatKit UI feature, addressing unknowns and technology decisions identified during planning.

## Decisions & Rationale

### 1. OpenAI Agents SDK with OpenRouter Integration
**Decision**: Use OpenAI's Assistants API (via OpenAI Agents SDK) with OpenRouter as the provider
**Rationale**:
- OpenRouter provides access to multiple free models that satisfy the constraint of using free models
- The Assistants API provides built-in tool calling capabilities needed for MCP tool integration
- OpenAI's ecosystem offers strong support for conversation history management
**Alternatives considered**:
- Direct OpenAI API calls: Less convenient for tool integration
- Alternative agent frameworks: Would require more custom development

### 2. State Management Architecture
**Decision**: Stateless request-response flow with database-stored conversation history
**Rationale**:
- Aligns with constitutional principle of statelessness
- Ensures scalability and reliability across distributed deployments
- Allows for proper conversation persistence and auditability
**Alternatives considered**:
- Server-side session state: Would violate constitutional principles
- Client-side storage only: Would compromise conversation continuity

### 3. Authentication Strategy
**Decision**: JWT-based authentication with Better Auth
**Rationale**:
- Aligns with constitutional principle of strict user isolation
- Better Auth provides robust authentication with minimal setup
- JWT tokens can be easily passed between frontend and backend
**Alternatives considered**:
- Session-based authentication: Would require server-side state storage
- Custom auth system: Would be more complex and potentially less secure

### 4. Database Schema Design
**Decision**: Two-table design with Conversation and Message entities
**Rationale**:
- Simple yet effective for storing conversation history
- Enables proper user isolation through user_id foreign keys
- Supports the constitutional requirement for conversation persistence
**Alternatives considered**:
- Single table with denormalized data: Would complicate querying
- More complex schema: Would add unnecessary complexity for this use case

### 5. Error Handling Strategy
**Decision**: Exponential backoff with user notification for external service failures
**Rationale**:
- Provides resilience against intermittent API failures
- Keeps users informed about the status of their requests
- Follows best practices for handling external dependencies
**Alternatives considered**:
- Immediate failure: Would provide poor user experience
- Silent retries: Would hide potential problems from users

### 6. Frontend Architecture
**Decision**: Next.js 16+ with ChatKit UI components
**Rationale**:
- Next.js provides excellent server-side rendering capabilities
- Built-in API routes simplify backend integration
- Strong TypeScript support improves development experience
- ChatKit UI provides a solid foundation for chat interface
**Alternatives considered**:
- Pure React SPA: Would require additional backend setup
- Other frameworks: Would not align with constitutional requirements

## Implementation Considerations

### MCP Tool Integration
- MCP tools need to be properly formatted for OpenAI's Assistants API
- Each tool should have clear input/output schemas
- Proper error handling within tools to maintain user experience

### Performance Optimization
- Consider caching strategies for frequently accessed data
- Optimize database queries for conversation history retrieval
- Implement proper loading states in UI during agent processing

### Security Measures
- Validate and sanitize all user inputs
- Ensure proper authentication on all API endpoints
- Implement rate limiting to prevent abuse