"""Talk to the Kubernetes API from code. pip install kubernetes"""
from kubernetes import client, config

config.load_kube_config()          # inside a pod use: config.load_incluster_config()
v1 = client.CoreV1Api()
for p in v1.list_pod_for_all_namespaces().items:
    print(f"{p.metadata.namespace:20} {p.metadata.name:40} {p.status.phase}")
