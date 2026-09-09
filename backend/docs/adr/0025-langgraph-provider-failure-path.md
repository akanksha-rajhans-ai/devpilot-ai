# ADR 0025: LangGraph Provider Failure Path

## Status

Accepted

## Context

DevPilot AI now has LangGraph routing and model-backed graph nodes. Provider failures need to be represented safely inside workflow state for agent UI and future orchestration behavior.

## Options Considered

1. Let provider failures bubble up as HTTP 502
2. Convert provider failures into workflow failure state
3. Add retries immediately
4. Add a dedicated error handling node immediately

## Decision

Represent handled provider failures as graph state with `status=failed` and a safe error message.

## Consequences

The API can return a completed HTTP response even when the workflow fails. This is useful for agent UIs and future retries/fallbacks. The current approach does not yet distinguish failure categories or retry automatically.