# 05 · Scaling & Scheduling

## Requests & Limits
- **requests**: guaranteed amount; scheduler uses it to place the pod.
- **limits**: ceiling. Over CPU limit → throttled. Over memory limit → **OOMKilled**.
- QoS: Guaranteed (requests = limits) > Burstable > BestEffort (evicted first).

## Probes
| Probe | Failing means | Real-world use |
|---|---|---|
| startup | keep waiting, don't run others | Slow Java app booting 60s |
| readiness | removed from Service traffic | Cache warming, DB down |
| liveness | container restarted | Deadlocked process |
See `apache-deployment.yaml`.

## HPA – more/less pods (horizontal)
Black Friday traffic: CPU > 50% → add pods (max 5). Needs **metrics-server** and CPU *requests*.
```bash
kubectl apply -f apache-deployment.yaml -f hpa.yaml
kubectl run load --rm -it --image=busybox -n apache -- sh -c "while true; do wget -q -O- http://apache-service; done"
kubectl get hpa -n apache -w
```

## VPA – bigger/smaller pods (vertical)
Right-sizes requests from real usage. Install from the [kubernetes/autoscaler](https://github.com/kubernetes/autoscaler/tree/master/vertical-pod-autoscaler) repo (`./hack/vpa-up.sh`), then `kubectl apply -f vpa.yaml`. `updateMode: "Off"` = recommendations only (safest). Don't combine HPA and VPA on the same CPU metric.

## Scheduling controls (`scheduling.yaml`)
- **nodeSelector / nodeAffinity**: *attract* pods to nodes (SSD nodes, a zone).
- **Taints** (on node) **repel**; **tolerations** (on pod) allow. GPU nodes get `dedicated=gpu:NoSchedule` so only GPU jobs land there.
- Also: `podAntiAffinity` / `topologySpreadConstraints` to spread replicas across nodes/zones.
```bash
kubectl taint node worker1 dedicated=gpu:NoSchedule
kubectl taint node worker1 dedicated=gpu:NoSchedule-   # remove
```

## ResourceQuota & LimitRange (`quota-limitrange.yaml`)
Quota caps a namespace total; LimitRange sets per-container defaults. `kubectl describe quota -n apache`.
