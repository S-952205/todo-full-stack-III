# ADR-003: Project Structure

**Status**: Accepted
**Date**: 2026-01-10

## Context

The backend needs to be organized in a way that promotes maintainability, separation of concerns, and scalability. The architecture must accommodate models, database connection logic, authentication, and route handlers while following established patterns for Python web applications.

## Decision

We will organize the backend with separate modules following a modular architecture:

```
backend/
├── main.py                 # Application entry point and middleware
├── models.py               # Database tables and schemas
├── db.py                   # Neon database connection logic
├── auth.py                 # JWT verification logic
├── routes/
│   └── tasks.py            # Task CRUD handlers
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variables template
└── tests/
    ├── conftest.py
    ├── test_auth.py
    └── test_tasks.py
```

This structure separates concerns into distinct modules while maintaining simplicity for the initial implementation.

## Alternatives Considered

1. **Package-based Structure**: Separate each concern into its own package with multiple modules
   - Pros: Better organization for larger applications, clearer separation of concerns
   - Cons: More complex for initial development, potential over-engineering for this scope

2. **Domain-driven Structure**: Organize by business domain (e.g., task management domain)
   - Pros: Better alignment with business logic, easier to reason about functionality
   - Cons: More complex initial setup, may be overkill for simple todo application

3. **Layered Architecture**: Separate into presentation, business logic, and data access layers across packages
   - Pros: Clear separation of architectural layers, good for complex business logic
   - Cons: More complex file navigation, potential over-engineering for this scope

## Consequences

**Positive:**
- Clear separation of concerns making the codebase easier to understand and maintain
- Simplified initial development with minimal directory nesting
- Follows common Python/FastAPI project organization patterns
- Easy to add new route handlers in the routes/ directory
- Clear location for database models and connection logic

**Negative:**
- May become unwieldy as the application grows (can be refactored later)
- Some code duplication possible between modules
- May require restructuring as complexity increases

## References

- plan.md: Project Structure section
- research.md: Project Structure decision
- spec.md: API Endpoints section