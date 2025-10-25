# On-Prem Deployment of OpenAI 120B Model using vllm

**Author:** [Shivank Chaudhary](https://www.linkedin.com/in/shivank1128/)

**Published:** August 10, 2025

OpenAI just dropped 2 open models, i.e, 20B and 120B models.

Reference Links:

- [openai/gpt-oss-20b](https://huggingface.co/openai/gpt-oss-20b?source=post_page-----686734ecf8c7---------------------------------------)
- [openai/gpt-oss-120b](https://huggingface.co/openai/gpt-oss-120b?source=post_page-----686734ecf8c7---------------------------------------)

This deployment guide provides an on-premise AI chat system using OpenAI open-source models served via vLLM for high-performance inferencing.

The setup is GPU-accelerated with NVIDIA GPUs for faster response times and integrated with OpenWebUI to provide a web-based chat interface.

This guide will walk you through the deployment of OpenAI OSS Models

## Deployment

Make sure you have a K8s cluster with NVidia GPU operator installed:

```bash
NAME                                                           READY   STATUS      RESTARTS       AGE
gpu-feature-discovery-v2xpk                                    1/1     Running     0              4d8h
gpu-operator-644fb64985-ffzws                                  1/1     Running     0              4d8h
gpu-operator-node-feature-discovery-gc-6b54df9879-r49xs        1/1     Running     0              4d8h
gpu-operator-node-feature-discovery-master-56d87c5b58-rrgsn    1/1     Running     0              4d8h
gpu-operator-node-feature-discovery-worker-gsd2l               1/1     Running     0              4d8h
nvidia-container-toolkit-daemonset-kgp82                       1/1     Running     0              4d8h
nvidia-cuda-validator-2qpb2                                    0/1     Completed   0              4d8h
nvidia-dcgm-exporter-bxvrt                                     1/1     Running     0              4d8h
nvidia-device-plugin-daemonset-bvqt5                           1/1     Running     0              4d8h
nvidia-driver-daemonset-5.15.0-140-generic-ubuntu22.04-x45xq   2/2     Running     3 (4d8h ago)   4d8h
nvidia-mig-manager-h2vjg                                       1/1     Running     0              4d8h
nvidia-operator-validator-4r42f                                1/1     Running     0              4d8h
```

### Node GPU resources

```yaml
Capacity:
  cpu: 192
  ephemeral-storage: 1844284980Ki
  hugepages-1Gi: 0
  hugepages-2Mi: 0
  memory: 1056290768Ki
  nvidia.com/gpu: 8
  pods: 110
Allocatable:
  cpu: 192
  ephemeral-storage: 1699693034754
  hugepages-1Gi: 0
  hugepages-2Mi: 0
  memory: 1056188368Ki
  nvidia.com/gpu: 8
  pods: 110
```

### Prepare vLLM deployment

#### 120B Model

PVC for Model storage:

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: vllm-cache-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 250Gi
  volumeMode: Filesystem
```

vLLM deployment:

> NOTE: Fill the proxy details, if your system is behind proxy

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: vllm-server
  name: vllm-server
spec:
  replicas: 1
  selector:
    matchLabels:
      app: vllm-server
  template:
    metadata:
      labels:
        app: vllm-server
    spec:
      hostIPC: true
      volumes:
        - name: cache-volume
          persistentVolumeClaim:
            claimName: vllm-cache-pvc
        - name: shm
          emptyDir:
            medium: Memory
            sizeLimit: "32Gi"
      containers:
        - name: vllm-gptoss
          image: vllm/vllm-openai:gptoss
          command:
            - "vllm"
            - "serve"
            - "openai/gpt-oss-120b"
            - "--host"
            - "0.0.0.0"
            - "--port"
            - "8000"
            - "--gpu-memory-utilization"
            - "0.90"
            - "--max-model-len"
            - "80000"
          ports:
            - containerPort: 8000
          resources:
            requests:
              nvidia.com/gpu: 1
            limits:
              nvidia.com/gpu: 1
          volumeMounts:
            - mountPath: /root/.cache/huggingface
              name: cache-volume
            - mountPath: /dev/shm
              name: shm
          env:
            - name: LOG_LEVEL
              value: "DEBUG"
            - name: TIKTOKEN_RS_CACHE_DIR
              value: "/vllm-workspace"
            - name: HTTP_PROXY
              value: "<Proxy Setting for your env>"
            - name: HTTPS_PROXY
              value: "<Proxy Setting for your env>"
            - name: NO_PROXY
              value: "localhost,127.0.0.1"
          securityContext:
            privileged: true
```

#### 20B Model

PVC for Model:

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: vllm-cache-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 250Gi
  volumeMode: Filesystem
```

vLLM deployment:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: vllm-server
  name: vllm-server
spec:
  replicas: 1
  selector:
    matchLabels:
      app: vllm-server
  template:
    metadata:
      labels:
        app: vllm-server
    spec:
      hostIPC: true
      volumes:
        - name: cache-volume
          persistentVolumeClaim:
            claimName: vllm-cache-pvc
        - name: shm
          emptyDir:
            medium: Memory
            sizeLimit: "32Gi"
      containers:
        - name: vllm-gptoss
          image: vllm/vllm-openai:gptoss
          command:
            - "vllm"
            - "serve"
            - "openai/gpt-oss-20b"
            - "--host"
            - "0.0.0.0"
            - "--port"
            - "8000"
            - "--gpu-memory-utilization"
            - "0.90"
            - "--max-model-len"
            - "50000"
          ports:
            - containerPort: 8000
          resources:
            requests:
              nvidia.com/gpu: 6
            limits:
              nvidia.com/gpu: 6
          volumeMounts:
            - mountPath: /root/.cache/huggingface
              name: cache-volume
            - mountPath: /dev/shm
              name: shm
          env:
            - name: LOG_LEVEL
              value: "DEBUG"
            - name: TIKTOKEN_RS_CACHE_DIR
              value: "/vllm-workspace"
            - name: HTTP_PROXY
              value: "<Proxy Setting for your env>"
            - name: HTTPS_PROXY
              value: "<Proxy Setting for your env>"
            - name: NO_PROXY
              value: "localhost,127.0.0.1"
          securityContext:
            privileged: true
```

Service to Access Model

```yaml
apiVersion: v1
kind: Service
metadata:
  name: vllm-service
spec:
  selector:
    app: vllm-server
  ports:
    - protocol: TCP
      port: 8000
      targetPort: 8000
  type: NodePort
```

### Service to Access Model

```yaml
apiVersion: v1
kind: Service
metadata:
  name: vllm-service
spec:
  selector:
    app: vllm-server
  ports:
    - protocol: TCP
      port: 8000
      targetPort: 8000
  type: NodePort
```

Validate working of LLM model via API call:

```bash
curl --noproxy "*" \
  -X POST http://172.21.162.11:32513/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "openai/gpt-oss-120b",
    "messages": [{"role": "user", "content": "Hello, how are you?"}],
    "temperature": 2.0
  }'
```

Response:

```json
{
  "id": "chatcmpl-...",
  "object": "chat.completion",
  "created": 1754658263,
  "model": "openai/gpt-oss-120b",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Hello! I'm doing great, thanks for asking. How about you?"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": { "prompt_tokens": 77, "completion_tokens": 68, "total_tokens": 145 }
}
```

Great, Model is deployed and working fine.

### OpenWeb UI (Optional)

Deployment:

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: open-webui-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: open-webui
  labels:
    app: open-webui
spec:
  replicas: 1
  selector:
    matchLabels:
      app: open-webui
  template:
    metadata:
      labels:
        app: open-webui
    spec:
      containers:
        - name: open-webui
          image: ghcr.io/open-webui/open-webui:main
          ports:
            - containerPort: 8080
          env:
            - name: OPENAI_API_BASE_URL
              value: "http://vllm-service:8000/v1"
            - name: OPENAI_API_KEY
              value: "test"
            - name: ENABLE_OLLAMA_API
              value: "false"
            - name: ENABLE_RAG_WEB_SEARCH
              value: "false"
          volumeMounts:
            - name: open-webui-data
              mountPath: /app/backend/data
      volumes:
        - name: open-webui-data
          persistentVolumeClaim:
            claimName: open-webui-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: open-webui
spec:
  type: NodePort
  selector:
    app: open-webui
  ports:
    - port: 80
      targetPort: 8080
      protocol: TCP
```

> Dashboard can be accessed on NodePort.

### Reference

- https://openai.com/index/introducing-gpt-oss/
