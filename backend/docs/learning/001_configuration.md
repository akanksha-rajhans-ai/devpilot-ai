# 001 Configuration Management

## What Problem Did This Solve?

The application needs a reliable way to manage environment-specific values such as app name, database URL, Redis URL, logging level, and LLM provider settings.

## Why Was This Design Chosen?

We used Pydantic Settings because it validates configuration, reads from environment variables, supports `.env` files for local development, and keeps configuration separate from application logic.

## What Alternatives Exist?

- Raw `os.environ`
- Python config files
- YAML/TOML config files
- Secret managers such as AWS Secrets Manager

## What Would Break If This Disappeared?

The app would rely on hardcoded values. Changing environments would require code changes, increasing the risk of production mistakes.

## How Would This Evolve At 10x Traffic?

Secrets would move to AWS Secrets Manager or Kubernetes Secrets. Config would be injected at deployment time. Settings would remain read-only at runtime.

## Interview Questions

1. Why should config come from environment variables?
2. How do you avoid committing secrets?
3. Why use Pydantic Settings instead of `os.environ` directly?
4. How would config differ between local, staging, and production?