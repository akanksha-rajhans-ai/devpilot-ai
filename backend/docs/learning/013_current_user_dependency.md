# 013 Current User Dependency

## What Problem Did This Solve?

The platform needed a reusable way to protect API routes and identify the authenticated user from a JWT bearer token.

## Why Was This Design Chosen?

We used FastAPI's dependency injection and `HTTPBearer` security helper. This keeps authentication logic centralized and lets protected routes declare their authentication requirement with `Depends`.

## What Alternatives Exist?

- Parse the Authorization header manually in every route
- Use middleware only
- Use API keys
- Use server-side sessions
- Delegate entirely to an identity provider

## What Would Break If This Component Disappeared?

Every protected route would need custom token parsing and validation. This would duplicate logic and increase security risk.

## How Would This Evolve At 10x Traffic?

The dependency would decode the token, validate issuer/audience, load the user from PostgreSQL or cache, check active status, attach roles and permissions, and emit audit logs.

## Interview Questions

1. What is the `Authorization: Bearer` header?
2. Why should authentication logic live in a reusable dependency?
3. Why return 401 for missing or invalid authentication?
4. What does the JWT `sub` claim represent?
5. How would this dependency change once users are stored in a database?