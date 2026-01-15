# ADR-001: Backend Technology Stack

**Status**: Accepted
**Date**: 2026-01-10

## Context

We need to build a secure FastAPI backend that manages Todo tasks and integrates with a Neon PostgreSQL database. The system requires JWT-based authentication and authorization to ensure strict user isolation. The architecture must follow modern best practices for scalability, security, and maintainability.

## Decision

We will use the following integrated backend technology stack:

- **Language**: Python 3.13+
- **Framework**: FastAPI for web API development
- **ORM**: SQLModel for database operations
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: Better Auth with local JWT verification
- **Dependencies**: psycopg2-binary, python-jose

## Alternatives Considered

1. **Alternative Stack**: Django + Django ORM + PostgreSQL
   - Pros: Mature ecosystem, built-in admin interface, comprehensive framework
   - Cons: Heavier framework, less async support, slower development for API-only applications

2. **Alternative Stack**: Flask + SQLAlchemy + PostgreSQL
   - Pros: Lightweight, flexible, familiar to many developers
   - Cons: Requires more boilerplate code, less automatic documentation, fewer built-in features

3. **Alternative Stack**: Node.js + Express + Prisma + PostgreSQL
   - Pros: JavaScript ecosystem, strong async support, Prisma ORM benefits
   - Cons: Different language than specified, potential type safety concerns

4. **Alternative Stack**: Pure SQLAlchemy instead of SQLModel
   - Pros: More mature, extensive documentation
   - Cons: Requires separate validation layer (Pydantic), more code duplication between models and schemas

## Consequences

**Positive:**
- FastAPI provides automatic OpenAPI documentation and excellent developer experience
- SQLModel reduces code duplication by combining SQLAlchemy and Pydantic
- Neon Serverless PostgreSQL offers scalability and ease of management
- Strong typing support throughout the stack
- Built-in async support for better performance
- Automatic request/response validation

**Negative:**
- FastAPI and SQLModel are relatively newer technologies compared to Django/Flask
- May have fewer third-party integrations than more established frameworks
- Learning curve for team members unfamiliar with FastAPI

## References

- plan.md: Technical Context section
- research.md: Technology Stack Selection decision
- spec.md: Backend Requirements section