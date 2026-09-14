# 029 Agent Audit Events

## What Problem Did This Solve?

The platform needed audit visibility into agent workflow execution. Agent workflows can route requests, call providers, fail, retry, and pause for approval, so their lifecycle must be traceable.

## Why Was This Design Chosen?

We reused the existing `audit_event` utility to record workflow start and finish events from the API endpoint. This keeps audit logging consistent across admin and agent activity.

## What Alternatives Exist?

- Do not audit agent workflows yet
- Audit only failed workflows
- Audit inside every graph node
- Store audit records in a database immediately
- Emit audit events asynchronously

## What Would Break If This Component Disappeared?

Operators would lack a clear record of agent execution. Sensitive workflow activity, approval pauses, and failures would be harder to investigate.

## How Would This Evolve At 10x Traffic?

Audit events would include actor ID, tenant ID, workflow ID, node-level events, tool calls, approval decisions, and resource identifiers. Events would be persisted to an append-only audit store or SIEM.

## Interview Questions

1. Why should agent workflows be audited?
2. What is the difference between audit logs and observability logs?
3. Why audit both workflow start and finish?
4. What metadata is safe to include in agent audit logs?
5. How will this apply to MCP tool execution?