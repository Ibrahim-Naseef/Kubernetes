# Kubernetes in One Shot – Notes, Examples & Labs

Hands-on notes following the **[Kubernetes In One Shot](https://www.youtube.com/watch?v=W04brGNgxN4&t=37225s)** course. Each topic folder has a short explanation, a real-world example, `kubectl` commands, and ready-to-apply manifests.

> The sample Django notes app now lives in its own repository (add your link here). Examples in this repo use nginx, Apache and MySQL so they run anywhere.

## Learning path

| # | Folder | Topics |
|---|---|---|
| 00 | [setup](00-setup) | Monolith vs microservices, architecture, local (kind) & AWS EC2 setup, kubectl |
| 01 | [core-concepts](01-core-concepts) | Pods, namespaces, labels, selectors, annotations, init & sidecar containers |
| 02 | [workloads](02-workloads) | Deployments, StatefulSets, DaemonSets, ReplicaSets, Jobs, CronJobs |
| 03 | [networking](03-networking) | Cluster networking, Services, Ingress, Network Policies |
| 04 | [storage](04-storage) | PV, PVC, StorageClass, ConfigMaps, Secrets |
| 05 | [scaling-scheduling](05-scaling-scheduling) | HPA, VPA, node affinity, taints/tolerations, quotas, limits, probes |
| 06 | [cluster-administration](06-cluster-administration) | RBAC, cluster upgrade, CRDs |
| 07 | [monitoring-logging](07-monitoring-logging) | Metrics Server, logging, Prometheus & Grafana |
| 08 | [advanced-features](08-advanced-features) | Operators, Helm, service mesh, Kubernetes API |
| 09 | [security](09-security) | Pod Security Standards, image scanning, network policies, secrets encryption |
| 10 | [cloud-native](10-cloud-native) | EKS/AKS/GKE, cluster autoscaler, Spot/preemptible nodes |
| 11 | [troubleshooting](11-troubleshooting) | kubectl debugging, logs, resource usage analysis |

## My original labs
The files I wrote while following the course are kept in [`my-labs/`](my-labs), one folder per app with its own README: [nginx](my-labs/nginx), [apache](my-labs/apache), [mysql](my-labs/mysql).

## Quick start
```bash
# prerequisites: Docker, kubectl, kind
kind create cluster --name dev --config 00-setup/kind-config.yaml
kubectl apply -f 01-core-concepts/namespace-pod-labels.yaml
kubectl apply -f 02-workloads/deployment.yaml
kubectl apply -f 03-networking/service-clusterip.yaml
kubectl get all -n nginx
kubectl port-forward svc/nginx-service 8080:80 -n nginx     # http://localhost:8080
```
Clean up: `kind delete cluster --name dev`

## Notes
- Manifests use pinned image tags (not `latest`) and namespaces; apply a folder's namespace file first.
- Replace placeholder secrets (`REPLACE_WITH_A_LOCAL_PASSWORD`, `change-me`) locally – never commit real ones.
- Some labs need extras: metrics-server (HPA), VPA, an ingress controller, a Network Policy-capable CNI. The topic README says which.
- Cloud examples (EKS etc.) cost money – delete clusters after practice.

## License
MIT – see [LICENSE](LICENSE).
