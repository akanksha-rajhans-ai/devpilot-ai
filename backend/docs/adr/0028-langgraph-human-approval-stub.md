# ADR 0028: LangGraph Human Approval Stub

## Status

Accepted

## Context

DevPilot AI will eventually execute tool and MCP workflows that may interact with files, GitHub, Slack, databases, deployments, and other sensitive systems.

## Options Considered

1. Allow all graph routes to execute automatically
2. Block risky requests entirely
3. Add a deterministic human approval route
4. Implement a complete approval/resume system immediately

## Decision

Add a simple `needs_approval` route that returns `status=waiting_for_approval` for risky requests.

## Consequences

The platform now models human approval as part of workflow state. No actual approval/resume UI exists yet, and risk classification is currently keyword-based.