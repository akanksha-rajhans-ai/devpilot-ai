# 005 Error Handling

## What Problem Did This Solve?

The application needs a consistent error response format so clients can reliably handle failures. Without centralized error handling, different errors may return different shapes depending on where they originate.

## Why Was This Design Chosen?

We used FastAPI exception handlers because they let us centralize framework-level, validation, and unexpected error handling without adding extra dependencies.

## What Alternatives Exist?

- Let FastAPI return default errors
- Raise custom exceptions everywhere
- Use middleware-only error handling
- Use a third-party API error framework

## What Would Break If This Component Disappeared?

Clients would receive inconsistent error responses. Internal details could accidentally leak. Logs would be less useful during debugging and incident response.

## How Would This Evolve At 10x Traffic?

Responses would include trace IDs, machine-readable error codes, localized messages if needed, and links to internal documentation. Alerts would trigger on error rates rather than individual failures.

## Interview Questions

1. Why should APIs have a consistent error format?
2. What should be logged but not returned to clients?
3. What is the difference between 400, 401, 403, 404, 422, and 500?
4. Why should unhandled exceptions return generic messages?
5. How would trace IDs improve error debugging?