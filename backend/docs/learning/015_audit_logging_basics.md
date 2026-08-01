# 015 Audit Logging Basics

## What Problem Did This Solve?

The platform needs a way to record security-sensitive events such as authorization denials and admin access. Audit logs help answer who did what, when, and with what outcome.

## Why Was This Design Chosen?

We added a small reusable `audit_event` utility that records event name, outcome, actor ID, trace ID, and metadata. This keeps audit logging consistent while avoiding a database-backed audit system too early.

## What Alternatives Exist?

- Use normal application logs only
- Store audit events in a database immediately
- Send audit events to a SIEM
- Use cloud-native audit systems
- Use event streaming for audit records

## What Would Break If This Component Disappeared?

Security-sensitive actions would be harder to investigate. The platform would lack a clear record of denied access, admin access, and future tool or agent execution events.

## How Would This Evolve At 10x Traffic?

Audit events would be stored in an append-only table, streamed to a SIEM, protected from tampering, searchable by actor/resource/trace ID, and retained according to compliance policies.

## Interview Questions

1. What is the difference between application logs and audit logs?
2. Why should denied authorization attempts be audited?
3. What fields belong in an audit event?
4. What should never be included in audit metadata?
5. How would audit logging apply to MCP tools?