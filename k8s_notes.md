# Kubernetes Deployment Notes

## Architecture

- `backend` Deployment: 2 replicas
- `backend` Service: ClusterIP on port 8000
- `frontend` Deployment: 2 replicas
- `frontend` Service: NodePort on port 30080 -> 8501
- LLM credentials are supplied through the `my-first-app-secret` Kubernetes Secret.
- Images use `imagePullPolicy: Never` because the Day 28 images are intended to be loaded into Minikube.

## Secret

Create the secret from the terminal. Never commit the API key in YAML:

```powershell
kubectl create secret generic my-first-app-secret --from-literal=GROQ_API_KEY="YOUR_REAL_KEY"
```

Verify without printing the secret:

```powershell
kubectl get secret my-first-app-secret
```

## Apply

```powershell
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/backend-service.yaml
kubectl apply -f k8s/frontend-deployment.yaml
kubectl apply -f k8s/frontend-service.yaml
```

Check rollout and readiness:

```powershell
kubectl get deployments
kubectl get pods -o wide
kubectl get services
kubectl rollout status deployment/backend
kubectl rollout status deployment/frontend
```

## Access

```powershell
minikube service frontend --url
```

The frontend Service is exposed as NodePort `30080`.

## Scaling test

The required backend scale test:

```powershell
kubectl scale deployment backend --replicas=3
kubectl get pods -w
```

Expected observation: the Deployment creates a third backend pod while the existing replicas continue serving traffic.

## Rolling update test

Change the backend image tag in `k8s/backend-deployment.yaml` to a new tag, for example:

```yaml
image: my-first-app-backend:v2
```

Load/build that tagged image in Minikube before applying it, then:

```powershell
kubectl apply -f k8s/backend-deployment.yaml
kubectl rollout status deployment/backend
kubectl get pods
```

Expected observation: Kubernetes performs a rolling replacement according to the Deployment strategy, keeping available replicas during the update rather than deleting all old pods at once.

Check rollout history:

```powershell
kubectl rollout history deployment/backend
```

## Teardown

```powershell
kubectl delete -f k8s/frontend-service.yaml
kubectl delete -f k8s/frontend-deployment.yaml
kubectl delete -f k8s/backend-service.yaml
kubectl delete -f k8s/backend-deployment.yaml
kubectl delete secret my-first-app-secret
```

Or, after applying all manifests:

```powershell
kubectl delete -f k8s/
```

## Observations

Record the actual output from the commands above here after testing. Keep secrets and real API keys out of this file.
