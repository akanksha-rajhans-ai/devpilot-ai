# 019 Prompt Management Basics

## What Problem Did This Solve?

The platform needed a centralized way to define and version prompts instead of scattering prompt strings throughout routes, services, or future graph nodes.

## Why Was This Design Chosen?

We created a small prompt registry with named, versioned prompt templates. This keeps prompt construction separate from service logic and prepares the platform for prompt evaluation and versioning.

## What Alternatives Exist?

- Hardcode prompts inside services
- Store prompts as plain text files
- Store prompts in a database
- Use LangChain prompt templates immediately
- Use a dedicated prompt management platform

## What Would Break If This Component Disappeared?

Prompt changes would be harder to track, test, evaluate, and roll back. Future agents could accidentally duplicate or drift from expected prompt behavior.

## How Would This Evolve At 10x Traffic?

Prompts would be versioned, evaluated against golden datasets, tracked in observability, and possibly loaded from a prompt registry with approval workflows.

## Interview Questions

1. Why are prompts application logic?
2. Why version prompts?
3. How do prompt changes affect evaluation?
4. Why should prompts not be scattered across services?
5. How would prompt management connect to LangGraph later?