# 01 · Core Concepts

**Pod** – smallest deployable unit: one or more containers sharing network (one IP) and volumes.
**Namespace** – virtual cluster inside a cluster; isolates teams/environments (`dev`, `staging`, `prod`).
**Labels** – key/value tags to *identify and group* objects. **Selectors** – queries over labels.
**Annotations** – non-identifying metadata (owner, docs link, tool config); can't be selected on.

## Real world
A shop runs `frontend`, `cart`, `payments`. Each Pod carries `app=<name>`, `tier=...`, `env=prod`. A Service finds its pods by selector; ops can run `kubectl delete pods -l env=dev` to clean up a whole environment.

```bash
kubectl apply -f namespace-pod-labels.yaml
kubectl get pods -n nginx --show-labels
kubectl get pods -n nginx -l 'app=nginx,env in (dev,staging)'   # selectors
kubectl label pod nginx-pod -n nginx release=v2 --overwrite
kubectl annotate pod nginx-pod -n nginx build=1234
kubectl config set-context --current --namespace=nginx          # default namespace
```

## Multi-container patterns (files in this folder)
- **Init container** (`pod-init-container.yaml`): runs to completion *before* the app. Use: wait for DB, run migrations, download config.
- **Sidecar** (`pod-sidecar.yaml`): runs alongside the app. Use: log shipper (Fluent Bit), proxy (Envoy), secret refresher.

```yaml
initContainers:
  - name: wait-for-db
    image: busybox:1.36
    command: ['sh','-c','until nc -z mysql-service.mysql 3306; do sleep 2; done']
```
```bash
kubectl logs sidecar-test -c sidecar-container -f
```
