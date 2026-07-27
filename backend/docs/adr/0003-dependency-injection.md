# ADR 0003: Dependency Injection

## Status

Accepted

## Context

DevPilot AI will need shared dependencies such as settings, database sessions, authenticated users, service classes, repositories, LLM providers, retrievers, and workflow orchestrators.

## Options Considered

1. Manually instantiate dependencies inside route handlers
2. Use module-level global objects
3. Use FastAPI's built-in dependency injection
4. Add an external dependency injection container

## Decision

Use FastAPI's built-in dependency injection system.

## Consequences

Routes remain small, dependencies are easier to test, and future platform services can be introduced cleanly. FastAPI's dependency system is framework-specific, so if the project moved away from FastAPI, dependency wiring would need to be redesigned.