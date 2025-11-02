# Deploying a Production-Ready VLLM Stack on Kubernetes with HPA Autoscaling

**Author:** [Shivank Chaudhary](https://www.linkedin.com/in/shivank1128/)

**Published:** November 1, 2025

---

Running large language models (LLMs) in production requires careful orchestration of resources, efficient scaling mechanisms, and robust infrastructure. In this guide, I’ll walk you through deploying a multi-model VLLM (Very Large Language Model) stack on Kubernetes with Horizontal Pod Autoscaling (HPA), based on our battle-tested production configuration.

This setup has been successfully managing multiple LLMs from OpenAI, Meta, Qwen, and Google, serving production traffic with automatic scaling based on demand.

---

## Why VLLM?

VLLM is a fast and memory-efficient inference engine designed specifically for LLMs. It provides:

- High throughput serving with PagedAttention
- Continuous batching of incoming requests
- Optimized CUDA kernels for better GPU utilization
- OpenAI-compatible API endpoints

---

## Architecture Overview

Our production stack consists of three key components:

- **Multiple Model Deployments**: Each LLM runs in its own deployment with dedicated resources and configuration tailored to the model’s requirements.
- **Router Service**: A lightweight router that distributes incoming requests across model instances and handles load balancing.
- **Autoscaling Infrastructure**: HPA configuration that scales deployments based on custom Prometheus metrics, specifically monitoring the number of waiting requests.

---

## Prerequisites

Before diving into the deployment, ensure you have:

- A Kubernetes cluster with GPU nodes
- Helm 3.x installed
- Prometheus operator for custom metrics (required for HPA)
- A storage class that supports ReadWriteMany (RWX) access mode
- Hugging Face tokens for model downloads

---

## Installation Guide

### Step 1: Add the Repository

```
helm repo add vllm https://vllm-project.github.io/production-stack
```

---

### Step 2: Understanding the Configuration

Let me break down the key configuration parameters for each model:

```
- name: "gptoss-20b"
  repository: "vllm/vllm-openai" # VLLM image supporting your model
  tag: "latest"
  modelURL: "openai/gpt-oss-20b" # Hugging Face model identifier
  replicaCount: 1 # Minimum replicas
  requestCPU: 10
  requestMemory: "64Gi"
  requestGPU: 1
  pvcStorage: "250Gi"
  pvcAccessMode:
    - ReadWriteMany # Critical for fast scaling!
```

**Important Note**: Using `ReadWriteMany` (RWX) access mode is crucial when HPA is enabled. This allows multiple pods to mount the same persistent volume simultaneously, dramatically reducing scaling time since new pods don't need to re-download the model weights.

---

### Step 3: VLLM Configuration Deep Dive

Each model has specific VLLM runtime configurations:

```
vllmConfig:
  enableChunkedPrefill: false
  enablePrefixCaching: false
  dtype: "bfloat16"
  extraArgs: ["--disable-log-requests", "--gpu-memory-utilization", "0.8"]
```

**Key Parameters**:

- `dtype`: Using `bfloat16` provides a good balance between performance and memory usage
- `gpu-memory-utilization`: Set to 0.8-0.85 to leave headroom for CUDA operations
- `tensorParallelSize`: For larger models requiring multiple GPUs (e.g., 120B model uses 4 GPUs)
- `maxModelLen`: Context window size, adjust based on your use case

---

### Step 4: Autoscaling Configuration

Please refer to keda autoscaling guide for HPA:

https://docs.vllm.ai/projects/production-stack/en/latest/use_cases/autoscaling-keda.html

---

## Production Model Examples

### Small Model: Llama 3.1 8B Instruct

Ideal for cost-effective inference with good performance:

```
- name: "meta-llama-31-8b-instruct"
  repository: "vllm/vllm-openai"
  tag: "latest"
  modelURL: "meta-llama/Llama-3.1-8B-Instruct"
  replicaCount: 1
  requestCPU: 8
  requestMemory: "32Gi"
  requestGPU: 1
  pvcStorage: "100Gi"
  vllmConfig:
    maxModelLen: 80000
    dtype: "bfloat16"
    extraArgs: ["--disable-log-requests", "--gpu-memory-utilization", "0.85"]
```

### Large Model: GPT-OSS 120B

For high-quality outputs requiring significant compute:

```
- name: "gptoss-120b"
  repository: "vllm/vllm-openai"
  tag: "latest"
  modelURL: "openai/gpt-oss-120b"
  replicaCount: 1
  requestCPU: 16
  requestMemory: "128Gi"
  requestGPU: 4 # Multi-GPU setup
  pvcStorage: "600Gi"
  vllmConfig:
    tensorParallelSize: 4 # Parallel across 4 GPUs
    dtype: "bfloat16"
    extraArgs: ["--disable-log-requests", "--gpu-memory-utilization", "0.85"]
```

### Embedding Model: Qwen3 Embedding 8B

Perfect for semantic search and RAG applications:

```
- name: "qwen3-embedding-8b"
  repository: "vllm/vllm-openai"
  tag: "latest"
  modelURL: "Qwen/Qwen3-Embedding-8B"
  replicaCount: 1
  requestCPU: 16
  requestMemory: "64Gi"
  requestGPU: 1
  pvcStorage: "100Gi"
  vllmConfig:
    maxModelLen: 32768
    dtype: "bfloat16"
    extraArgs: ["--disable-log-requests", "--gpu-memory-utilization", "0.85"]
```

### Multimodal Model: Qwen3 Omni

Audio-visual-text multimodal model with custom CUDA image:

```
- name: "qwen3-omni"
  repository: "qwenllm/qwen3-omni" # Custom repository
  tag: "3-cu124" # CUDA 12.4 optimized
  modelURL: "Qwen/Qwen3-Omni-30B-A3B-Instruct"
  replicaCount: 1
  requestCPU: 24
  requestMemory: "128Gi"
  requestGPU: 1
  pvcStorage: "100Gi"
  vllmConfig:
    tensorParallelSize: 1
    maxModelLen: 32768 # 32768 for 1 GPU, 65536 for 4 GPUs
    dtype: "bfloat16"
    extraArgs: ["--disable-log-requests", "--gpu-memory-utilization", "0.90"]
```

### Reasoning Model: LLM360 K2-Think

Specialized for complex reasoning tasks:

```
- name: "llm360-k2-think"
  repository: "vllm/vllm-openai"
  tag: "v0.10.1.1" # Specific version for compatibility
  modelURL: "LLM360/K2-Think"
  replicaCount: 1
  requestCPU: 16
  requestMemory: "64Gi"
  requestGPU: 4
  pvcStorage: "100Gi"
  vllmConfig:
    tensorParallelSize: 4
    maxModelLen: 65536
    dtype: "bfloat16"
    extraArgs: ["--disable-log-requests", "--gpu-memory-utilization", "0.85"]
```

### Vision-Language Model: Qwen3 Thinking

Large-scale multimodal reasoning model:

```
- name: "qwen3-thinking"
  repository: "vllm/vllm-openai"
  tag: "latest"
  modelURL: "Qwen/Qwen3-VL-235B-A22B-Thinking"
  replicaCount: 1
  requestCPU: 32
  requestMemory: "256Gi"
  requestGPU: 4 # Requires 4 GPUs
  pvcStorage: "900Gi" # Large storage for weights
  vllmConfig:
    tensorParallelSize: 4
    dtype: "bfloat16"
    extraArgs: ["--disable-log-requests", "--gpu-memory-utilization", "0.95"]
```

### Vision-Language Model: Qwen3 Instruct

High-performance multimodal instruction-following model:

```
- name: "qwen3-instruct"
  repository: "vllm/vllm-openai"
  tag: "latest"
  modelURL: "Qwen/Qwen3-VL-235B-A22B-Instruct"
  replicaCount: 1
  requestCPU: 32
  requestMemory: "256Gi"
  requestGPU: 4
  pvcStorage: "800Gi"
  vllmConfig:
    tensorParallelSize: 4
    dtype: "bfloat16"
    extraArgs: ["--disable-log-requests", "--gpu-memory-utilization", "0.9"]
```

---

## Router Configuration

The router handles incoming traffic and distributes it across model instances:

```
routerSpec:
  replicaCount: 1
  autoscaling:
    enabled: true
    minReplicas: 1
    maxReplicas: 10
    targetCPUUtilizationPercentage: 80
  resources:
    requests:
      cpu: 400m
      memory: 700Mi
    limits:
      memory: 700Mi
```

The router is lightweight and scales independently based on CPU utilization.

---

## Deployment

### Deploy the Stack

```
helm install vllm vllm -f prod-values.yaml -n vllm --install --create-namespace
```

### Verify Deployment

Check your pods:

```
kubectl get pods -n vllm
```

Expected output:

```
NAME READY STATUS RESTARTS AGE
vllm-deployment-router-5bc8f96685-284m4 1/1 Running 0 8d
vllm-gemma-3-27b-it-deployment-vllm-9d9f8b554-cdlvj 1/1 Running 2 8d
vllm-gptoss-120b-deployment-vllm-d75bdcc7f-zprkb 1/1 Running 6 7d
vllm-qwen3-omni-deployment-vllm-85bfc6dfc7-jb59f 1/1 Running 0 26h
```

Check HPA status:

```
kubectl get hpa -n vllm
```

Expected output:

```
NAME REFERENCE TARGETS MINPODS MAXPODS REPLICAS
vllm-gptoss-120b-hpa Deployment/vllm-gptoss-120b-deployment-vllm 0/20 1 2 1
vllm-router-hpa Deployment/vllm-deployment-router cpu: 2%/80% 3 10 3
```

---

## Best Practices and Lessons Learned

### Storage Strategy

**Always use ReadWriteMany (RWX) for model weights**: This is perhaps the most critical optimization. When a new pod spins up during scaling, it can immediately access the pre-downloaded model weights. Without RWX, each pod would need to download 100GB+ of weights, adding 5–10 minutes to scaling time.

### GPU Memory Utilization

Start with 0.8 (80%) GPU memory utilization and adjust based on OOM errors. Larger models can often push to 0.85, but leave some headroom.

### Scaling Behavior

Our aggressive scale-up (0 second stabilization) combined with conservative scale-down (10 minutes) prevents request queuing during traffic spikes while avoiding unnecessary pod churn during temporary dips.

### Model Selection

Choose your models wisely:

- 8B models for cost-effective, high-throughput workloads
- 27B models for balanced quality and performance
- 120B+ models only when output quality justifies the cost

### Resource Requests

Set realistic CPU and memory requests. Underprovisioning leads to OOMKills; overprovisioning wastes cluster resources.

### Monitoring and Observability

Key metrics to watch:

- `vllm_num_requests_waiting`: Primary scaling trigger
- `vllm_num_requests_running`: Current load
- GPU utilization: Should stay high but not maxed out
- Time to scale: Monitor how long new pods take to become ready

### Cost Optimization Tips

1. **Right-size your models**: Don’t use a 120B model when an 8B model suffices
2. **Use spot instances**: For non-critical workloads, GPU spot instances can save 60–80%
3. **Aggressive scale-to-zero**: Consider scaling to zero replicas during off-peak hours
4. **Batch requests**: VLLM’s continuous batching is most efficient with multiple concurrent requests

---

## Conclusion

Running a production VLLM stack requires careful attention to resource allocation, storage configuration, and autoscaling policies. The configuration shared here has proven stable and cost-effective for serving multiple models under varying load conditions.

**Key takeaways:**

- Use ReadWriteMany storage for fast scaling
- Configure aggressive scale-up, conservative scale-down
- Monitor the right metrics (waiting requests, not just CPU/memory)
- Choose appropriate models for your use case
- Leave GPU memory headroom for stability

This setup has been serving production traffic reliably for weeks, automatically handling traffic spikes and optimizing resource usage during quiet periods.

---

## Next Steps

- Implement request queuing and prioritization
- Integrate with litellm for router optimization and token metering
- Add model caching for frequently accessed weights
- Set up comprehensive monitoring dashboards
- Implement blue-green deployments for model updates
- Explore multi-cluster deployments for high availability

