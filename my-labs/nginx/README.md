# nginx lab

Original hands-on files: nginx used to practise most workload, networking and storage objects. Everything lives in the `nginx` namespace.

| File | Object | What it demonstrates |
|---|---|---|
| `namespace.yaml` | Namespace | Isolated space for the lab |
| `pod.yaml` | Pod | Single pod with a toleration (`prod=true:NoSchedule`) |
| `replicaset.yaml` | ReplicaSet | Keeps 2 nginx pods running |
| `deployment.yaml` | Deployment | 2 replicas, resource requests/limits, mounts a PVC |
| `daemonset.yaml` | DaemonSet | One nginx pod per node |
| `jobs.yaml` | Job | Run-to-completion task (`sleep 30`) |
| `cron-job.yaml` | CronJob | Backup every minute using hostPath volumes |
| `service.yaml` | Service (ClusterIP) | Stable internal endpoint for nginx |
| `ingress.yaml` | Ingress | Routes `/nginx` to nginx and `/` to the notes app |
| `persistent-volume.yaml` | PV | 1Gi hostPath disk (`local-storage`) |
| `persistent-volume-claim.yaml` | PVC | Claims that disk for the Deployment |

## Run it
```bash
cd my-labs/nginx
kubectl apply -f namespace.yaml

# storage first (the Deployment needs the PVC)
kubectl apply -f persistent-volume.yaml -f persistent-volume-claim.yaml

kubectl apply -f deployment.yaml -f service.yaml
kubectl get all,pvc -n nginx

# try the other workloads one at a time
kubectl apply -f pod.yaml
kubectl apply -f replicaset.yaml
kubectl apply -f daemonset.yaml
kubectl apply -f jobs.yaml && kubectl logs job/nginx-job -n nginx
kubectl apply -f cron-job.yaml && kubectl get cronjob,jobs -n nginx

kubectl port-forward svc/nginx-service 8080:80 -n nginx   # http://localhost:8080
```

## Things to know
- `deployment.yaml`, `replicaset.yaml` and `daemonset.yaml` share the label `app: nginx`, so `nginx-service` selects pods from all of them. Apply them one at a time to see each behave.
- The Deployment mounts the PVC over the nginx web root, so the page is empty (403/404) until you add an `index.html` to the volume.
- `ingress.yaml` needs an ingress controller, and its `/` rule points to `notes-app-service` (the Django notes app, from the separate repo). That Service must exist in the `nginx` namespace or the rule has no backend.
- PVs are cluster-scoped, so the `namespace` field in `persistent-volume.yaml` is ignored (newer kubectl may warn).
- Cleanup: `kubectl delete ns nginx && kubectl delete pv local-pv`

Topic notes: [Workloads](../../02-workloads), [Networking](../../03-networking), [Storage](../../04-storage).
