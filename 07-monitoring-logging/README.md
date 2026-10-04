# 07 · Monitoring & Logging

## Metrics Server (powers `kubectl top` and HPA)
```bash
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
# kind/local only (self-signed kubelet certs):
kubectl patch deploy metrics-server -n kube-system --type=json \
  -p='[{"op":"add","path":"/spec/template/spec/containers/0/args/-","value":"--kubelet-insecure-tls"}]'
kubectl top nodes && kubectl top pods -A --sort-by=memory
```

## Logging
Containers log to stdout/stderr; kubelet keeps them on the node (lost when the pod/node dies).
```bash
kubectl logs <pod> -f --tail=100 -c <container>
kubectl logs <pod> --previous              # logs of the crashed container
kubectl logs -l app=nginx --all-containers --prefix   # many pods at once
kubectl get events -A --sort-by=.lastTimestamp
```
Production: ship logs off-node with a DaemonSet agent (**Fluent Bit / Promtail**) → **Loki / Elasticsearch / CloudWatch**, then search in Grafana/Kibana.

## Monitoring stack: Prometheus + Grafana + Alertmanager
```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install kube-prometheus-stack prometheus-community/kube-prometheus-stack -n monitoring --create-namespace
kubectl port-forward svc/kube-prometheus-stack-grafana 3000:80 -n monitoring   # admin / prom-operator
```
- Prometheus **scrapes** `/metrics`; PromQL e.g. `sum(rate(container_cpu_usage_seconds_total{namespace="nginx"}[5m])) by (pod)`.
- `servicemonitor.yaml` registers your app and adds a "pod crash-looping" alert.
- What to watch: the 4 golden signals – latency, traffic, errors, saturation. Others: Datadog, New Relic, OpenTelemetry.
