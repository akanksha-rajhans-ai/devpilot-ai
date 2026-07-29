# ADR 0010: API Versioning & Router Structure

## Status

Accepted

## Context

DevPilot AI will grow from a small FastAPI application into a platform with authentication, agents, retrieval, tools, evaluations, and operational endpoints.

## Options Considered

1. Register every route directly in `main.py`
2. Use unversioned product APIs
3. Use URL-based API versioning
4. Use header-based API versioning

## Decision

Use URL-based versioning for product APIs under `/api/v1` and keep operational endpoints such as `/health/live` and `/health/ready` unversioned.

## Consequences

The API structure is easier to scale and reason about. Product APIs can evolve by introducing future versions. Operational endpoints remain stable for infrastructure systems such as load balancers and Kubernetes probes.