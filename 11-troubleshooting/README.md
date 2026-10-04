# 11 · Debugging & Troubleshooting

## The 4-step routine
```bash
kubectl get pods -o wide                       # 1. status, node, restarts
kubectl describe pod <pod>                     # 2. Events section at the bottom = the "why"
kubectl logs <pod> [-c ctr] [--previous]       # 3. app output (--previous for crashed container)
kubectl get events --sort-by=.lastTimestamp    # 4. cluster-wide timeline
```

## Status → cause → fix
| Status | Usual cause | Fix |
|---|---|---|
| `Pending` | Not enough CPU/mem, unbound PVC, taint/affinity mismatch | `describe` → "FailedScheduling"; lower requests, add nodes, fix tolerations |
| `ImagePullBackOff` | Wrong image/tag, private registry w/o `imagePullSecrets` | Fix tag; `kubectl create secret docker-registry` |
| `CrashLoopBackOff` | App exits (bad config, missing env, failed dependency) | `logs --previous`; check ConfigMap/Secret names |
| `OOMKilled` (exit 137) | Memory > limit | Raise limit / fix leak; `kubectl top pod` |
| `Running` but `0/1 Ready` | Readiness probe failing | Check probe path/port |
| `CreateContainerConfigError` | Missing ConfigMap/Secret | Create it / fix the name |
| `Evicted` | Node pressure | Set requests, add capacity |

Practice: `kubectl apply -f broken-pods.yaml` and diagnose each pod.

## Service not reachable?
```bash
kubectl get endpoints <svc>                    # empty => selector/labels mismatch or pods not Ready
kubectl run dbg --rm -it --image=nicolaka/netshoot -- bash
  nslookup mysql-service.mysql ; curl -v http://nginx-service.nginx
kubectl port-forward svc/<svc> 8080:80         # bypass ingress to isolate the layer
```
Order to check: Pod Ready → Endpoints → Service port/targetPort → DNS → NetworkPolicy → Ingress/controller logs.

## Debug tools
```bash
kubectl debug -it <pod> --image=busybox --target=<container>   # ephemeral debug container (distroless images)
kubectl debug node/<node> -it --image=ubuntu                   # shell on a node
kubectl exec -it <pod> -- env | sort
kubectl auth can-i --list                                      # permission issues (Forbidden)
```

## Resource usage analysis
```bash
kubectl top nodes ; kubectl top pods -A --sort-by=cpu
kubectl describe node <node> | grep -A8 "Allocated resources"  # requests vs capacity
kubectl get pods -A -o custom-columns=NS:.metadata.namespace,POD:.metadata.name,CPU:.spec.containers[*].resources.requests.cpu,MEM:.spec.containers[*].resources.requests.memory
```
Many restarts + memory near limit → raise limits; usage far below requests → shrink (VPA recommendations help); node full of requests but idle → over-provisioned.
