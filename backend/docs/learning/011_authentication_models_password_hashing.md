# 011 Authentication Models & Password Hashing

## What Problem Did This Solve?

The platform needs a safe foundation for user registration and login. This feature defines authentication request/response models and password hashing utilities.

## Why Was This Design Chosen?

We separated Pydantic schemas from password hashing logic. Schemas validate input/output shapes, while `security.py` owns security-related utilities.

## What Alternatives Exist?

- Store plaintext passwords
- Use reversible encryption
- Use hashlib directly
- Use Argon2 instead of bcrypt
- Delegate authentication entirely to an identity provider

## What Would Break If This Component Disappeared?

The platform would not have a safe way to handle user credentials. Storing plaintext passwords would create severe security risk.

## How Would This Evolve At 10x Traffic?

Password hashes would be stored in PostgreSQL. Login attempts would be rate-limited. Account lockout, MFA, OAuth, password reset, and audit logging would be added.

## Interview Questions

1. Why should passwords be hashed instead of encrypted?
2. Why is bcrypt better than a fast hash like SHA-256 for passwords?
3. Why should API responses never include password hashes?
4. What is the difference between registration and login validation?
5. How would you migrate from bcrypt to another hashing algorithm?