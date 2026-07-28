# ADR 0008: CI With GitHub Actions

## Status

Accepted

## Context

DevPilot AI needs automated validation on push and pull request to keep the codebase deployable.

## Options Considered

1. Manual local testing only
2. GitHub Actions
3. Jenkins
4. AWS CodeBuild

## Decision

Use GitHub Actions for the initial backend CI pipeline.

## Consequences

The repository now validates backend tests automatically using Python 3.12. The workflow is simple and does not yet include linting, type checks, coverage, Docker builds, security scanning, or deployment.
