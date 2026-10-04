# 02 · Workloads

| Object | Use it for | Real-world example |
|---|---|---|
| **ReplicaSet** | Keep N identical pods running | Rarely used directly; Deployments manage them |
| **Deployment** | Stateless apps, rolling updates, rollback | Web storefront, REST API |
| **StatefulSet** | Stable identity + own disk per pod | MySQL, Kafka, Elasticsearch |
| **DaemonSet** | One pod per node | Log collector, node monitoring agent |
| **Job** | Run to completion | DB migration, video transcoding |
| **CronJob** | Job on a schedule | Nightly backup, weekly report |

## Deployment: rollout & rollback
```bash
kubectl apply -f deployment.yaml
kubectl set image deploy/nginx-deployment nginx=nginx:1.28 -n nginx   # rolling update
kubectl rollout status deploy/nginx-deployment -n nginx
kubectl rollout undo deploy/nginx-deployment -n nginx                 # bad release? roll back
kubectl scale deploy/nginx-deployment --replicas=5 -n nginx
```
`maxUnavailable: 0` + `maxSurge: 1` = new pod must be ready before an old one is removed → zero downtime.

## StatefulSet
Pods are named `mysql-0, mysql-1, mysql-2`, started in order, each with its own PVC (`mysql-data-mysql-0`). Reachable at `mysql-0.mysql-service.mysql.svc.cluster.local` through a **headless** Service (`clusterIP: None`).
```bash
kubectl apply -f statefulset-mysql.yaml
kubectl delete pod mysql-0 -n mysql      # comes back as mysql-0 with the SAME data
```

## Others
```bash
kubectl apply -f daemonset.yaml && kubectl get ds -n nginx   # 1 pod per node
kubectl apply -f job.yaml && kubectl logs job/nginx-job -n nginx
kubectl apply -f cronjob.yaml && kubectl get cronjob,jobs -n nginx
kubectl create job --from=cronjob/minute-backup manual-run -n nginx   # trigger now
```
Job tips: `backoffLimit` (retries), `ttlSecondsAfterFinished` (auto-cleanup), `completions`/`parallelism` for batch fan-out.
