# 003 Dependency Injection

## What Problem Did This Solve?

Routes should not manually construct or fetch every dependency they need. Dependency injection lets the framework provide shared dependencies such as settings, database sessions, current users, repositories, services, and LLM providers.

## Why Was This Design Chosen?

FastAPI has built-in dependency injection through `Depends`, so we can use the framework's native pattern without adding extra libraries.

## What Alternatives Exist?

- Manually call dependencies inside each route
- Use global objects
- Use a third-party dependency injection container
- Instantiate services directly in route handlers

## What Would Break If This Component Disappeared?

The code would become harder to test and harder to evolve. Routes would be tightly coupled to concrete implementations, making it difficult to swap settings, database sessions, repositories, or AI providers in tests.

## How Would This Evolve At 10x Traffic?

Dependency injection would manage database sessions, service objects, authenticated users, authorization checks, rate limiters, repositories, cache clients, and workflow orchestrators. It would also help isolate request-scoped dependencies from application-scoped dependencies.

## Interview Questions

1. What is dependency injection?
2. Why does DI improve testability?
3. How does FastAPI implement DI?
4. What is the difference between request-scoped and application-scoped dependencies?
5. How would you inject a database session into a route?