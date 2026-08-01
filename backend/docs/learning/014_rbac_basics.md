# 014 RBAC Basics

## What Problem Did This Solve?

The platform needed a reusable way to restrict access to routes based on user roles. Authentication alone proves identity, but authorization decides what that identity is allowed to do.

## Why Was This Design Chosen?

We implemented a FastAPI dependency factory called `require_roles`, which lets each route declare its required roles clearly.

## What Alternatives Exist?

- Hardcode role checks inside each route
- Use permission strings instead of roles
- Use policy-based access control
- Use attribute-based access control
- Delegate authorization to an external policy engine

## What Would Break If This Component Disappeared?

Every protected route would need to implement its own authorization logic. This would create duplication and increase the risk of inconsistent security behavior.

## How Would This Evolve At 10x Traffic?

Roles would be loaded from the database or identity provider, cached, audited, and possibly replaced or extended by permission-based or policy-based access control.

## Interview Questions

1. What is the difference between authentication and authorization?
2. Why does missing authentication return 401 while insufficient permissions returns 403?
3. What are the limits of simple role-based access control?
4. Should roles always be trusted from JWT claims?
5. How would authorization apply to MCP tool execution?