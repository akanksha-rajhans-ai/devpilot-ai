# 016 Rate Limiting Basics

## What Problem Did This Solve?

The platform needs protection against excessive requests, accidental traffic spikes, brute-force attempts, and expensive AI workflow abuse.

## Why Was This Design Chosen?

We implemented a simple in-memory middleware to learn rate limiting concepts before introducing Redis-backed distributed rate limiting.

## What Alternatives Exist?

- No rate limiting
- NGINX/API gateway rate limiting
- Redis-backed counters
- Token bucket algorithms
- Managed cloud rate limiting such as AWS WAF/API Gateway

## What Would Break If This Component Disappeared?

The API would be more vulnerable to abuse and accidental overload. Future LLM and tool execution endpoints could generate uncontrolled cost.

## How Would This Evolve At 10x Traffic?

Rate limiting would move to Redis, API Gateway, or NGINX so limits apply consistently across multiple API instances. Limits would be per user, API key, tenant, route, and cost class.

## Interview Questions

1. Why is rate limiting important for AI platforms?
2. Why does in-memory rate limiting fail with multiple API instances?
3. What is HTTP 429?
4. What is the difference between fixed window, sliding window, and token bucket?
5. Where should rate limiting live in a production architecture?