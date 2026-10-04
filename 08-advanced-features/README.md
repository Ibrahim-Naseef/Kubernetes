# 08 · Advanced Features

## Helm – package manager for K8s
A **chart** = templates + `values.yaml`. One command installs a whole app; values customise per environment. `helm-chart/` is an Apache chart.
```bash
curl -fsSL https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
helm install web ./helm-chart -n apache --create-namespace --set replicaCount=3
helm upgrade web ./helm-chart -f values-prod.yaml
helm history web && helm rollback web 1
helm template web ./helm-chart | less        # preview rendered YAML
helm lint ./helm-chart
```
Real world: `helm install ingress-nginx ingress-nginx/ingress-nginx` instead of writing 20 manifests.

## Operators
Operator = **CRD + controller** encoding human operational knowledge (backup, failover, upgrade).
Reconcile loop: *observe → compare to desired → act → repeat*.
```bash
helm install cnpg cnpg/cloudnative-pg -n cnpg --create-namespace   # Postgres operator
```
```yaml
apiVersion: postgresql.cnpg.io/v1
kind: Cluster
metadata: {name: shop-db}
spec:
  instances: 3              # operator handles replication + automatic failover
  storage: {size: 5Gi}
```
Build your own with Kubebuilder or Operator SDK (Go) / Kopf (Python).

## Service Mesh (Istio / Linkerd)
Sidecar (or ambient) proxies handle service-to-service traffic: automatic **mTLS**, retries, timeouts, **canary releases**, tracing – with zero code changes.
```bash
istioctl install --set profile=demo -y
kubectl label namespace default istio-injection=enabled     # new pods get the proxy
kubectl apply -f istio-canary.yaml                          # 90/10 traffic split
```
Use when you have many microservices; skip it for a handful (adds complexity/overhead).

## Kubernetes API
Everything (`kubectl`, dashboards, operators) calls the REST API.
```bash
kubectl proxy --port=8001 &
curl localhost:8001/api/v1/namespaces/nginx/pods
kubectl get --raw /apis | head                      # API groups
kubectl api-resources && kubectl explain pod.spec
kubectl get pods -v=8                               # see the HTTP calls kubectl makes
```
From code: `api-access.py` (Python client). Inside a pod, use its ServiceAccount token (`config.load_incluster_config()`) – RBAC still applies.
