# 028 LangGraph Human Approval Stub

## What Problem Did This Solve?

The workflow needed a safe way to identify requests that may require human approval before execution. This is important before adding tools that can read, write, delete, deploy, or call external systems.

## Why Was This Design Chosen?

We added a deterministic approval route and a `waiting_for_approval` workflow status. This teaches human-in-the-loop design without introducing a full approval UI or persistent resume flow yet.

## What Alternatives Exist?

- Let agents execute all actions freely
- Block risky requests entirely
- Ask an LLM to classify risk
- Add a full approval system immediately
- Use policy-based authorization only

## What Would Break If This Component Disappeared?

Future tool and MCP workflows could execute sensitive operations without explicit human control. The system would be less safe and harder to trust in enterprise environments.

## How Would This Evolve At 10x Traffic?

Approval requests would be persisted, assigned to approvers, audited, resumed from checkpoints, and governed by policy based on user, role, tenant, tool, and resource sensitivity.

## Interview Questions

1. Why do AI agents need human approval gates?
2. What types of actions should require approval?
3. How does checkpointing support approval workflows?
4. Why distinguish `waiting_for_approval` from `failed`?
5. How will this apply to MCP tool execution?