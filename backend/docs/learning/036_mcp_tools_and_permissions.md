# 036: MCP Tools and Permissions

## What Was Built

DevPilot exposes knowledge operations through a typed tool catalog and an MCP
server. The same executor supports deterministic local agent tests and remote
MCP clients.

## Core Lesson

MCP is a transport and discovery protocol. It does not replace authorization.
Every tool still needs application-owned policy, bounded inputs, audit events,
and a decision about human approval.

## Interview Questions

1. What problem does MCP solve that a normal REST API does not directly solve?
2. Why must tool authorization live outside the model prompt?
3. What is the difference between tool discovery and tool execution?
4. How do you defend against a model choosing the wrong tool?
5. Which actions require idempotency keys?
6. Where should tool outputs be validated and size-limited?
7. Why are read, write, and sensitive permissions distinct?
8. How would you isolate an untrusted filesystem MCP server?

## Production Evolution

Use workload identity, network isolation, per-tool timeouts, circuit breakers,
output schemas, tenant-aware authorization, approval records, and immutable audit
storage. Remote MCP servers should be treated as external dependencies.
