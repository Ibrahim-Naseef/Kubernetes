# 04 · Storage & Configuration

Container disks vanish on restart → use volumes.

```
Pod ──mounts──▶ PVC (request) ──binds──▶ PV (actual disk) ◀──provisioned by── StorageClass
```
- **PV**: a piece of storage (cluster-scoped, so *no namespace*).
- **PVC**: "I need 1Gi RWO" – namespaced, used by pods.
- **StorageClass**: recipe for **dynamic provisioning** (EBS gp3, Azure Disk, GCE PD). Developer creates a PVC → disk appears automatically.
- Access modes: `ReadWriteOnce` (one node), `ReadOnlyMany`, `ReadWriteMany` (needs NFS/EFS). Reclaim: `Retain` keeps data, `Delete` removes the disk.

Real world: a Postgres pod crashes and is rescheduled; the PVC re-attaches and no data is lost.
```bash
kubectl apply -f pv-pvc.yaml && kubectl get pv,pvc -A
kubectl patch pvc local-pvc -n nginx -p '{"spec":{"resources":{"requests":{"storage":"5Gi"}}}}'  # if allowVolumeExpansion
```

## ConfigMap & Secret
Keep config out of images so one image runs in dev/stage/prod.
```bash
kubectl create configmap app-config --from-literal=LOG_LEVEL=debug --from-file=nginx.conf
kubectl create secret generic db-cred --from-literal=password='S3cr3t!'
kubectl get secret db-cred -o jsonpath='{.data.password}' | base64 -d
```
Consume as env vars, `envFrom`, or mounted files (see `app-with-config.yaml`). Mounted ConfigMaps update live (~1 min); env vars need a pod restart.

⚠️ Secrets are only **base64-encoded**, not encrypted. Enable encryption at rest + RBAC (see `09-security`) or use External Secrets / Vault / cloud secret managers.
