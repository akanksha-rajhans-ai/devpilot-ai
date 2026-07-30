# ADR 0011: Password Hashing

## Status

Accepted

## Context

DevPilot AI needs authentication support. Before implementing JWT or persistence, the platform needs a safe way to handle user passwords.

## Options Considered

1. Store plaintext passwords
2. Encrypt passwords
3. Hash passwords with a fast hash function
4. Hash passwords with bcrypt using Passlib
5. Delegate all authentication to an external identity provider immediately

## Decision

Use Passlib with bcrypt for password hashing and verification.

## Consequences

Plaintext passwords are never stored. Password verification can be tested independently. Bcrypt adds computational cost by design, which is acceptable for login flows but should be protected with rate limiting.