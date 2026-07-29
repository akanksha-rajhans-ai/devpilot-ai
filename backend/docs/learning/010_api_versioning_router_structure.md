# 010 API Versioning & Router Structure

## What Problem Did This Solve?

The application needed a scalable route organization pattern before adding authentication, users, agents, documents, tools, and evaluations.

## Why Was This Design Chosen?

We introduced a central versioned API router under `/api/v1` while keeping operational endpoints such as health checks unversioned.

## What Alternatives Exist?

- Put all routes directly in `main.py`
- Use unversioned product APIs
- Version every endpoint including health
- Version by request header instead of URL path

## What Would Break If This Component Disappeared?

As the API grows, route registration would become harder to maintain. Future API changes could break clients without a clear versioning strategy.

## How Would This Evolve At 10x Traffic?

Each domain would have its own router, such as auth, users, agents, documents, tools, and evaluations. API v2 could be introduced without removing v1 immediately.

## Interview Questions

1. Why version APIs?
2. Why keep health endpoints unversioned?
3. What are alternatives to URL-based versioning?
4. When would you introduce `/api/v2`?
5. How does router composition keep FastAPI apps maintainable?
