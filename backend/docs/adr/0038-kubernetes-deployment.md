# ADR 0038: Package Production Workloads with Helm

## Status

Accepted

## Decision

Docker Compose is the local multi-service environment. Production workloads are
packaged with Helm for EKS, with migrations as a hook job and managed AWS services
for PostgreSQL, Redis, secrets, DNS, and telemetry.

## Consequences

The runtime is portable across Kubernetes environments, while AWS provisioning
remains an explicit infrastructure step requiring account-specific decisions.
