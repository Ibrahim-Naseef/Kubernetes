# My Labs

My original hands-on practice files, kept as I wrote them. One folder per application, each with its own README (file list, run order, things to know).

| Folder | Practises |
|---|---|
| [nginx](nginx) | Pod, ReplicaSet, Deployment, DaemonSet, Job, CronJob, Service, Ingress, PV/PVC |
| [apache](apache) | Deployment, Service, HPA, VPA, RBAC (ServiceAccount, Role, RoleBinding) |
| [mysql](mysql) | StatefulSet, headless Service, ConfigMap, Secret, volumeClaimTemplates |

The numbered folders at the repo root (`00-setup` ... `11-troubleshooting`) hold the topic-wise notes with cleaned-up examples. Use them for the theory and these labs for practice.

Each lab uses its own namespace, so you can run them independently:
```bash
kind create cluster --name dev --config ../00-setup/kind-config.yaml
```
