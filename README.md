# DevPilot AI

DevPilot AI is an enterprise AI platform for developer productivity.

The project is being built incrementally as a production-style platform, not as a one-off chatbot. The goal is to learn and demonstrate backend engineering, platform engineering, AI orchestration, retrieval, evaluation, observability, cloud deployment, and enterprise readiness.

## Current Status

Milestone 1 is focused on platform foundation.

Implemented so far:

- Configuration management with Pydantic Settings
- Centralized application logging
- FastAPI dependency injection foundation
- Liveness and readiness health endpoints
- Centralized API error handling
- Request middleware with trace IDs
- Docker runtime artifacts
- GitHub Actions backend CI

AI features such as LangGraph, RAG, and MCP will be added after the platform foundation is stable and deployable.

## Architecture So Far

```text
Client
  -> FastAPI application
    -> Trace middleware
    -> Exception handlers
    -> API routes
      -> Dependency-injected settings
    -> Structured logs


Current endpoints:
GET /health/live
GET /health/ready
Tech Stack
Current:
Python 3.12 target runtime
FastAPI
Pydantic Settings
Pytest
GitHub Actions
Docker artifacts
Planned:
JWT authentication
RBAC
PostgreSQL
Redis
LangGraph
LangChain
MCP
RAG/vector search
OpenTelemetry
AWS deployment
Kubernetes/EKS
NGINX ingress
Local Development
1. Create and activate virtual environment
From the backend folder:
cd backend
python3 -m venv .venv
source .venv/bin/activate
2. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
3. Configure environment
Copy the example environment file:
cp .env.example .env
4. Run tests
pytest
5. Run API locally
uvicorn app.main:app --reload
Open:
http://127.0.0.1:8000/health/live
http://127.0.0.1:8000/health/ready
Docker Runtime
Docker artifacts are included:
backend/Dockerfile
backend/.dockerignore
docker-compose.yml
When Docker is available:
docker compose up --build
Then open:
http://127.0.0.1:8000/health/live

Local validation currently uses the Python virtual environment.
CI
GitHub Actions runs backend tests on push and pull request using Python 3.12.
Workflow:
.github/workflows/backend-ci.yml
Learning Artifacts
Each major feature includes:
a learning journal entry under backend/docs/learning
an Architecture Decision Record under backend/docs/adr
These documents explain the design choices, alternatives, trade-offs, and interview discussion points.
Roadmap
Milestone 1: Platform Foundation
Configuration
Logging
Dependency injection
Health checks
Error handling
Trace IDs
Docker
CI
Local development documentation
Milestone 2: Authentication & API Gateway
JWT authentication
User identity
RBAC
Rate limiting
Audit logging
Milestone 3: AI Provider Layer
LLM provider abstraction
Mock provider
OpenAI provider
Token and latency tracking
Milestone 4: LangGraph Orchestration
Graph state
Planner node
Router node
Conditional edges
Retries
Human approval
Milestone 5: RAG Knowledge Layer
Document ingestion
Chunking
Embeddings
Vector search
Citations
Retrieval evaluation
Milestone 6: MCP Tool Integration
MCP client
MCP server
Filesystem/code search tools
Tool permissions
Tool audit logs
Milestone 7: Evaluation & Observability
Golden datasets
Faithfulness checks
Cost tracking
OpenTelemetry
Dashboards
Milestone 8: AWS & Kubernetes Deployment
ECR
ECS/Fargate
CloudWatch
Secrets Manager
NGINX
EKS
Helm