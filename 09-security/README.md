# 09 · Security

Layers: **image → pod → network → secrets → access (RBAC) → cluster.**

## Pod Security Standards (PSS)
Built-in admission that replaces PodSecurityPolicy. Levels: `privileged` (anything) → `baseline` (blocks known escalations) → `restricted` (non-root, no privilege escalation, drop all capabilities). Enforced with namespace labels – see `pod-security-standards.yaml`.
```bash
kubectl label ns default pod-security.kubernetes.io/enforce=baseline
kubectl label --dry-run=server --overwrite ns --all pod-security.kubernetes.io/enforce=restricted  # who would break?
```

## Image scanning
Find CVEs *before* deploy. Use small base images (distroless/alpine), pin tags/digests (never `latest`), run as non-root.
```bash
trivy image nginx:1.27 --severity HIGH,CRITICAL
trivy k8s --report summary cluster          # scan the running cluster
```
CI example: `trivy-ci.yaml`. Also: cosign for signing, admission policies (Kyverno/OPA Gatekeeper) to allow only signed/registry-approved images.

## Network Policies
Default-deny + explicit allows (example in `../03-networking/network-policy.yaml`). Real world: only the API pods may talk to the DB; a compromised frontend can't reach it.

## Secrets encryption
By default Secrets sit **unencrypted in etcd**. Enable encryption at rest with `encryption-config.yaml` (kube-apiserver flag `--encryption-provider-config`), verify:
```bash
ETCDCTL_API=3 etcdctl get /registry/secrets/default/db-cred | hexdump -C | head   # should show k8s:enc:aescbc, not plaintext
kubectl get secrets -A -o json | kubectl replace -f -    # re-write old secrets encrypted
```
Managed clouds: EKS envelope encryption with KMS (`--encryption-config` in eksctl), AKS/GKE KMS. Better still: External Secrets Operator / Vault / AWS Secrets Manager.

## Quick checklist
- RBAC least privilege; no `cluster-admin` for apps
- `securityContext`: `runAsNonRoot`, `readOnlyRootFilesystem`, `allowPrivilegeEscalation: false`
- Resource limits everywhere; PSS `restricted` on app namespaces
- Scan images, keep K8s updated, audit logs on
