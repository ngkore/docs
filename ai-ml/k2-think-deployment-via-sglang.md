# K2-Think (LLM) OnPrem Deployment via sglang

**Author:** [Shivank Chaudhary](https://www.linkedin.com/in/shivank1128/)

**Published:** September 14, 2025

Running state-of-the-art large language models in production requires careful orchestration, especially when dealing with multi-GPU workloads that demand significant computational resources. In this comprehensive guide, we’ll explore how to deploy K2-Think — on Kubernetes using modern serving frameworks.

## K2-Think: LLM360’s Reasoning Specialist

K2-Think from LLM360 focuses on enhanced reasoning capabilities with:

- **Context Length**: Up to 65,536 tokens
- **Architecture**: Optimized for multi-turn conversations
- **Serving Framework**: vLLM with OpenAI-compatible API

Let’s start with the prerequisites:

- A K8s cluster installed with Nvidia GPU Operator

```bash
NAMESPACE         NAME                                                              READY   STATUS      RESTARTS      AGE
cert-manager      cert-manager-5969544f77-pmrt7                                     1/1     Running     0             9d
cert-manager      cert-manager-cainjector-65967ff5cc-tbntm                          1/1     Running     0             9d
cert-manager      cert-manager-webhook-7c665868cb-n9n7r                             1/1     Running     0             9d
addons            gpu-feature-discovery-2c2bz                                       1/1     Running     0             19d
addons            gpu-feature-discovery-js5k7                                       1/1     Running     0             45h
addons            gpu-feature-discovery-ss2zk                                       1/1     Running     0             19d
addons            gpu-operator-76db5d4656-27lmb                                     1/1     Running     0             19d
addons            ingress-nginx-controller-677d485949-nnsmn                         1/1     Running     0             13d
addons            local-path-provisioner-596b4859f7-nhp8j                           1/1     Running     0             13d
addons            metallb-controller-54574fc5b7-2c625                               1/1     Running     0             13d
addons            metallb-speaker-2dv8n                                             4/4     Running     0             13d
addons            metallb-speaker-k2r7z                                             4/4     Running     0             13d
addons            metallb-speaker-rdqtb                                             4/4     Running     0             45h
addons            nvidia-container-toolkit-daemonset-c6dsr                          1/1     Running     0             45h
addons            nvidia-container-toolkit-daemonset-wndt4                          1/1     Running     0             19d
addons            nvidia-container-toolkit-daemonset-xnlmw                          1/1     Running     0             19d
addons            nvidia-cuda-validator-44zsb                                       0/1     Completed   0             19d
addons            nvidia-cuda-validator-fvf77                                       0/1     Completed   0             19d
addons            nvidia-cuda-validator-mjm7r                                       0/1     Completed   0             45h
addons            nvidia-dcgm-exporter-hflzf                                        1/1     Running     0             45h
addons            nvidia-dcgm-exporter-knqbf                                        1/1     Running     0             19d
addons            nvidia-dcgm-exporter-spst5                                        1/1     Running     0             19d
addons            nvidia-device-plugin-daemonset-7lxtk                              1/1     Running     0             45h
addons            nvidia-device-plugin-daemonset-djz4l                              1/1     Running     0             19d
addons            nvidia-device-plugin-daemonset-phz6m                              1/1     Running     0             19d
addons            nvidia-driver-daemonset-5.15.0-140-generic-ubuntu22.04-4xqrc      2/2     Running     4 (19d ago)   19d
addons            nvidia-driver-daemonset-5.15.0-140-generic-ubuntu22.04-p5tkn      2/2     Running     3 (19d ago)   19d
addons            nvidia-driver-daemonset-5.15.0-140-generic-ubuntu22.04-s8djl      2/2     Running     5 (45h ago)   45h
addons            nvidia-gpu-operator-node-feature-discovery-gc-85cbffc74d-4nxn4    1/1     Running     0             19d
addons            nvidia-gpu-operator-node-feature-discovery-master-7f8d4b68582kn   1/1     Running     0             19d
addons            nvidia-gpu-operator-node-feature-discovery-worker-mkxzq           1/1     Running     0             45h
addons            nvidia-gpu-operator-node-feature-discovery-worker-v24vq           1/1     Running     0             19d
addons            nvidia-gpu-operator-node-feature-discovery-worker-x8cxv           1/1     Running     0             19d
addons            nvidia-mig-manager-2vzkf                                          1/1     Running     0             19d
addons            nvidia-mig-manager-vs7w2                                          1/1     Running     0             45h
addons            nvidia-mig-manager-xhdbk                                          1/1     Running     0             19d
addons            nvidia-operator-validator-fc69v                                   1/1     Running     0             19d
addons            nvidia-operator-validator-qjmkh                                   1/1     Running     0             45h
addons            nvidia-operator-validator-v6jsq                                   1/1     Running     0             19d
compass-system    compass-agent-678f4d9cbd-z55rv                                    1/1     Running     9 (13d ago)   19d
grok              grok2-sglang-f68f88b9b-9bsvl                                      0/1     Init:0/1    0             2m20s
kube-system       calico-kube-controllers-868cbf9cc-h7sz2                           1/1     Running     0             19d
kube-system       calico-node-8t486                                                 1/1     Running     0             19d
kube-system       calico-node-stkng                                                 1/1     Running     0             45h
kube-system       calico-node-xt56j                                                 1/1     Running     0             19d
kube-system       coredns-75bc46dc6c-6wvnt                                          1/1     Running     0             19d
kube-system       coredns-75bc46dc6c-x4smv                                          1/1     Running     0             19d
kube-system       etcd-hgx-gpu-compute-150                                          1/1     Running     0             19d
kube-system       kube-apiserver-hgx-gpu-compute-150                                1/1     Running     0             19d
kube-system       kube-controller-manager-hgx-gpu-compute-150                       1/1     Running     0             19d
kube-system       kube-proxy-6gk57                                                  1/1     Running     0             19d
kube-system       kube-proxy-mqmsg                                                  1/1     Running     0             19d
kube-system       kube-proxy-qvkvn                                                  1/1     Running     0             45h
kube-system       kube-scheduler-hgx-gpu-compute-150                                1/1     Running     0             19d
longhorn-system   csi-attacher-5cfcfffdf-mpkfx                                      1/1     Running     1 (19d ago)   19d
longhorn-system   csi-attacher-5cfcfffdf-mqpbr                                      1/1     Running     1 (19d ago)   19d
longhorn-system   csi-attacher-5cfcfffdf-skjq6                                      1/1     Running     1 (19d ago)   19d
longhorn-system   csi-provisioner-76bf7c68ff-4z8qc                                  1/1     Running     0             19d
longhorn-system   csi-provisioner-76bf7c68ff-8mtx4                                  1/1     Running     0             19d
longhorn-system   csi-provisioner-76bf7c68ff-vj5fb                                  1/1     Running     1 (19d ago)   19d
longhorn-system   csi-resizer-75c4685b5b-46n5s                                      1/1     Running     0             19d
longhorn-system   csi-resizer-75c4685b5b-nlc42                                      1/1     Running     0             19d
longhorn-system   csi-resizer-75c4685b5b-qw2mp                                      1/1     Running     0             19d
longhorn-system   csi-snapshotter-769588d6bb-czkkl                                  1/1     Running     0             19d
longhorn-system   csi-snapshotter-769588d6bb-jdsz5                                  1/1     Running     0             19d
longhorn-system   csi-snapshotter-769588d6bb-t49d9                                  1/1     Running     0             19d
longhorn-system   engine-image-ei-b4bcf0a5-572vl                                    1/1     Running     0             19d
longhorn-system   engine-image-ei-b4bcf0a5-nxp4p                                    1/1     Running     0             45h
longhorn-system   engine-image-ei-b4bcf0a5-rglbk                                    1/1     Running     0             19d
longhorn-system   instance-manager-2c1a767560aac05a8eebcfefc4fd72e4                 1/1     Running     0             19d
longhorn-system   instance-manager-6be5230635b99ba14cbcabdcc2b2f343                 1/1     Running     0             45h
longhorn-system   instance-manager-fd77d6a642bfebd11e64659fadc84aaf                 1/1     Running     0             19d
longhorn-system   longhorn-csi-plugin-7zcz4                                         3/3     Running     0             19d
longhorn-system   longhorn-csi-plugin-92cw8                                         3/3     Running     0             19d
longhorn-system   longhorn-csi-plugin-vrxjg                                         3/3     Running     1 (45h ago)   45h
longhorn-system   longhorn-driver-deployer-58c9dd465-wth7d                          1/1     Running     0             19d
longhorn-system   longhorn-manager-2pm64                                            2/2     Running     0             45h
longhorn-system   longhorn-manager-lfsfv                                            2/2     Running     0             19d
longhorn-system   longhorn-manager-t9jlz                                            2/2     Running     0             19d
longhorn-system   longhorn-ui-7f7b9f785f-879kc                                      1/1     Running     0             19d
longhorn-system   longhorn-ui-7f7b9f785f-pq6m6                                      1/1     Running     0             19d
prometheus        alertmanager-prometheus-kube-prometheus-alertmanager-0            2/2     Running     0             12d
prometheus        prometheus-grafana-bfc8bdb48-tvhzb                                3/3     Running     0             12d
prometheus        prometheus-kube-prometheus-operator-df5494fb5-fl7ds               1/1     Running     0             12d
prometheus        prometheus-kube-state-metrics-86847bb8bc-rl6sk                    1/1     Running     0             12d
prometheus        prometheus-prometheus-kube-prometheus-prometheus-0                2/2     Running     0             12d
prometheus        prometheus-prometheus-node-exporter-7l6d8                         1/1     Running     0             45h
prometheus        prometheus-prometheus-node-exporter-cw5ft                         1/1     Running     0             12d
prometheus        prometheus-prometheus-node-exporter-j4tjb
```

- Storage class configured

```bash
kubectl get sc
NAME                 PROVISIONER             RECLAIMPOLICY   VOLUMEBINDINGMODE      ALLOWVOLUMEEXPANSION   AGE
local-path           rancher.io/local-path   Delete          WaitForFirstConsumer   true                   13d
longhorn (default)   driver.longhorn.io      Delete          Immediate              true                   19d
longhorn-static      driver.longhorn.io      Delete          Immediate              true                   19d

```

Check Available resource on Nodes:

```yaml
Capacity:
  cpu: 192
  ephemeral-storage: 1844284980Ki
  hugepages-1Gi: 0
  hugepages-2Mi: 0
  memory: 1056290728Ki
  nvidia.com/gpu: 8
  pods: 110
Allocatable:
  cpu: 192
  ephemeral-storage: 1699693034754
  hugepages-1Gi: 0
  hugepages-2Mi: 0
  memory: 1056188328Ki
  nvidia.com/gpu: 8
  pods: 110
```

Create PVC for Model weights storage

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: k2-think-cache-pvc
  namespace: k2-think
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 200Gi
  storageClassName: local-path # Use the appropriate storage class in your cluster
```

### Grok2 Deployement Manifest file

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: k2-think
  namespace: k2-think
  labels:
    app: k2-think
spec:
  replicas: 1
  selector:
    matchLabels:
      app: k2-think
  template:
    metadata:
      labels:
        app: k2-think
    spec:
      containers:
        - name: vllm
          image: vllm/vllm-openai:v0.10.1.1
          imagePullPolicy: IfNotPresent
          command:
            - vllm
            - serve
          args:
            - LLM360/K2-Think
            - --host
            - 0.0.0.0
            - --port
            - "8000"
            - --tensor-parallel-size
            - "4"
            - --gpu-memory-utilization
            - "0.92"
            - --max-model-len
            - "65536"
          env:
            - name: LOG_LEVEL
              value: DEBUG
            - name: TIKTOKEN_RS_CACHE_DIR
              value: /vllm-workspace
          ports:
            - name: http
              containerPort: 8000
              protocol: TCP
          resources:
            requests:
              nvidia.com/gpu: "4"
            limits:
              nvidia.com/gpu: "4"
          volumeMounts:
            - name: cache-volume
              mountPath: /root/.cache/huggingface
            - name: shm
              mountPath: /dev/shm
          # Health probes
          livenessProbe:
            httpGet:
              path: /health
              port: http
              scheme: HTTP
            initialDelaySeconds: 1200
            periodSeconds: 15
            timeoutSeconds: 5
            failureThreshold: 6
            successThreshold: 1
          readinessProbe:
            httpGet:
              path: /health
              port: http
              scheme: HTTP
            initialDelaySeconds: 1200
            periodSeconds: 10
            timeoutSeconds: 5
            failureThreshold: 12
            successThreshold: 1
      volumes:
        - name: cache-volume
          persistentVolumeClaim:
            claimName: k2-think-cache-pvc
        - name: shm
          emptyDir:
            medium: Memory
            sizeLimit: 32Gi
```
