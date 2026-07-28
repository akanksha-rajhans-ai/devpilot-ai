# 008 CI With GitHub Actions

## What Problem Did This Solve?

The project needs automated verification so every push and pull request runs tests in a clean environment.

## Why Was This Design Chosen?

GitHub Actions integrates directly with GitHub repositories and is sufficient for running backend tests, building Docker images later, and eventually deploying to AWS.

## What Alternatives Exist?

- Run tests manually only
- Jenkins
- CircleCI
- GitLab CI
- Buildkite
- AWS CodeBuild

## What Would Break If This Component Disappeared?

The team would rely on developers remembering to run tests locally. Broken code could be pushed without automated feedback.

## How Would This Evolve At 10x Traffic?

CI would add linting, type checks, coverage, Docker image builds, vulnerability scanning, ECR image pushes, staging deployments, smoke tests, and production promotion workflows.

## Interview Questions

1. What is continuous integration?
2. Why run CI in a clean environment?
3. Why pin the Python version in CI?
4. What checks should block a pull request?
5. How does CI lead into CD?

## CI Failure Lesson

CI initially failed because the local `.env` used `APP_NAME="DevPilot AI"`, while the default value in `config.py` still used `DevPilot Platform`.

Local tests passed because `.env` masked the mismatch. GitHub Actions ran in a clean environment without `.env`, so it exposed the incorrect default.

This showed why CI matters: it validates the project outside the developer's local machine and catches hidden environment assumptions.