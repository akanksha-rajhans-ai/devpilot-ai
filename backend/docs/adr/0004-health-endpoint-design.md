# ADR 0004: Health Endpoint Design

## Status

Accepted

## Context

DevPilot AI needs health endpoints that can support containerized deployments and future Kubernetes probes.

## Options Considered

1. Keep a single `/health` endpoint
2. Split liveness and readiness endpoints
3. Use Kubernetes-style `/livez` and `/readyz`
4. Put health endpoints under `/api/v1`

## Decision

Expose `/health/live` and `/health/ready`.

## Consequences

The API gives deployment systems clearer operational signals. Liveness remains lightweight, while readiness can evolve to check dependencies such as database, Redis, vector store, and AI provider availability.