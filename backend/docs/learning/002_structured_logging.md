# 002 Structured Logging

## What Problem Did This Solve?

The application needs a consistent way to record runtime events such as startup, health checks, warnings, and errors.

## Why Was This Design Chosen?

We used Python's built-in logging module because it is standard, lightweight, and works well with FastAPI, Docker, and cloud logging systems.

## What Alternatives Exist?

- `print()` statements
- structlog
- loguru
- JSON logging
- OpenTelemetry logs

## What Would Break If This Component Disappeared?

The app would become difficult to debug. Production failures would be harder to investigate because runtime behavior would not be recorded consistently.

## How Would This Evolve At 10x Traffic?

Logs would become structured JSON, include request IDs and trace IDs, and flow into a centralized system such as CloudWatch, Datadog, ELK, or Grafana Loki.

## Interview Questions

1. Why is `print()` not enough for production logging?
2. Why should logs go to stdout in containerized applications?
3. What is the difference between logs, metrics, and traces?
4. What information should not be logged?
5. How would you correlate logs across multiple services?