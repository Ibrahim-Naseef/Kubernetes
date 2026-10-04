# apache lab

Original hands-on files: Apache httpd used to practise autoscaling and RBAC. Everything lives in the `apache` namespace.

| File | Object | What it demonstrates |
|---|---|---|
| `namespace.yaml` | Namespace | Lab namespace |
| `deployment.yaml` | Deployment | `httpd`, 1 replica, requests 100m CPU / 128Mi, limits 200m / 256Mi |
| `service.yaml` | Service (ClusterIP) | Internal access on port 80 |
| `hpa.yaml` | HorizontalPodAutoscaler | Scales 1-5 pods on CPU utilization |
| `vpa.yaml` | VerticalPodAutoscaler | Auto-adjusts pod resource requests |
| `service-account.yaml` | ServiceAccount | Identity `apache-user` |
| `role.yaml` | Role | Manage pods, deployments, services in `apache` |
| `role-binding.yaml` | RoleBinding | Gives `apache-user` the `apache-manager` role |

## Prerequisites
- **metrics-server** for the HPA (see [monitoring notes](../../07-monitoring-logging)).
- **VPA components** for `vpa.yaml`. The VPA is not built into Kubernetes; install it from [kubernetes/autoscaler](https://github.com/kubernetes/autoscaler/tree/master/vertical-pod-autoscaler) (`./hack/vpa-up.sh`). The full autoscaler source that used to be vendored here was removed to keep the repo small.

## Run it
```bash
cd my-labs/apache
kubectl apply -f namespace.yaml
kubectl apply -f deployment.yaml -f service.yaml
kubectl apply -f hpa.yaml            # needs metrics-server
kubectl apply -f vpa.yaml            # needs VPA installed

# generate load and watch scaling
kubectl run load --rm -it --image=busybox -n apache -- sh -c "while true; do wget -q -O- http://apache-service; done"
kubectl get hpa -n apache -w

# RBAC
kubectl apply -f service-account.yaml -f role.yaml -f role-binding.yaml
kubectl auth can-i create deployments -n apache --as=system:serviceaccount:apache:apache-user   # yes
kubectl auth can-i delete nodes --as=system:serviceaccount:apache:apache-user                   # no
```

## Things to know
- The HPA target is `averageUtilization: 5` (very low on purpose, so it scales quickly in a demo). Use ~50-70 for real workloads.
- Don't run HPA and VPA on the same CPU metric for a real app; use VPA `updateMode: "Off"` for recommendations only.
- The Role's `rbac.authorization.k8s.io` and `batch` API groups are unused (no matching resources); safe to remove.
- Cleanup: `kubectl delete ns apache`

Helm version of this app: [`08-advanced-features/helm-chart`](../../08-advanced-features/helm-chart). Topic notes: [Scaling](../../05-scaling-scheduling), [RBAC](../../06-cluster-administration).
