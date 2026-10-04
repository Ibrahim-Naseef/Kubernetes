# 10 · Cloud-Native Kubernetes

## Managed services
Cloud runs the control plane (HA, patching, etcd backups); you manage workloads and nodes.
| | AWS **EKS** | Azure **AKS** | Google **GKE** |
|---|---|---|---|
| Create | `eksctl create cluster -f eksctl-cluster.yaml` | `az aks create -g rg -n demo --node-count 2` | `gcloud container clusters create demo --num-nodes 2` |
| Kubeconfig | `aws eks update-kubeconfig --name demo-cluster` | `az aks get-credentials -g rg -n demo` | `gcloud container clusters get-credentials demo` |
| Notes | Highly flexible, more manual add-ons | Free control plane, AD integration | Most automated; Autopilot mode |
Public apps: `Service type: LoadBalancer` or Ingress → cloud load balancer; PVCs → EBS/Azure Disk/PD automatically.
Always delete test clusters (`eksctl delete cluster ...`) – they bill by the hour.

## Cluster Autoscaler (adds/removes *nodes*)
Pending pods (no room) → scale node group **up**; underused nodes → scale **down**. Complements HPA (pods) – HPA creates pods, CA creates nodes for them.
```bash
helm repo add autoscaler https://kubernetes.github.io/autoscaler
helm install ca autoscaler/cluster-autoscaler -n kube-system \
  --set autoDiscovery.clusterName=demo-cluster --set awsRegion=ap-south-1
kubectl logs -n kube-system -l app.kubernetes.io/name=aws-cluster-autoscaler -f
```
Node groups need the `k8s.io/cluster-autoscaler/...` tags (see `eksctl-cluster.yaml`). Alternative on AWS: **Karpenter** (faster, picks instance types automatically). Pods **must set resource requests** or CA can't compute need.

## Spot / Preemptible nodes
Spare cloud capacity at 60–90% discount, but can be reclaimed with ~2 min notice (AWS Spot, Azure Spot, GKE Spot/Preemptible).
- Good: stateless workers, CI runners, batch jobs, dev clusters.
- Bad: databases, single-replica services.
- Pattern: on-demand group for critical pods + tainted Spot group (`eksctl-cluster.yaml`); workloads opt in with a toleration (`spot-workload.yaml`); diversify instance types; run ≥2 replicas; add a `PodDisruptionBudget` (`pdb.yaml`); handle SIGTERM gracefully.
