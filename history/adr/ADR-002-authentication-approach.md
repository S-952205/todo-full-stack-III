# ADR-002: Authentication Approach

**Status**: Accepted
**Date**: 2026-01-10

## Context

The system requires JWT-based authentication and authorization to ensure strict user isolation. Every request must be authenticated using JWT tokens in the Authorization header. The approach must balance security requirements with performance considerations.

## Decision

We will implement local JWT verification in FastAPI using the shared secret (stateless auth) to reduce latency and avoid additional API calls to Better Auth for each request. This approach involves decoding and validating JWT tokens directly within the FastAPI application using the BETTER_AUTH_SECRET.

## Alternatives Considered

1. **Remote Verification**: Call Better Auth API for verification on each request
   - Pros: Centralized validation, immediate revocation capability, stronger security control
   - Cons: Higher latency due to additional network calls, dependency on external service availability, potential performance bottleneck

2. **Hybrid Approach**: Local verification with periodic remote validation
   - Pros: Balance between performance and security, ability to catch revoked tokens periodically
   - Cons: Increased complexity, still has some latency overhead, more difficult to implement correctly

3. **Session-based Authentication**: Store session data server-side
   - Pros: Easier to implement revocation, no token parsing complexity
   - Cons: Doesn't align with JWT requirement, requires additional storage, doesn't scale horizontally as well

## Consequences

**Positive:**
- Reduced latency for API requests since no additional network calls are required
- Improved scalability as authentication doesn't depend on external service availability
- Better performance under high load conditions
- Aligns with the requirement for stateless authentication

**Negative:**
- Less immediate revocation capability (would require token expiration or blacklisting mechanism)
- Responsibility for proper JWT validation lies with the application
- Potential security risk if secret is compromised (affects all tokens)
- Requires careful implementation to avoid common JWT vulnerabilities

## References

- plan.md: Technical Context and Constitution Check sections
- research.md: Authentication Approach decision
- spec.md: Security & Authentication section (FR-001, FR-002)