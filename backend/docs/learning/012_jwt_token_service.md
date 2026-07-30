# 012 JWT Token Service

## What Problem Did This Solve?

The platform needs a way to represent authenticated users across stateless HTTP requests. JWT access tokens allow the API to issue signed tokens after login and verify them on later requests.

## Why Was This Design Chosen?

JWT is a common approach for stateless API authentication. The token service is implemented as reusable security utilities before adding login endpoints or user persistence.

## What Alternatives Exist?

- Server-side sessions
- Opaque tokens stored in Redis
- Managed identity provider tokens
- API keys
- mTLS for service-to-service auth

## What Would Break If This Component Disappeared?

The API would not have a reusable way to issue or verify access tokens. Future protected routes would need to invent authentication logic independently.

## How Would This Evolve At 10x Traffic?

Access tokens would use stronger secret management, refresh tokens, key rotation, issuer/audience validation, token revocation strategies, and integration with enterprise identity providers.

## Interview Questions

1. What is a JWT?
2. What is the `sub` claim?
3. Why should JWTs expire?
4. Why should secrets not be stored inside JWT payloads?
5. What are the trade-offs between JWTs and server-side sessions?