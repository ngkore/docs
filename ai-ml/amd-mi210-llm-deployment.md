# Running LLMs on AMD MI210 GPUs with vLLM and Kubernetes: A Deployment Guide

**Author:** [Shivank Chaudhary](https://www.linkedin.com/in/shivank1128/)

**Published:** Jun 9, 2026

*Chat, embedding, and speech models on AMD Instinct MI210 (gfx90a) — with the full manifests and the version/quantization decisions that actually matter.*

If you've got a cluster of **AMD Instinct MI210** cards and you want to serve open LLMs on them, here's the honest summary: it works well, but nearly every image, guide, and "day 0 support" headline out there is written for the newer **MI300-class cards** — and a few of those assumptions quietly break on the MI210.

This guide gives you the working manifests for six models, and — just as importantly — explains *why* each choice was made: which vLLM image, why not the newest version, and the FP8/MXFP4 story that decides what you can even run. If you're on MI210 (or its dual-die cousin the MI250, same chip), this should get you serving quickly.

## TL;DR

- The MI210 is **gfx90a** (CDNA2). Fully supported by ROCm and vLLM, but **not** part of the MI300-era "day 0" optimized story.
- **It has no native FP8 or MXFP4.** This single fact decides which models and checkpoints you can run.
- Use a **pinned** AMD `rocm/vllm` image — not the latest vLLM — and set `VLLM_USE_AITER=0`.
- For MXFP4-native models like gpt-oss, use **BF16 upcasts** (e.g. unsloth's) to route around the missing format.
- Full copy-paste manifests for all six models are below.

## Part 1: The "day 0 support" reality check

AMD's same-day support announcements for new models are real — but the fine print targets **MI355X, MI350X, MI325X, and MI300X**. The MI210 isn't on that list.

That doesn't mean MI210 is unsupported. gfx90a is a first-class CI target for vLLM's ROCm backend. It means:

- No AMD-branded "optimized" prebuilt images tuned for your card.
- No newest FP8/FP4 kernels or AITER fast paths — those target gfx942+ (MI300).
- "Day 0 supported in vLLM" means a model's *architecture* merged on launch day. That's architecture-agnostic Python — it'll generally **load** on gfx90a, but only if it doesn't need a numeric format or kernel your card lacks.

Which brings us to the one constraint that shapes everything.

## Part 2: The MXFP4 and FP8 story — and why we used unsloth weights

This is the most important section in the guide, so let me be concrete.

Modern frontier models are increasingly shipped in **low-precision formats** to fit on fewer GPUs. Two show up constantly:

- **FP8** (8-bit float) — many DeepSeek checkpoints.
- **MXFP4** (4-bit microscaling) — this is how **gpt-oss** fits 120B parameters onto a single 80 GB H100.

The MI210 (gfx90a) supports **neither** in the way these checkpoints assume. If you try to serve a model whose weights are published *only* in FP8, vLLM fails with a beautifully specific error:

```console
ValueError: type fp8e4b8 not supported in this architecture.
The supported fp8 dtypes are ('fp8e5',)
```

That's the GPU telling you it doesn't have the `e4m3` FP8 datatype the checkpoint needs. MXFP4 is the same story — gfx90a has no kernels for it.

So your model-selection rule is simple:

> ***Run BF16/FP16 weights, or INT4 (AWQ/GPTQ) quants. Avoid FP8/MXFP4-native checkpoints.***

That sounds like it rules out gpt-oss entirely. Here's the trick that saved it:

### Using unsloth's BF16 weights

The community (unsloth, among others) publishes **BF16 upcasts** of MXFP4 models. These take every 4-bit MXFP4 weight and expand it back to full BF16. The model is numerically the same architecture — it just no longer requires the MXFP4 kernels your card doesn't have.

The trade-off is **size**. MXFP4 is 4 bits/weight; BF16 is 16. So a BF16 upcast is roughly 4× larger:

- `unsloth/gpt-oss-20b-BF16` → ~42 GB (fits one card)
- `unsloth/gpt-oss-120b-BF16` → ~230 GB (needs ~4 cards via tensor-parallel)

But it *runs*. I had gpt-oss-20b-BF16 generating coherent text on MI210 — a model I'd assumed was off-limits because of MXFP4. The lesson generalizes:

> *When a model "doesn't support" your GPU, the blocker is usually the **numeric format**, not the architecture. Find a BF16 or INT4 repackaging and you're often back in business — you just pay for it in VRAM.*

The models in this guide, all BF16 and all gfx90a-friendly: **Qwen3-32B**, **Mixtral-8x7B**, **gpt-oss-20b/120b (BF16 upcasts)**, **Qwen3-Embedding-8B**, and **Whisper-large-v3**.

## Part 3: The image story — what's inside, and why not the latest vLLM

I used:

```text
rocm/vllm:rocm6.4.1_vllm_0.10.1_20250909
```

Decode the tag: **ROCm 6.4.1**, **vLLM 0.10.1**, built **2025-09-09**. These AMD-published images are *curated combinations* — a ROCm userspace, a PyTorch built against that exact ROCm, vLLM, Triton, the OpenAI-compatible server, and CK flash-attention, all known to work together.

### What comes with it (and what to watch on gfx90a)

- A **PyTorch built for a multi-arch list that includes gfx90a** — so your MI210 kernels are present.
- **AITER** is in there, but built for **gfx942/gfx950 only** (MI300-class). On gfx90a it has no kernels, so you must disable it (`VLLM_USE_AITER=0`) or you'll hit runtime dispatch errors.
- A full ROCm 6.4.1 runtime — which means your **node's ROCm driver should be ≥ 6.4.1**. A node older than the image is the most common "it loads but crashes" cause. Match them.

### Why not the latest vLLM?

It's tempting to grab the newest vLLM (0.2x at time of writing) for the freshest model support. Don't, at least not blindly, and here's the reasoning:

1. **gfx90a isn't in vLLM's hot CI path.** The project's momentum is firmly toward MI300+ and CUDA. Newer releases regularly deprecate or refactor older code paths, and a regression on gfx90a can ship unnoticed because nobody's testing MI210 on every PR. A release that's a little older has had time to bake.
2. **The curated combo matters more than the version number.** Pulling the latest vLLM via `pip` into a base with a mismatched ROCm/PyTorch is a great way to spend an afternoon debugging ABI errors. The AMD prebuilt image hands you a ROCm+torch+vLLM trio that was validated together.
3. **0.10.1 was new enough.** It's a September 2025 build — after gpt-oss's release — so it already knew about the architectures I cared about. The cost of pinning an older version is missing the very newest model types; for everything in this guide, it wasn't a problem.
4. **Reproducibility.** Pin the image (ideally by digest) so what you validated is exactly what you ship.

The rule of thumb: a known-good pinned image that already contains gfx90a beats chasing `latest` every time — for an older architecture especially.

## Two env vars, every pod

```yaml
env:
  - { name: VLLM_USE_AITER, value: "0" }              # AITER's FP8 kernels don't exist on gfx90a
  - { name: VLLM_USE_TRITON_FLASH_ATTN, value: "1" }  # Triton flash-attn = the safe gfx90a path
```

## One entrypoint quirk

The `rocm/vllm:*` images don't auto-launch the server, so set an explicit `command: ["vllm", "serve", "<model>", ...]`. (The upstream `vllm/vllm-openai-rocm` image is the opposite — its entrypoint *is* the server, so you'd pass `--model ...` directly. Mixing these up means the container starts and does nothing.)

## Part 4: Deployment fundamentals

Install the **AMD GPU Operator** first — it advertises the `amd.com/gpu` schedulable resource.

**Sizing.** Each MI210 presents as **one 64 GB device**, so `amd.com/gpu: N` = N cards, and `--tensor-parallel-size N` spans them. Rough BF16 math (≈2 bytes/param):

| Model | Weights | Cards (TP) |
|---|---|---|
| Qwen3-Embedding-8B | ~16 GB | 1 |
| Whisper-large-v3 | ~3 GB | 1 |
| Qwen3-32B | ~64 GB | 2 |
| Mixtral-8x7B | ~93 GB | 2 |
| gpt-oss-20b-BF16 | ~42 GB | 2 |
| gpt-oss-120b-BF16 | ~230 GB | 8 |

`--enforce-eager` is recommended on gfx90a (skips HIP graph capture — saves memory, dodges a class of issues), and give each pod a real `/dev/shm` for tensor-parallel comms.

## Part 5: The manifests

All six assume namespace `llm` and a Hugging Face token secret (gated models like Qwen3 and Mixtral need it):

```bash
kubectl create namespace llm
kubectl create secret generic hf-token-secret -n llm --from-literal=token=hf_xxxxxxxx
```

PVCs below use `storageClassName: local-path` — swap in whatever StorageClass your cluster has.

### 1. Qwen3-32B (chat, TP=2)

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata: { name: cache-qwen3-32b, namespace: llm }
spec:
  accessModes: ["ReadWriteOnce"]
  storageClassName: local-path
  resources: { requests: { storage: 120Gi } }

apiVersion: apps/v1
kind: Deployment
metadata: { name: qwen3-32b, namespace: llm, labels: { app: qwen3-32b } }
spec:
  replicas: 1
  selector: { matchLabels: { app: qwen3-32b } }
  template:
    metadata: { labels: { app: qwen3-32b } }
    spec:
      securityContext: { supplementalGroups: [44, 109] }   # video/render gids; verify per node
      volumes:
        - { name: cache, persistentVolumeClaim: { claimName: cache-qwen3-32b } }
        - { name: shm, emptyDir: { medium: Memory, sizeLimit: 16Gi } }
      containers:
        - name: vllm
          image: rocm/vllm:rocm6.4.1_vllm_0.10.1_20250909
          command: ["vllm","serve","Qwen/Qwen3-32B",
                    "--tensor-parallel-size=2","--dtype=bfloat16",
                    "--max-model-len=32768","--gpu-memory-utilization=0.92",
                    "--enforce-eager","--port=8000"]
          securityContext:
            capabilities: { add: ["SYS_PTRACE"] }
            seccompProfile: { type: Unconfined }
          env:
            - { name: VLLM_USE_AITER, value: "0" }
            - { name: VLLM_USE_TRITON_FLASH_ATTN, value: "1" }
            - { name: HUGGING_FACE_HUB_TOKEN, valueFrom: { secretKeyRef: { name: hf-token-secret, key: token } } }
          ports: [ { containerPort: 8000 } ]
          resources: { limits: { amd.com/gpu: "2" } }
          volumeMounts:
            - { name: cache, mountPath: /root/.cache/huggingface }
            - { name: shm, mountPath: /dev/shm }
          startupProbe:   { httpGet: { path: /health, port: 8000 }, periodSeconds: 15, failureThreshold: 80 }
          readinessProbe: { httpGet: { path: /health, port: 8000 }, periodSeconds: 10 }

apiVersion: v1
kind: Service
metadata: { name: qwen3-32b, namespace: llm }
spec:
  selector: { app: qwen3-32b }
  ports: [ { port: 8000, targetPort: 8000 } ]
```

Every other manifest follows this exact shape — only the model, `--tensor-parallel-size`, `amd.com/gpu`, and a couple of flags change. Test any chat model with:

```bash
kubectl exec -n llm deploy/qwen3-32b  curl -s http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"Qwen/Qwen3-32B","messages":[{"role":"user","content":"Say hi"}],"max_tokens":32}'
```

### 2. Mixtral-8x7B-Instruct (chat, TP=2)

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata: { name: cache-mixtral-8x7b, namespace: llm }
spec:
  accessModes: ["ReadWriteOnce"]
  storageClassName: local-path
  resources: { requests: { storage: 200Gi } }

apiVersion: apps/v1
kind: Deployment
metadata: { name: mixtral-8x7b, namespace: llm, labels: { app: mixtral-8x7b } }
spec:
  replicas: 1
  selector: { matchLabels: { app: mixtral-8x7b } }
  template:
    metadata: { labels: { app: mixtral-8x7b } }
    spec:
      securityContext: { supplementalGroups: [44, 109] }
      volumes:
        - { name: cache, persistentVolumeClaim: { claimName: cache-mixtral-8x7b } }
        - { name: shm, emptyDir: { medium: Memory, sizeLimit: 16Gi } }
      containers:
        - name: vllm
          image: rocm/vllm:rocm6.4.1_vllm_0.10.1_20250909
          command: ["vllm","serve","mistralai/Mixtral-8x7B-Instruct-v0.1",
                    "--tensor-parallel-size=2","--dtype=bfloat16",
                    "--max-model-len=8192","--gpu-memory-utilization=0.90",
                    "--enforce-eager","--port=8000"]
          securityContext:
            capabilities: { add: ["SYS_PTRACE"] }
            seccompProfile: { type: Unconfined }
          env:
            - { name: VLLM_USE_AITER, value: "0" }
            - { name: VLLM_USE_TRITON_FLASH_ATTN, value: "1" }
            - { name: HUGGING_FACE_HUB_TOKEN, valueFrom: { secretKeyRef: { name: hf-token-secret, key: token } } }
          ports: [ { containerPort: 8000 } ]
          resources: { limits: { amd.com/gpu: "2" } }
          volumeMounts:
            - { name: cache, mountPath: /root/.cache/huggingface }
            - { name: shm, mountPath: /dev/shm }
          startupProbe:   { httpGet: { path: /health, port: 8000 }, periodSeconds: 15, failureThreshold: 80 }
          readinessProbe: { httpGet: { path: /health, port: 8000 }, periodSeconds: 10 }

apiVersion: v1
kind: Service
metadata: { name: mixtral-8x7b, namespace: llm }
spec:
  selector: { app: mixtral-8x7b }
  ports: [ { port: 8000, targetPort: 8000 } ]
```

> Mixtral is tight at TP=2 across two cards. If it OOMs or restart-loops on load, that's the first lever — drop `--max-model-len` to 8192 (done above) and `--gpu-memory-utilization` to 0.88.

### 3. gpt-oss-20b-BF16 (chat, TP=2)

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata: { name: cache-gpt-oss-20b, namespace: llm }
spec:
  accessModes: ["ReadWriteOnce"]
  storageClassName: local-path
  resources: { requests: { storage: 120Gi } }

apiVersion: apps/v1
kind: Deployment
metadata: { name: gpt-oss-20b, namespace: llm, labels: { app: gpt-oss-20b } }
spec:
  replicas: 1
  selector: { matchLabels: { app: gpt-oss-20b } }
  template:
    metadata: { labels: { app: gpt-oss-20b } }
    spec:
      securityContext: { supplementalGroups: [44, 109] }
      volumes:
        - { name: cache, persistentVolumeClaim: { claimName: cache-gpt-oss-20b } }
        - { name: shm, emptyDir: { medium: Memory, sizeLimit: 16Gi } }
      containers:
        - name: vllm
          image: rocm/vllm:rocm6.4.1_vllm_0.10.1_20250909
          command: ["vllm","serve","unsloth/gpt-oss-20b-BF16",
                    "--tensor-parallel-size=2","--dtype=bfloat16",
                    "--max-model-len=8192","--gpu-memory-utilization=0.90",
                    "--enforce-eager","--port=8000"]
          securityContext:
            capabilities: { add: ["SYS_PTRACE"] }
            seccompProfile: { type: Unconfined }
          env:
            - { name: VLLM_USE_AITER, value: "0" }
            - { name: VLLM_USE_TRITON_FLASH_ATTN, value: "1" }
            - { name: HUGGING_FACE_HUB_TOKEN, valueFrom: { secretKeyRef: { name: hf-token-secret, key: token } } }
          ports: [ { containerPort: 8000 } ]
          resources: { limits: { amd.com/gpu: "2" } }
          volumeMounts:
            - { name: cache, mountPath: /root/.cache/huggingface }
            - { name: shm, mountPath: /dev/shm }
          startupProbe:   { httpGet: { path: /health, port: 8000 }, periodSeconds: 15, failureThreshold: 80 }
          readinessProbe: { httpGet: { path: /health, port: 8000 }, periodSeconds: 10 }

apiVersion: v1
kind: Service
metadata: { name: gpt-oss-20b, namespace: llm }
spec:
  selector: { app: gpt-oss-20b }
  ports: [ { port: 8000, targetPort: 8000 } ]
```

> This is the MXFP4-upcast model from Part 2. Tip: gpt-oss puts its reasoning in a `reasoning_content` field — if `content` looks short, check both. A coherent reply here is your proof that the architecture runs on gfx90a.

### 4. gpt-oss-120b-BF16 (chat, TP=8 — needs 8 cards on one node)

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata: { name: cache-gpt-oss-120b, namespace: llm }
spec:
  accessModes: ["ReadWriteOnce"]
  storageClassName: local-path
  resources: { requests: { storage: 320Gi } }

apiVersion: apps/v1
kind: Deployment
metadata: { name: gpt-oss-120b, namespace: llm, labels: { app: gpt-oss-120b } }
spec:
  replicas: 1
  selector: { matchLabels: { app: gpt-oss-120b } }
  template:
    metadata: { labels: { app: gpt-oss-120b } }
    spec:
      securityContext: { supplementalGroups: [44, 109] }
      volumes:
        - { name: cache, persistentVolumeClaim: { claimName: cache-gpt-oss-120b } }
        - { name: shm, emptyDir: { medium: Memory, sizeLimit: 32Gi } }
      containers:
        - name: vllm
          image: rocm/vllm:rocm6.4.1_vllm_0.10.1_20250909
          command: ["vllm","serve","unsloth/gpt-oss-120b-BF16",
                    "--tensor-parallel-size=8","--dtype=bfloat16",
                    "--max-model-len=8192","--gpu-memory-utilization=0.92",
                    "--enforce-eager","--port=8000"]
          securityContext:
            capabilities: { add: ["SYS_PTRACE"] }
            seccompProfile: { type: Unconfined }
          env:
            - { name: VLLM_USE_AITER, value: "0" }
            - { name: VLLM_USE_TRITON_FLASH_ATTN, value: "1" }
            - { name: HUGGING_FACE_HUB_TOKEN, valueFrom: { secretKeyRef: { name: hf-token-secret, key: token } } }
          ports: [ { containerPort: 8000 } ]
          resources: { limits: { amd.com/gpu: "8" } }   # all 8 cards on ONE node
          volumeMounts:
            - { name: cache, mountPath: /root/.cache/huggingface }
            - { name: shm, mountPath: /dev/shm }
          startupProbe:   { httpGet: { path: /health, port: 8000 }, periodSeconds: 20, failureThreshold: 120 }
          readinessProbe: { httpGet: { path: /health, port: 8000 }, periodSeconds: 15 }

apiVersion: v1
kind: Service
metadata: { name: gpt-oss-120b, namespace: llm }
spec:
  selector: { app: gpt-oss-120b }
  ports: [ { port: 8000, targetPort: 8000 } ]
```

> *The ~230 GB BF16 upcast is the price of running an MXFP4 model on a card without MXFP4. It needs eight MI210s in a single node — if you don't have that, this is the one model here that won't fit as-is.*

### 5. Qwen3-Embedding-8B (embeddings, TP=1)

Embedding models are a different task — note `--task embed` and the `/v1/embeddings` endpoint.

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata: { name: cache-qwen3-embed-8b, namespace: llm }
spec:
  accessModes: ["ReadWriteOnce"]
  storageClassName: local-path
  resources: { requests: { storage: 60Gi } }

apiVersion: apps/v1
kind: Deployment
metadata: { name: qwen3-embed-8b, namespace: llm, labels: { app: qwen3-embed-8b } }
spec:
  replicas: 1
  selector: { matchLabels: { app: qwen3-embed-8b } }
  template:
    metadata: { labels: { app: qwen3-embed-8b } }
    spec:
      securityContext: { supplementalGroups: [44, 109] }
      volumes:
        - { name: cache, persistentVolumeClaim: { claimName: cache-qwen3-embed-8b } }
        - { name: shm, emptyDir: { medium: Memory, sizeLimit: 8Gi } }
      containers:
        - name: vllm
          image: rocm/vllm:rocm6.4.1_vllm_0.10.1_20250909
          command: ["vllm","serve","Qwen/Qwen3-Embedding-8B",
                    "--task=embed",            # newer vLLM: --runner pooling
                    "--tensor-parallel-size=1","--dtype=bfloat16",
                    "--max-model-len=8192","--gpu-memory-utilization=0.85",
                    "--enforce-eager","--port=8000"]
          securityContext:
            capabilities: { add: ["SYS_PTRACE"] }
            seccompProfile: { type: Unconfined }
          env:
            - { name: VLLM_USE_AITER, value: "0" }
            - { name: VLLM_USE_TRITON_FLASH_ATTN, value: "1" }
            - { name: HUGGING_FACE_HUB_TOKEN, valueFrom: { secretKeyRef: { name: hf-token-secret, key: token } } }
          ports: [ { containerPort: 8000 } ]
          resources: { limits: { amd.com/gpu: "1" } }
          volumeMounts:
            - { name: cache, mountPath: /root/.cache/huggingface }
            - { name: shm, mountPath: /dev/shm }
          startupProbe:   { httpGet: { path: /health, port: 8000 }, periodSeconds: 15, failureThreshold: 60 }
          readinessProbe: { httpGet: { path: /health, port: 8000 }, periodSeconds: 10 }

apiVersion: v1
kind: Service
metadata: { name: qwen3-embed-8b, namespace: llm }
spec:
  selector: { app: qwen3-embed-8b }
  ports: [ { port: 8000, targetPort: 8000 } ]
```

Test it:

```bash
kubectl exec -n llm deploy/qwen3-embed-8b curl -s http://localhost:8000/v1/embeddings \
  -H "Content-Type: application/json" \
  -d '{"model":"Qwen/Qwen3-Embedding-8B","input":"hello world"}'
```

A healthy response has a `data[0].embedding` array (4096 floats for this model).

### 6. Whisper-large-v3 (speech-to-text, TP=1)

Whisper auto-detects as transcription, uses `--max-model-len 448`, and serves `/v1/audio/transcriptions`. **Do not** copy vLLM's example `kv_cache_dtype=fp8` — that's the FP8 wall again.

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata: { name: cache-whisper-v3, namespace: llm }
spec:
  accessModes: ["ReadWriteOnce"]
  storageClassName: local-path
  resources: { requests: { storage: 40Gi } }

apiVersion: apps/v1
kind: Deployment
metadata: { name: whisper-v3, namespace: llm, labels: { app: whisper-v3 } }
spec:
  replicas: 1
  selector: { matchLabels: { app: whisper-v3 } }
  template:
    metadata: { labels: { app: whisper-v3 } }
    spec:
      securityContext: { supplementalGroups: [44, 109] }
      volumes:
        - { name: cache, persistentVolumeClaim: { claimName: cache-whisper-v3 } }
        - { name: shm, emptyDir: { medium: Memory, sizeLimit: 8Gi } }
      containers:
        - name: vllm
          image: rocm/vllm:rocm6.4.1_vllm_0.10.1_20250909
          command: ["vllm","serve","openai/whisper-large-v3",
                    "--tensor-parallel-size=1","--dtype=bfloat16",
                    "--max-model-len=448","--gpu-memory-utilization=0.85",
                    "--enforce-eager","--port=8000"]
          securityContext:
            capabilities: { add: ["SYS_PTRACE"] }
            seccompProfile: { type: Unconfined }
          env:
            - { name: VLLM_USE_AITER, value: "0" }
            - { name: VLLM_USE_TRITON_FLASH_ATTN, value: "1" }
            - { name: HUGGING_FACE_HUB_TOKEN, valueFrom: { secretKeyRef: { name: hf-token-secret, key: token } } }
          ports: [ { containerPort: 8000 } ]
          resources: { limits: { amd.com/gpu: "1" } }
          volumeMounts:
            - { name: cache, mountPath: /root/.cache/huggingface }
            - { name: shm, mountPath: /dev/shm }
          startupProbe:   { httpGet: { path: /health, port: 8000 }, periodSeconds: 15, failureThreshold: 60 }
          readinessProbe: { httpGet: { path: /health, port: 8000 }, periodSeconds: 10 }

apiVersion: v1
kind: Service
metadata: { name: whisper-v3, namespace: llm }
spec:
  selector: { app: whisper-v3 }
  ports: [ { port: 8000, targetPort: 8000 } ]
```

**The Whisper gotcha:** a base vLLM image often lacks audio libraries. You'll get a `500`, and — confusingly — the `text` field may literally read `"Please install vllm[audio] for audio support"`. That's the error, not a transcription. Fix it by adding the audio extras to your image:

```bash
RUN pip install --no-cache-dir librosa soundfile
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*
```

(You can `pip install` into the running pod to confirm the fix, but it's ephemeral — bake it into the image to make it stick.)

## The checklist I'd tape to my monitor

1. **MI210 = gfx90a. No FP8/MXFP4.** Choose BF16/FP16 or INT4 checkpoints.
2. For MXFP4 models (gpt-oss), use a **BF16 upcast** and budget ~4× the VRAM.
3. Use a **pinned** `rocm/vllm` image; match the **node ROCm driver** to (or above) the image's ROCm.
4. Set `VLLM_USE_AITER=0` and the Triton attention backend on every pod.
5. Match the image's **entrypoint** to its arg style (`vllm serve …` vs `--model …`).
6. `amd.com/gpu: N` = N cards; size TP to fit weights in 64 GB chunks.
7. Embeddings → `--task embed` + `/v1/embeddings`. Whisper → `/v1/audio/transcriptions` + `vllm[audio]`.
8. **Validate before you trust** — one real request per model.

## A closing thought

The biggest mindset shift was treating "it deployed" and "it works" as two different facts. A pod going `1/1 Running` only means the process started. The real proof is one successful request that exercises the actual kernels on the actual silicon — because gfx90a isn't in most CI matrices, *you* are the validation step. Send the request, read the response, then trust it.

If you're staring at an MI210 box wondering whether modern LLMs will run on it: they will. Route around FP8/MXFP4, pin a good image, and the rest is ordinary Kubernetes.

*Happy serving.*
