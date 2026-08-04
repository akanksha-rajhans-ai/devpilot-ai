# ADR 0016: Rate Limiting Basics

## Status

Accepted

## Context

DevPilot AI will expose APIs that may trigger expensive AI workflows, retrieval, database queries, and MCP tool calls. The platform needs basic abuse and overload protection.

## Options Considered

1. No rate limiting initially
2. In-memory rate limiting middleware
3. Redis-backed rate limiting
4. NGINX or API gateway rate limiting
5. Managed cloud rate limiting

## Decision

Start with in-memory rate limiting middleware for learning and local protection.

## Consequences

The implementation is simple and testable, but not horizontally scalable. It should be replaced or complemented by Redis, NGINX, API Gateway, or AWS WAF before production deployment.