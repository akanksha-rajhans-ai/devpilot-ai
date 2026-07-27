# 004 Health Endpoint Refinement

## What Problem Did This Solve?

The application needs separate health checks for process liveness and service readiness. A single `/health` endpoint does not clearly tell infrastructure whether to restart the process or simply stop routing traffic to it.

## Why Was This Design Chosen?

We split health checks into `/health/live` and `/health/ready`, following common container and Kubernetes practices.

## What Alternatives Exist?

- Single `/health` endpoint
- `/livez` and `/readyz`
- Health checks under `/api/v1/health`
- External monitoring checks only

## What Would Break If This Component Disappeared?

Deployment systems would have less reliable signals. They might route traffic to an app that is alive but unable to serve requests because a required dependency is unavailable.

## How Would This Evolve At 10x Traffic?

Readiness would check database, Redis, vector store, object storage, and required internal services. It might expose dependency latency and degraded states while keeping sensitive details hidden.

## Interview Questions

1. What is the difference between liveness and readiness?
2. Should liveness call the database? Why or why not?
3. When should readiness return 503?
4. How do Kubernetes probes use health endpoints?
5. What dependencies should an AI platform check before receiving traffic?