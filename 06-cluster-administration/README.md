# 06 · Cluster Administration

## RBAC – who can do what
`Role` (namespaced) / `ClusterRole` (cluster-wide) = permissions. `RoleBinding` / `ClusterRoleBinding` = attach to user, group, or ServiceAccount. Principle of least privilege.

Real world: CI pipeline gets a ServiceAccount allowed to manage Deployments in `apache` only.
```bash
kubectl apply -f rbac-serviceaccount.yaml -f rbac-role.yaml -f rbac-rolebinding.yaml   # create namespace apache first
kubectl auth can-i delete pods -n apache --as=system:serviceaccount:apache:apache-user   # yes
kubectl auth can-i delete nodes --as=system:serviceaccount:apache:apache-user            # no
kubectl create token apache-user -n apache        # short-lived token for CI
```
`dashboard-admin-user.yaml` grants cluster-admin to a dashboard user – **learning clusters only**.

## Cluster upgrade (kubeadm; one minor version at a time, e.g. 1.34 → 1.35)
```bash
# 1. read release notes, back up etcd, upgrade control plane first
sudo kubeadm upgrade plan && sudo kubeadm upgrade apply v1.35.1
# 2. per worker (one at a time):
kubectl drain worker1 --ignore-daemonsets --delete-emptydir-data   # evict pods safely
sudo kubeadm upgrade node && sudo apt-get install -y kubelet=1.35.1-* && sudo systemctl restart kubelet
kubectl uncordon worker1
```
Managed services: `eksctl upgrade cluster`, `az aks upgrade`, `gcloud container clusters upgrade`. Use PodDisruptionBudgets so drains don't cause outages.
Backup: `ETCDCTL_API=3 etcdctl snapshot save backup.db`.

## Custom Resource Definitions (CRDs)
Teach the API server new object types. `crd/devopsbatch-crd.yaml` defines `DevopsBatch`; then it's a first-class resource:
```bash
kubectl apply -f crd/devopsbatch-crd.yaml
kubectl apply -f crd/devopsbatch-example.yaml
kubectl get devopsbatch      # or: kubectl get dv
```
A CRD alone only *stores* data. Add a controller to act on it → that's an **Operator** (see `08`). Real examples: `Certificate` (cert-manager), `Prometheus`, `PostgresCluster`.
