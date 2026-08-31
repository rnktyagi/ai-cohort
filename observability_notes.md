# Day 30 — Langfuse Observability Notes

## What changed

The FastAPI backend now creates Langfuse generation observations around the existing
streaming `generate_answer()` calls.

Tracked LLM operations:

- `coverage-answer`
- `conversation-summary`

Each generation includes request/session metadata and records the generated output.
The application calls `langfuse.flush()` after the streaming generation so traces are
sent promptly.

Langfuse credentials are intentionally NOT stored in YAML or committed to Git.

## Python dependency

Add this package to `requirements-backend.txt`:

```text
langfuse
```

Then rebuild the backend image.

## Local configuration

Add these variables to the local `.env` file:

```text
LANGFUSE_PUBLIC_KEY=pk-lf-REPLACE_ME
LANGFUSE_SECRET_KEY=sk-lf-REPLACE_ME
LANGFUSE_BASE_URL=https://cloud.langfuse.com
LANGFUSE_TRACING_ENVIRONMENT=local
```

Do not commit `.env`.

Langfuse uses these environment variables for authentication. The current Python SDK
uses `get_client()` and the observation API.

## Kubernetes Secret

Create the Langfuse Secret from PowerShell:

```powershell
kubectl create secret generic langfuse-secret `
  --from-literal=LANGFUSE_PUBLIC_KEY="YOUR_PUBLIC_KEY" `
  --from-literal=LANGFUSE_SECRET_KEY="YOUR_SECRET_KEY" `
  --from-literal=LANGFUSE_BASE_URL="https://cloud.langfuse.com"
```

Verify only the Secret metadata:

```powershell
kubectl get secret langfuse-secret
```

Never run commands that print the Secret contents and never put the real values in YAML.

## Redeploy

After the backend image has been rebuilt and made available to Minikube:

```powershell
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/backend-service.yaml
kubectl apply -f k8s/frontend-deployment.yaml
kubectl apply -f k8s/frontend-service.yaml
```

Confirm the backend rollout:

```powershell
kubectl rollout status deployment/backend
kubectl get pods -o wide
kubectl get deployments
```

The backend pods should become `Running` and `Ready`.

## Langfuse confirmation

1. Send a normal chat request through the frontend.
2. Open the Langfuse project dashboard.
3. Confirm a new trace/generation appears.
4. Confirm the observation name is `coverage-answer`.
5. Confirm the trace contains the request/session metadata.
6. Confirm the LLM output is visible in the generation observation.

If no trace appears, check backend logs:

```powershell
kubectl logs deployment/backend
```

Then verify that the Secret exists:

```powershell
kubectl get secret langfuse-secret
```

## Kubernetes debugging checklist

```powershell
kubectl get pods
kubectl describe pod <backend-pod-name>
kubectl logs deployment/backend
kubectl get events --sort-by=.lastTimestamp
kubectl get secret langfuse-secret
```

If a pod is not Ready, inspect its readiness probe and container logs before changing
the deployment.

## Alert sketch

Recommended production alerts:

- **Backend unavailable:** no Ready backend replicas for > 2 minutes.
- **Crash loop:** backend container restarts exceed a small threshold in 5 minutes.
- **High latency:** p95 `/chat` latency exceeds the agreed service target.
- **LLM errors:** generation error rate exceeds the agreed threshold.
- **LLM cost:** daily Langfuse cost exceeds the project budget.
- **Trace ingestion:** expected traces stop arriving while chat traffic continues.

A simple alert flow:

```text
User request
    |
    v
FastAPI backend
    |
    +---- /health ----> Kubernetes readiness/liveness
    |
    +---- LLM call ---> Langfuse
                         |
                         +--> latency / errors / tokens / cost
                         |
                         +--> alerting
```

## Important note

Langfuse credentials are secrets. Keep them in `.env` locally or in the Kubernetes
Secret `langfuse-secret`. Do not commit either credential value to the repository.
