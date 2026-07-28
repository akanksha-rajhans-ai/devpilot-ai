## Local Environment Constraint

Docker Desktop could not be executed on the corporate-managed Mac because Oracle Santa blocked `com.docker.backend`.

The Dockerfile and Compose configuration were still created to document the intended reproducible runtime. Local verification was performed using the Python virtual environment instead.

In a production or unrestricted development environment, the same configuration would be validated with `docker compose up --build`.