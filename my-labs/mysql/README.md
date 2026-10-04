# mysql lab

Original hands-on files: a 3-replica MySQL StatefulSet with a headless Service, a ConfigMap and a Secret. Everything lives in the `mysql` namespace.

| File | Object | What it demonstrates |
|---|---|---|
| `namespace.yaml` | Namespace | Lab namespace |
| `secret.yaml` | Secret | `MYSQL_ROOT_PASSWORD` (placeholder) |
| `configmap.yaml` | ConfigMap | `MYSQL_DATABASE: devops` |
| `service.yaml` | Headless Service | Per-pod DNS (`mysql-0.mysql-service...`) |
| `statefulset.yaml` | StatefulSet | 3 pods, each with its own 1Gi PVC via `volumeClaimTemplates` |

## Run it
```bash
cd my-labs/mysql

# 1. set your own password first (edit secret.yaml, replace REPLACE_WITH_A_LOCAL_PASSWORD)
kubectl apply -f namespace.yaml
kubectl apply -f secret.yaml -f configmap.yaml -f service.yaml
kubectl apply -f statefulset.yaml

kubectl get pods,pvc -n mysql          # mysql-statefulset-0, -1, -2 + one PVC each
kubectl exec -it mysql-statefulset-0 -n mysql -- mysql -uroot -p -e "SHOW DATABASES;"
```

## Prove persistence
```bash
kubectl exec -it mysql-statefulset-0 -n mysql -- mysql -uroot -p -e "CREATE TABLE devops.t(id INT); INSERT INTO devops.t VALUES (1);"
kubectl delete pod mysql-statefulset-0 -n mysql        # pod is recreated with the same name and disk
kubectl exec -it mysql-statefulset-0 -n mysql -- mysql -uroot -p -e "SELECT * FROM devops.t;"
```

## Things to know
- The 3 replicas are **independent MySQL servers**, not a replicated cluster. Real replication needs extra config or an operator (e.g. MySQL Operator, Percona).
- Other pods connect with `mysql-statefulset-0.mysql-service.mysql.svc.cluster.local:3306`.
- Secrets are only base64-encoded; never commit a real password. See [security notes](../../09-security).
- Cleanup: `kubectl delete ns mysql` (PVCs from StatefulSets are kept until deleted: `kubectl delete pvc --all -n mysql`).

Topic notes: [StatefulSets](../../02-workloads), [Storage & Secrets](../../04-storage).
