# 00 · Setup & Architecture

## Monolithic vs Microservices
| | Monolith | Microservices |
|---|---|---|
| Deploy | One big unit | Many small services |
| Scale | Whole app | Only the busy service |
| Failure | One bug can take everything down | Isolated |
| Example | Single Django app: UI + payments + search | `web`, `payments`, `search` as separate Deployments |

Kubernetes (K8s) shines with microservices: it schedules, heals, scales and networks containers for you.

## Architecture
- **Control plane**: `kube-apiserver` (front door), `etcd` (cluster database), `kube-scheduler` (picks a node), `controller-manager` (keeps actual state = desired state).
- **Worker node**: `kubelet` (runs pods), `kube-proxy` (service networking), container runtime (containerd).

Flow of `kubectl apply -f deploy.yaml`: kubectl → API server → stored in etcd → scheduler picks node → kubelet starts container.

## Local setup (kind = Kubernetes in Docker)
```bash
kind create cluster --name dev --config kind-config.yaml   # 1 control-plane + 3 workers
kubectl cluster-info && kubectl get nodes
```

## AWS EC2 setup (kubeadm, Ubuntu 22.04+, t3.medium or bigger)
```bash
# on every node: disable swap, install containerd + kubeadm/kubelet/kubectl
sudo swapoff -a
sudo apt-get update && sudo apt-get install -y containerd kubelet kubeadm kubectl

# control-plane only
sudo kubeadm init --pod-network-cidr=10.244.0.0/16
mkdir -p ~/.kube && sudo cp /etc/kubernetes/admin.conf ~/.kube/config && sudo chown $USER ~/.kube/config
kubectl apply -f https://github.com/flannel-io/flannel/releases/latest/download/kube-flannel.yml

# workers: run the `kubeadm join ...` command printed by init
```
Open security-group ports: 6443 (API), 10250 (kubelet), 30000-32767 (NodePorts).

## kubectl essentials
```bash
kubectl get pods -A -o wide          # everything, with node/IP
kubectl apply -f file.yaml           # create/update declaratively
kubectl describe pod <name>          # events = first place to look
kubectl logs <pod> -c <container> -f
kubectl exec -it <pod> -- sh
kubectl explain deployment.spec.strategy   # built-in docs
kubectl config get-contexts && kubectl config use-context <ctx>
```
Tip: `alias k=kubectl` and `source <(kubectl completion bash)`.
