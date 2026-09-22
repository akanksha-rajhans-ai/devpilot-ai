# 038: Cloud-Native Deployment

## What Was Built

Docker Compose runs NGINX, FastAPI, PostgreSQL with pgvector, and Redis. The Helm
chart adds migrations, health probes, resource limits, autoscaling, disruption
budgets, services, and ingress for EKS.

## Interview Questions

1. Why should schema migration be a deployment job rather than run in every pod?
2. How do liveness and readiness probes differ?
3. Why does an HPA require resource requests?
4. What happens when a pod is terminated during an LLM request?
5. How should secrets reach EKS workloads?
6. When would ECS/Fargate be simpler than EKS?
7. How do NGINX ingress and an AWS load balancer divide responsibilities?
8. What would a safe canary release measure before promotion?
