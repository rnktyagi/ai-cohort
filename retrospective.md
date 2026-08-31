# Retrospective

## What worked

### Dockerization

The backend and frontend were separated into their own Docker images. The Compose configuration provided a straightforward local deployment with separate ports and a shared application network.

The final Compose stack successfully reached:

- backend: healthy
- frontend: running

### Application debugging

A useful debugging lesson was separating infrastructure failures from application failures.

The backend initially crashed because `generate_answer()` required a `context` argument while `retrieve_and_answer()` called it without one. The module also executed test questions during import, which was inappropriate for a FastAPI application.

The SQLite issue was caused by the frontend opening:

```python
sqlite3.connect("../coverage.db")
```

inside `/app`. Changing it to:

```python
sqlite3.connect("coverage.db")
```

matched the Docker mount and fixed the database lookup.

### Resource management

The Docker/WSL environment became unstable when the Windows C: drive reached effectively zero free space. Cleaning caches and moving Docker's virtual disk location to:

```text
D:\DockerDesktop
```

gave Docker enough room to recover.

## What was hard

The largest difficulty was the combination of a large Python dependency set, Docker image size, and limited local disk space.

The backend image became approximately 9 GB. Attempts to transfer it into Minikube repeatedly stalled with `minikube image load`.

Building the same dependency set inside Minikube was also impractically slow for the available development time.

## What I would do differently

1. Keep the backend dependency list as small as possible.
2. Use a registry workflow for Kubernetes images instead of repeatedly transferring a multi-GB image manually.
3. Check available disk space before starting large Docker builds.
4. Keep test/demo code behind `if __name__ == "__main__":` so importing application modules does not execute tests.
5. Use explicit absolute/container paths for persistent files such as SQLite databases.
6. Add automated smoke tests for `/health` and `/chat`.
7. Add CI validation for Dockerfiles and Kubernetes YAML before deployment.
8. Capture observability evidence while each feature is being implemented instead of at the end.

## Biggest lesson

The most important lesson was to isolate problems systematically:

```text
Application code
      ↓
Container build
      ↓
Container runtime
      ↓
Docker resources
      ↓
Kubernetes
      ↓
Observability
```

Fixing the lower layer before debugging the next layer prevents infrastructure problems from being mistaken for application bugs.
