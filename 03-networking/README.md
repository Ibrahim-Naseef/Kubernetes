# 03 · Networking

## Cluster networking rules
1. Every pod gets its own IP. 2. Pods talk to any pod without NAT. 3. Handled by a CNI plugin (Calico, Cilium, Flannel). Pod IPs change, so never hard-code them → use **Services**.

## Services (stable IP + DNS + load balancing)
| Type | Reachable from | Use |
|---|---|---|
| `ClusterIP` (default) | Inside cluster | Backend, DB |
| `NodePort` | `<nodeIP>:30000-32767` | Dev/testing |
| `LoadBalancer` | Internet via cloud LB | Public app on EKS/AKS/GKE |
| Headless (`clusterIP: None`) | Per-pod DNS | StatefulSets |

DNS: `<service>.<namespace>.svc.cluster.local` – e.g. a Django pod connects to `mysql-service.mysql:3306`.
```bash
kubectl apply -f service-clusterip.yaml
kubectl get endpoints nginx-service -n nginx     # empty? selector doesn't match pod labels
kubectl port-forward svc/nginx-service 8080:80 -n nginx
```

## Ingress (HTTP routing, TLS, one load balancer for many apps)
Needs an **ingress controller** (it does the real work; the Ingress is just rules).
```bash
# kind: label the ingress-ready node, then
kubectl apply -f https://kind.sigs.k8s.io/examples/ingress/deploy-ingress-nginx.yaml
kubectl apply -f ingress.yaml
curl -H "Host: shop.local" http://localhost/web
```
TLS: add `tls: [{hosts: [shop.local], secretName: shop-tls}]` (cert-manager can issue certs automatically).

## Network Policies (pod firewall)
Default is **allow all**. `network-policy.yaml` denies all ingress to the `mysql` namespace then allows only `backend` pods on 3306. Requires a CNI that enforces them (Calico/Cilium; not kind's default).
```bash
kubectl run test --rm -it --image=busybox -n default -- nc -zv mysql-0.mysql-service.mysql 3306   # blocked
```
