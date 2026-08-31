# Coverage Chatbot

A containerized policy-coverage chatbot built with FastAPI, Streamlit, SQLite, retrieval, an LLM-backed answer generation layer, guardrails, conversation history, token tracking, and observability support.

## What I built

- **FastAPI backend** for chat and health endpoints.
- **Streamlit frontend** for plan selection and conversational interaction.
- **SQLite** for plans, claims, and conversation history.
- **Retrieval + RAG** for answering policy questions from available context.
- **LLM integration** through an OpenAI-compatible API endpoint.
- **Guardrails** for prompt-injection and cross-member data access patterns.
- **Conversation memory** using session IDs and SQLite history.
- **Token/cost tracking** for LLM usage.
- **Docker Compose** deployment with separate backend/frontend containers.
- **Kubernetes manifests** for backend/frontend Deployments and Services.
- **Kubernetes probes** using `/health`.
- **Langfuse tracing** around answer-generation and conversation-summary LLM operations.

## Architecture

```text
Streamlit frontend
       |
       | HTTP / SSE
       v
FastAPI backend
       |
       +--> SQLite / conversation history
       |
       +--> Retrieval
       |
       +--> LLM
       |
       +--> Langfuse observability
```

## Local Docker deployment

The Day 28 Docker setup uses:

- `Dockerfile` for the backend
- `Dockerfile.frontend` for Streamlit
- `docker-compose.yml`
- `.env` for local secrets

Start the application with:

```powershell
docker compose up -d
```

The frontend is available at:

```text
http://localhost:8501
```

The backend exposes port `8000` and has a `/health` endpoint.

## Kubernetes

The `k8s/` directory contains the Day 29 deployment manifests.

The intended Kubernetes setup includes:

- 2 backend replicas initially
- backend and frontend Services
- readiness and liveness probes
- rolling-update configuration
- Kubernetes Secrets for API credentials

Secrets are created with `kubectl create secret` rather than committed as plaintext YAML.

## Observability

Langfuse tracing is integrated into the backend's LLM generation flow. The implementation records observations for:

- `coverage-answer`
- `conversation-summary`

Langfuse credentials must be supplied through environment variables or Kubernetes Secrets.

## Security

Real API keys and Langfuse credentials are intentionally excluded from the repository.

Do not commit:

```text
.env
```

or plaintext secret values.

## Status

The Docker Compose application was successfully built and brought up with a healthy backend and running frontend.

The Kubernetes manifests and observability implementation are included as the deployment/observability deliverables. The Minikube image-transfer step was not successfully demonstrated during development because the large backend image transfer repeatedly stalled.

## Demo

Add your final demo URL here when available:

```text
Demo: <DRIVE_OR_YOUTUBE_UNLISTED_LINK>
```
