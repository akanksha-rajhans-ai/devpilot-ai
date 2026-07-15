# ADR 0001: Configuration Management

## Status

Accepted

## Context

DevPilot Platform needs a consistent way to manage configuration across local development, testing, staging, and production.

## Options Considered

1. Hardcoded constants
2. Raw environment variables with `os.environ`
3. YAML/TOML config files
4. Pydantic Settings

## Decision

Use Pydantic Settings with environment variables and a local `.env` file.

## Consequences

Configuration is validated, centralized, and easy to override per environment. Secrets must not be committed. In production, values should come from the deployment environment or a secret manager.