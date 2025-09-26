# Grok2 OnPrem Deployment via sglang

**Author:** [Shivank Chaudhary](https://www.linkedin.com/in/shivank1128/)

**Published:** Sept 14, 2025


x.ai just released their massive grok2 model, this thirsty beast can eat a lot of GPU compute power on your clusters, so be ready for the heat.

In last blog we saw the deployment of GPToSS 20B and 120B models which is done by vllm, but this time we’ll be using sglang inferencing enginebecause vllm does not support this transformer model as of today, but it’s in progress, https://github.com/vllm-project/vllm/issues/23557

## Grok-2: xAI’s Frontier Model

Grok-2, developed by xAI, represents cutting-edge capabilities in reasoning and knowledge synthesis. Key characteristics:

- **Size**: Large-scale transformer architecture
- **Quantization**: FP8 precision for memory efficiency
- **Serving Framework**: SGLang for optimized inference

Let’s start with the prerequisites:

- A K8s cluster installed with Nvidia GPU Operator

```shell
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
grok              grok2-sglang-f68f88b9b-9bsvl                                      0/1     Init:0/1   0             2m20s
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
prometheus        prometheus-prometheus-node-exporter-j4tjb                         1/1     Running     0             12d
```

- Storage class configured

```shell
kubectl get sc
NAME            PROVISIONER       RECLAIMPOLICY   VOLUMEBINDINGMODE     ALLOWVOLUMEEXPANSION   AGE
local-path      rancher.io/local-path   Delete    WaitForFirstConsumer  true                    13d
longhorn (default)   driver.longhorn.io Delete     Immediate             true                    19d
longhorn-static  driver.longhorn.io     Delete     Immediate             true                    19d
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
  name: grok2-weights-pvc
  namespace: grok
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 700Gi
  storageClassName: local-path # Use the appropriate storage class in your cluster
```

Grok2 Deployement Manifest file

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: grok2-sglang
  namespace: grok
  labels:
    app: grok2-sglang
spec:
  replicas: 1
  selector:
    matchLabels:
      app: grok2-sglang
  template:
    metadata:
      labels:
        app: grok2-sglang
    spec:
      imagePullSecrets:
        - name: dockerhub-creds
      initContainers:
        - name: fetch-weights
          image: python:3.11-slim
          imagePullPolicy: IfNotPresent
          command: ["/bin/sh", "-lc"]
          args:
            - |
              set -euo pipefail
              if [ -d "${MODEL_DIR}" ] && [ "$(ls -A ${MODEL_DIR})" ]; then
                echo "Weights already present. Skipping download."
                exit 0
              fi
              mkdir -p "${MODEL_DIR}"
              pip install --no-cache-dir --upgrade pip huggingface_hub hf_transfer protobuf
              hf download "${HF_REPO}" --local-dir "${MODEL_DIR}"
          env:
            - name: HF_REPO
              value: xai-org/grok-2
            - name: MODEL_DIR
              value: /models/grok-2
            - name: LOG_LEVEL
              value: DEBUG
          resources:
            requests:
              cpu: "1"
              memory: 1Gi
            limits:
              cpu: "4"
              memory: 8Gi
          volumeMounts:
            - name: weights
              mountPath: /models/grok-2
          terminationMessagePath: /dev/termination-log
          terminationMessagePolicy: File
      containers:
        - name: sglang
          image: lmsysorg/sglang:v0.5.2rc2-cu126
          imagePullPolicy: IfNotPresent
          command: ["python", "-m", "sglang.launch_server"]
          args:
            - --model-path
            - /models/grok-2
            - --tokenizer-path
            - /models/grok-2/tokenizer.tok.json
            - --tp
            - "8"
            - --quantization
            - fp8
            - --attention-backend
            - triton
            - --host
            - 0.0.0.0
            - --port
            - "30000"
          env:
            - name: LOG_LEVEL
              value: DEBUG
          ports:
            - containerPort: 30000
              protocol: TCP
          resources:
            requests:
              nvidia.com/gpu: "8"
            limits:
              nvidia.com/gpu: "8"
          volumeMounts:
            - name: weights
              mountPath: /models/grok-2
              readOnly: true
            - name: shm
              mountPath: /dev/shm
          terminationMessagePath: /dev/termination-log
          terminationMessagePolicy: File
      volumes:
        - name: weights
          persistentVolumeClaim:
            claimName: grok2-weights-pvc
        - name: shm
          emptyDir:
            medium: Memory
            sizeLimit: 32Gi
```

Logs:

```console
kubectl logs grok2-sglang-767c87b96-gvwxj -n grok
Defaulted container "sglang" out of: sglang, fetch-weights (init)
/usr/local/lib/python3.12/dist-packages/torch/cuda/__init__.py:63: FutureWarning: The pynvml package is deprecated. Please install nvidia-ml-py instead. If you did not install pynvml directly, please report this to the maintainers of the package that installed pynvml for you.
  import pynvml  # type: ignore[import]
W0911 10:24:10.440000 1 torch/utils/cpp_extension.py:2425] TORCH_CUDA_ARCH_LIST is not set, all archs for visible cards are included for compilation.
W0911 10:24:10.440000 1 torch/utils/cpp_extension.py:2425] If this is not desired, please set os.environ['TORCH_CUDA_ARCH_LIST'] to specific architectures.
`torch_dtype` is deprecated! Use `dtype` instead!
[2025-09-11 10:24:10] server_args=ServerArgs(model_path='/models/grok-2', tokenizer_path='/models/grok-2/tokenizer.tok.json', tokenizer_mode='auto', tokenizer_worker_num=1, skip_tokenizer_init=False, load_format='auto', model_loader_extra_config='{}', trust_remote_code=False, context_length=None, is_embedding=False, enable_multimodal=None, revision=None, model_impl='auto', host='0.0.0.0', port=30000, skip_server_warmup=False, warmups=None, nccl_port=None, dtype='auto', quantization='fp8', quantization_param_path=None, kv_cache_dtype='auto', mem_fraction_static=0.831, max_running_requests=None, max_queued_requests=9223372036854775807, max_total_tokens=None, chunked_prefill_size=8192, max_prefill_tokens=16384, schedule_policy='fcfs', schedule_conservativeness=1.0, page_size=1, hybrid_kvcache_ratio=None, swa_full_tokens_ratio=0.8, disable_hybrid_swa_memory=False, device='cuda', tp_size=8, pp_size=1, max_micro_batch_size=None, stream_interval=1, stream_output=False, random_seed=176157154, constrained_json_whitespace_pattern=None, watchdog_timeout=300, dist_timeout=None, download_dir=None, base_gpu_id=0, gpu_id_step=1, sleep_on_idle=False, log_level='info', log_level_http=None, log_requests=False, log_requests_level=2, crash_dump_folder=None, show_time_cost=False, enable_metrics=False, enable_metrics_for_all_schedulers=False, bucket_time_to_first_token=None, bucket_inter_token_latency=None, bucket_e2e_request_latency=None, collect_tokens_histogram=False, prompt_tokens_buckets=None, generation_tokens_buckets=None, decode_log_interval=40, enable_request_time_stats_logging=False, kv_events_config=None, gc_warning_threshold_secs=0.0, api_key=None, served_model_name='/models/grok-2', weight_version='default', chat_template=None, completion_template=None, file_storage_path='sglang_storage', enable_cache_report=False, reasoning_parser=None, tool_call_parser=None, tool_server=None, dp_size=1, load_balance_method='round_robin', dist_init_addr=None, nnodes=1, node_rank=0, json_model_override_args='{}', preferred_sampling_params=None, enable_lora=None, max_lora_rank=None, lora_target_modules=None, lora_paths=None, max_loaded_loras=None, max_loras_per_batch=8, lora_backend='triton', attention_backend='triton', decode_attention_backend=None, prefill_attention_backend=None, sampling_backend='flashinfer', grammar_backend='xgrammar', mm_attention_backend=None, speculative_algorithm=None, speculative_draft_model_path=None, speculative_draft_model_revision=None, speculative_num_steps=None, speculative_eagle_topk=None, speculative_num_draft_tokens=None, speculative_accept_threshold_single=1.0, speculative_accept_threshold_acc=1.0, speculative_token_map=None, ep_size=1, moe_a2a_backend='none', moe_runner_backend='auto', flashinfer_mxfp4_moe_precision='default', enable_flashinfer_allreduce_fusion=False, deepep_mode='auto', ep_num_redundant_experts=0, ep_dispatch_algorithm='static', init_expert_location='trivial', enable_eplb=False, eplb_algorithm='auto', eplb_rebalance_num_iterations=1000, eplb_rebalance_layers_per_chunk=None, eplb_min_rebalancing_utilization_threshold=1.0, expert_distribution_recorder_mode=None, expert_distribution_recorder_buffer_size=1000, enable_expert_distribution_metrics=False, deepep_config=None, moe_dense_tp_size=None, enable_hierarchical_cache=False, hicache_ratio=2.0, hicache_size=0, hicache_write_policy='write_through', hicache_io_backend='kernel', hicache_mem_layout='layer_first', hicache_storage_backend=None, hicache_storage_prefetch_policy='best_effort', hicache_storage_backend_extra_config=None, enable_double_sparsity=False, ds_channel_config_path=None, ds_heavy_channel_num=32, ds_heavy_token_num=256, ds_heavy_channel_type='qk', ds_sparse_decode_threshold=4096, cpu_offload_gb=0, offload_group_size=-1, offload_num_in_group=1, offload_prefetch_step=1, offload_mode='cpu', disable_radix_cache=False, cuda_graph_max_bs=None, cuda_graph_bs=None, disable_cuda_graph=False, disable_cuda_graph_padding=False, enable_profile_cuda_graph=False, enable_cudagraph_gc=False, enable_nccl_nvls=False, enable_symm_mem=False, disable_flashinfer_cutlass_moe_fp4_allgather=False, enable_tokenizer_batch_encode=False, disable_outlines_disk_cache=False, disable_custom_all_reduce=False, enable_mscclpp=False, disable_overlap_schedule=False, enable_mixed_chunk=False, enable_dp_attention=False, enable_dp_lm_head=False, enable_two_batch_overlap=False, tbo_token_distribution_threshold=0.48, enable_torch_compile=False, torch_compile_max_bs=32, torchao_config='', enable_nan_detection=False, enable_p2p_check=False, triton_attention_reduce_in_fp32=False, triton_attention_num_kv_splits=8, num_continuous_decode_steps=1, delete_ckpt_after_loading=False, enable_memory_saver=False, allow_auto_truncate=False, enable_custom_logit_processor=False, flashinfer_mla_disable_ragged=False, disable_shared_experts_fusion=False, disable_chunked_prefix_cache=False, disable_fast_image_processor=False, enable_return_hidden_states=False, scheduler_recv_interval=1, numa_node=None, debug_tensor_dump_output_folder=None, debug_tensor_dump_input_file=None, debug_tensor_dump_inject=False, debug_tensor_dump_prefill_only=False, disaggregation_mode='null', disaggregation_transfer_backend='mooncake', disaggregation_bootstrap_port=8998, disaggregation_decode_tp=None, disaggregation_decode_dp=None, disaggregation_prefill_pp=1, disaggregation_ib_device=None, num_reserved_decode_tokens=512, custom_weight_loader=[], weight_loader_disable_mmap=False, enable_pdmux=False, sm_group_num=3, enable_ep_moe=False, enable_deepep_moe=False, enable_flashinfer_cutlass_moe=False, enable_flashinfer_trtllm_moe=False, enable_triton_kernel_moe=False, enable_flashinfer_mxfp4_moe=False)
All deep_gemm operations loaded successfully!
[2025-09-11 10:24:11] Using default HuggingFace chat template with detected content format: string
/usr/local/lib/python3.12/dist-packages/torch/cuda/__init__.py:63: FutureWarning: The pynvml package is deprecated. Please install nvidia-ml-py instead. If you did not install pynvml directly, please report this to the maintainers of the package that installed pynvml for you.
  import pynvml  # type: ignore[import]
/usr/local/lib/python3.12/dist-packages/torch/cuda/__init__.py:63: FutureWarning: The pynvml package is deprecated. Please install nvidia-ml-py instead. If you did not install pynvml directly, please report this to the maintainers of the package that installed pynvml for you.
  import pynvml  # type: ignore[import]
/usr/local/lib/python3.12/dist-packages/torch/cuda/__init__.py:63: FutureWarning: The pynvml package is deprecated. Please install nvidia-ml-py instead. If you did not install pynvml directly, please report this to the maintainers of the package that installed pynvml for you.
  import pynvml  # type: ignore[import]
/usr/local/lib/python3.12/dist-packages/torch/cuda/__init__.py:63: FutureWarning: The pynvml package is deprecated. Please install nvidia-ml-py instead. If you did not install pynvml directly, please report this to the maintainers of the package that installed pynvml for you.
  import pynvml  # type: ignore[import]
/usr/local/lib/python3.12/dist-packages/torch/cuda/__init__.py:63: FutureWarning: The pynvml package is deprecated. Please install nvidia-ml-py instead. If you did not install pynvml directly, please report this to the maintainers of the package that installed pynvml for you.
  import pynvml  # type: ignore[import]
/usr/local/lib/python3.12/dist-packages/torch/cuda/__init__.py:63: FutureWarning: The pynvml package is deprecated. Please install nvidia-ml-py instead. If you did not install pynvml directly, please report this to the maintainers of the package that installed pynvml for you.
  import pynvml  # type: ignore[import]
/usr/local/lib/python3.12/dist-packages/torch/cuda/__init__.py:63: FutureWarning: The pynvml package is deprecated. Please install nvidia-ml-py instead. If you did not install pynvml directly, please report this to the maintainers of the package that installed pynvml for you.
  import pynvml  # type: ignore[import]
/usr/local/lib/python3.12/dist-packages/torch/cuda/__init__.py:63: FutureWarning: The pynvml package is deprecated. Please install nvidia-ml-py instead. If you did not install pynvml directly, please report this to the maintainers of the package that installed pynvml for you.
  import pynvml  # type: ignore[import]
/usr/local/lib/python3.12/dist-packages/torch/cuda/__init__.py:63: FutureWarning: The pynvml package is deprecated. Please install nvidia-ml-py instead. If you did not install pynvml directly, please report this to the maintainers of the package that installed pynvml for you.
  import pynvml  # type: ignore[import]
W0911 10:24:17.065000 224 torch/utils/cpp_extension.py:2425] TORCH_CUDA_ARCH_LIST is not set, all archs for visible cards are included for compilation.
W0911 10:24:17.065000 224 torch/utils/cpp_extension.py:2425] If this is not desired, please set os.environ['TORCH_CUDA_ARCH_LIST'] to specific architectures.
W0911 10:24:19.370000 218 torch/utils/cpp_extension.py:2425] TORCH_CUDA_ARCH_LIST is not set, all archs for visible cards are included for compilation.
W0911 10:24:19.370000 218 torch/utils/cpp_extension.py:2425] If this is not desired, please set os.environ['TORCH_CUDA_ARCH_LIST'] to specific architectures.
W0911 10:24:19.445000 221 torch/utils/cpp_extension.py:2425] TORCH_CUDA_ARCH_LIST is not set, all archs for visible cards are included for compilation.
W0911 10:24:19.445000 221 torch/utils/cpp_extension.py:2425] If this is not desired, please set os.environ['TORCH_CUDA_ARCH_LIST'] to specific architectures.
W0911 10:24:19.455000 216 torch/utils/cpp_extension.py:2425] TORCH_CUDA_ARCH_LIST is not set, all archs for visible cards are included for compilation.
W0911 10:24:19.455000 216 torch/utils/cpp_extension.py:2425] If this is not desired, please set os.environ['TORCH_CUDA_ARCH_LIST'] to specific architectures.
W0911 10:24:19.570000 217 torch/utils/cpp_extension.py:2425] TORCH_CUDA_ARCH_LIST is not set, all archs for visible cards are included for compilation.
W0911 10:24:19.570000 217 torch/utils/cpp_extension.py:2425] If this is not desired, please set os.environ['TORCH_CUDA_ARCH_LIST'] to specific architectures.
`torch_dtype` is deprecated! Use `dtype` instead!
W0911 10:24:19.668000 222 torch/utils/cpp_extension.py:2425] TORCH_CUDA_ARCH_LIST is not set, all archs for visible cards are included for compilation.
W0911 10:24:19.668000 222 torch/utils/cpp_extension.py:2425] If this is not desired, please set os.environ['TORCH_CUDA_ARCH_LIST'] to specific architectures.
W0911 10:24:19.724000 223 torch/utils/cpp_extension.py:2425] TORCH_CUDA_ARCH_LIST is not set, all archs for visible cards are included for compilation.
W0911 10:24:19.724000 223 torch/utils/cpp_extension.py:2425] If this is not desired, please set os.environ['TORCH_CUDA_ARCH_LIST'] to specific architectures.
W0911 10:24:19.729000 219 torch/utils/cpp_extension.py:2425] TORCH_CUDA_ARCH_LIST is not set, all archs for visible cards are included for compilation.
W0911 10:24:19.729000 219 torch/utils/cpp_extension.py:2425] If this is not desired, please set os.environ['TORCH_CUDA_ARCH_LIST'] to specific architectures.
`torch_dtype` is deprecated! Use `dtype` instead!
W0911 10:24:19.765000 220 torch/utils/cpp_extension.py:2425] TORCH_CUDA_ARCH_LIST is not set, all archs for visible cards are included for compilation.
W0911 10:24:19.765000 220 torch/utils/cpp_extension.py:2425] If this is not desired, please set os.environ['TORCH_CUDA_ARCH_LIST'] to specific architectures.
`torch_dtype` is deprecated! Use `dtype` instead!
`torch_dtype` is deprecated! Use `dtype` instead!
`torch_dtype` is deprecated! Use `dtype` instead!
`torch_dtype` is deprecated! Use `dtype` instead!
`torch_dtype` is deprecated! Use `dtype` instead!
[2025-09-11 10:24:20 TP0] Init torch distributed begin.
`torch_dtype` is deprecated! Use `dtype` instead!
[Gloo] Rank 3 is connected to 7 peer ranks. Expected number of connected peer ranks is : 7
[Gloo] Rank 1 is connected to 7 peer ranks. Expected number of connected peer ranks is : 7
[Gloo] Rank 0 is connected to 7 peer ranks. Expected number of connected peer ranks is : 7
[Gloo] Rank 2 is connected to 7 peer ranks. Expected number of connected peer ranks is : 7
[Gloo] Rank 4 is connected to 7 peer ranks. Expected number of connected peer ranks is : 7
[Gloo] Rank 5 is connected to 7 peer ranks. Expected number of connected peer ranks is : 7
[Gloo] Rank 7 is connected to 7 peer ranks. Expected number of connected peer ranks is : 7
[Gloo] Rank 6 is connected to 7 peer ranks. Expected number of connected peer ranks is : 7
[Gloo] Rank 0 is connected to 7 peer ranks. Expected number of connected peer ranks is : 7
[Gloo] Rank 3 is connected to 7 peer ranks. Expected number of connected peer ranks is : 7
[Gloo] Rank 1 is connected to 7 peer ranks. Expected number of connected peer ranks is : 7
[Gloo] Rank 2 is connected to 7 peer ranks. Expected number of connected peer ranks is : 7
[Gloo] Rank 4 is connected to 7 peer ranks. Expected number of connected peer ranks is : 7
[Gloo] Rank 5 is connected to 7 peer ranks. Expected number of connected peer ranks is : 7
[2025-09-11 10:24:21 TP0] sglang is using nccl==2.27.3
[Gloo] Rank 7 is connected to 7 peer ranks. Expected number of connected peer ranks is : 7
[Gloo] Rank 6 is connected to 7 peer ranks. Expected number of connected peer ranks is : 7
[Gloo] Rank 0 is connected to 0 peer ranks. Expected number of connected peer ranks is : 0
[Gloo] Rank 0 is connected to 0 peer ranks. Expected number of connected peer ranks is : 0
[Gloo] Rank 0 is connected to 0 peer ranks. Expected number of connected peer ranks is : 0
[Gloo] Rank 0 is connected to 0 peer ranks. Expected number of connected peer ranks is : 0
[Gloo] Rank 0 is connected to 0 peer ranks. Expected number of connected peer ranks is : 0
[Gloo] Rank 0 is connected to 0 peer ranks. Expected number of connected peer ranks is : 0
[Gloo] Rank 0 is connected to 0 peer ranks. Expected number of connected peer ranks is : 0
[Gloo] Rank 0 is connected to 0 peer ranks. Expected number of connected peer ranks is : 0
[Gloo] Rank 0 is connected to 0 peer ranks. Expected number of connected peer ranks is : 0
[Gloo] Rank 0 is connected to 0 peer ranks. Expected number of connected peer ranks is : 0
[Gloo] Rank 0 is connected to 0 peer ranks. Expected number of connected peer ranks is : 0
[Gloo] Rank 0 is connected to 0 peer ranks. Expected number of connected peer ranks is : 0
[Gloo] Rank 0 is connected to 0 peer ranks. Expected number of connected peer ranks is : 0
[Gloo] Rank 0 is connected to 0 peer ranks. Expected number of connected peer ranks is : 0
[Gloo] Rank 0 is connected to 0 peer ranks. Expected number of connected peer ranks is : 0
[Gloo] Rank 0 is connected to 0 peer ranks. Expected number of connected peer ranks is : 0
[Gloo] Rank 0 is connected to 7 peer ranks. Expected number of connected peer ranks is : 7
[Gloo] Rank 1 is connected to 7 peer ranks. Expected number of connected peer ranks is : 7
[Gloo] Rank 2 is connected to 7 peer ranks. Expected number of connected peer ranks is : 7
[Gloo] Rank 4 is connected to 7 peer ranks. Expected number of connected peer ranks is : 7
[Gloo] Rank 5 is connected to 7 peer ranks. Expected number of connected peer ranks is : 7
[Gloo] Rank 6 is connected to 7 peer ranks. Expected number of connected peer ranks is : 7
[Gloo] Rank 3 is connected to 7 peer ranks. Expected number of connected peer ranks is : 7
[Gloo] Rank 7 is connected to 7 peer ranks. Expected number of connected peer ranks is : 7
[2025-09-11 10:24:23 TP0] Init torch distributed ends. mem usage=1.25 GB
[2025-09-11 10:24:24 TP0] Load weight begin. avail mem=77.43 GB
[2025-09-11 10:24:25 TP0] #parameters (analytical): 243.74 B, #parameters (actual): 269.56 B
All deep_gemm operations loaded successfully!
Loading safetensors checkpoint shards:   0% Completed | 0/18 [00:00<?, ?it/s]
Loading safetensors checkpoint shards:   6% Completed | 1/18 [00:23<06:44, 23.81s/it]
Loading safetensors checkpoint shards:  11% Completed | 2/18 [00:31<03:46, 14.18s/it]
Loading safetensors checkpoint shards:  17% Completed | 3/18 [00:38<02:44, 10.94s/it]
Loading safetensors checkpoint shards:  22% Completed | 4/18 [00:39<01:41,  7.25s/it]
Loading safetensors checkpoint shards:  28% Completed | 5/18 [00:40<01:01,  4.73s/it]
Loading safetensors checkpoint shards:  33% Completed | 6/18 [00:44<00:54,  4.54s/it]
Loading safetensors checkpoint shards:  39% Completed | 7/18 [00:48<00:48,  4.44s/it]
Loading safetensors checkpoint shards:  61% Completed | 11/18 [00:49<00:11,  1.63s/it]
Loading safetensors checkpoint shards:  67% Completed | 12/18 [00:53<00:13,  2.21s/it]
Loading safetensors checkpoint shards:  72% Completed | 13/18 [00:53<00:08,  1.77s/it]
Loading safetensors checkpoint shards:  83% Completed | 15/18 [00:54<00:03,  1.13s/it]
[2025-09-11 10:25:26 TP3] #all_names: 835, #hit_names: 707, #missing_exclude_scales: 0
[2025-09-11 10:25:26 TP4] #all_names: 835, #hit_names: 707, #missing_exclude_scales: 0
[2025-09-11 10:25:26 TP2] #all_names: 835, #hit_names: 707, #missing_exclude_scales: 0
[2025-09-11 10:25:27 TP6] #all_names: 835, #hit_names: 707, #missing_exclude_scales: 0
[2025-09-11 10:25:31 TP1] #all_names: 835, #hit_names: 707, #missing_exclude_scales: 0
Loading safetensors checkpoint shards:  89% Completed | 16/18 [01:07<00:07,  3.78s/it]
Loading safetensors checkpoint shards: 100% Completed | 18/18 [01:08<00:00,  2.42s/it]
Loading safetensors checkpoint shards: 100% Completed | 18/18 [01:08<00:00,  3.78s/it]

[2025-09-11 10:25:33 TP0] #all_names: 835, #hit_names: 707, #missing_exclude_scales: 0
[2025-09-11 10:25:33 TP0] Load weight end. type=Grok1ForCausalLM, dtype=torch.bfloat16, avail mem=40.69 GB, mem usage=36.73 GB.
[2025-09-11 10:25:37 TP5] #all_names: 835, #hit_names: 707, #missing_exclude_scales: 0
[2025-09-11 10:25:42 TP7] #all_names: 835, #hit_names: 707, #missing_exclude_scales: 0
[2025-09-11 10:25:43 TP3] KV Cache is allocated. #tokens: 903439, K size: 13.79 GB, V size: 13.79 GB
[2025-09-11 10:25:43 TP6] KV Cache is allocated. #tokens: 903439, K size: 13.79 GB, V size: 13.79 GB
[2025-09-11 10:25:43 TP1] KV Cache is allocated. #tokens: 903439, K size: 13.79 GB, V size: 13.79 GB
[2025-09-11 10:25:43 TP2] KV Cache is allocated. #tokens: 903439, K size: 13.79 GB, V size: 13.79 GB
[2025-09-11 10:25:43 TP4] KV Cache is allocated. #tokens: 903439, K size: 13.79 GB, V size: 13.79 GB
[2025-09-11 10:25:43 TP0] KV Cache is allocated. #tokens: 903439, K size: 13.79 GB, V size: 13.79 GB
[2025-09-11 10:25:43 TP0] Memory pool end. avail mem=11.22 GB
[2025-09-11 10:25:43 TP5] KV Cache is allocated. #tokens: 903439, K size: 13.79 GB, V size: 13.79 GB
[2025-09-11 10:25:43 TP7] KV Cache is allocated. #tokens: 903439, K size: 13.79 GB, V size: 13.79 GB
[2025-09-11 10:25:43 TP0] Capture cuda graph begin. This can take up to several minutes. avail mem=11.16 GB
[2025-09-11 10:25:44 TP0] Capture cuda graph bs [1, 2, 4, 8, 16, 24, 32, 40, 48, 56, 64, 72, 80, 88, 96, 104, 112, 120, 128, 136, 144, 152, 160]
Capturing batches (bs=160 avail_mem=10.92 GB):   0%|          | 0/23 [00:00<?, ?it/s][2025-09-11 10:25:47 TP3] Config file not found at /sgl-workspace/sglang/python/sglang/srt/layers/moe/fused_moe_triton/configs/triton_3_4_0/E=8,N=2048,device_name=NVIDIA_H100_80GB_HBM3,dtype=fp8_w8a8.json. Fallback to triton version 3.1.0 and use MoE kernel config from /sgl-workspace/sglang/python/sglang/srt/layers/moe/fused_moe_triton/configs/triton_3_1_0/E=8,N=2048,device_name=NVIDIA_H100_80GB_HBM3,dtype=fp8_w8a8.json. Performance might be sub-optimal!
[2025-09-11 10:25:47 TP6] Config file not found at /sgl-workspace/sglang/python/sglang/srt/layers/moe/fused_moe_triton/configs/triton_3_4_0/E=8,N=2048,device_name=NVIDIA_H100_80GB_HBM3,dtype=fp8_w8a8.json. Fallback to triton version 3.1.0 and use MoE kernel config from /sgl-workspace/sglang/python/sglang/srt/layers/moe/fused_moe_triton/configs/triton_3_1_0/E=8,N=2048,device_name=NVIDIA_H100_80GB_HBM3,dtype=fp8_w8a8.json. Performance might be sub-optimal!
[2025-09-11 10:25:47 TP4] Config file not found at /sgl-workspace/sglang/python/sglang/srt/layers/moe/fused_moe_triton/configs/triton_3_4_0/E=8,N=2048,device_name=NVIDIA_H100_80GB_HBM3,dtype=fp8_w8a8.json. Fallback to triton version 3.1.0 and use MoE kernel config from /sgl-workspace/sglang/python/sglang/srt/layers/moe/fused_moe_triton/configs/triton_3_1_0/E=8,N=2048,device_name=NVIDIA_H100_80GB_HBM3,dtype=fp8_w8a8.json. Performance might be sub-optimal!
[2025-09-11 10:25:47 TP5] Config file not found at /sgl-workspace/sglang/python/sglang/srt/layers/moe/fused_moe_triton/configs/triton_3_4_0/E=8,N=2048,device_name=NVIDIA_H100_80GB_HBM3,dtype=fp8_w8a8.json. Fallback to triton version 3.1.0 and use MoE kernel config from /sgl-workspace/sglang/python/sglang/srt/layers/moe/fused_moe_triton/configs/triton_3_1_0/E=8,N=2048,device_name=NVIDIA_H100_80GB_HBM3,dtype=fp8_w8a8.json. Performance might be sub-optimal!
[2025-09-11 10:25:47 TP1] Config file not found at /sgl-workspace/sglang/python/sglang/srt/layers/moe/fused_moe_triton/configs/triton_3_4_0/E=8,N=2048,device_name=NVIDIA_H100_80GB_HBM3,dtype=fp8_w8a8.json. Fallback to triton version 3.1.0 and use MoE kernel config from /sgl-workspace/sglang/python/sglang/srt/layers/moe/fused_moe_triton/configs/triton_3_1_0/E=8,N=2048,device_name=NVIDIA_H100_80GB_HBM3,dtype=fp8_w8a8.json. Performance might be sub-optimal!
[2025-09-11 10:25:47 TP7] Config file not found at /sgl-workspace/sglang/python/sglang/srt/layers/moe/fused_moe_triton/configs/triton_3_4_0/E=8,N=2048,device_name=NVIDIA_H100_80GB_HBM3,dtype=fp8_w8a8.json. Fallback to triton version 3.1.0 and use MoE kernel config from /sgl-workspace/sglang/python/sglang/srt/layers/moe/fused_moe_triton/configs/triton_3_1_0/E=8,N=2048,device_name=NVIDIA_H100_80GB_HBM3,dtype=fp8_w8a8.json. Performance might be sub-optimal!
[2025-09-11 10:25:47 TP2] Config file not found at /sgl-workspace/sglang/python/sglang/srt/layers/moe/fused_moe_triton/configs/triton_3_4_0/E=8,N=2048,device_name=NVIDIA_H100_80GB_HBM3,dtype=fp8_w8a8.json. Fallback to triton version 3.1.0 and use MoE kernel config from /sgl-workspace/sglang/python/sglang/srt/layers/moe/fused_moe_triton/configs/triton_3_1_0/E=8,N=2048,device_name=NVIDIA_H100_80GB_HBM3,dtype=fp8_w8a8.json. Performance might be sub-optimal!
[2025-09-11 10:25:47 TP0] Config file not found at /sgl-workspace/sglang/python/sglang/srt/layers/moe/fused_moe_triton/configs/triton_3_4_0/E=8,N=2048,device_name=NVIDIA_H100_80GB_HBM3,dtype=fp8_w8a8.json. Fallback to triton version 3.1.0 and use MoE kernel config from /sgl-workspace/sglang/python/sglang/srt/layers/moe/fused_moe_triton/configs/triton_3_1_0/E=8,N=2048,device_name=NVIDIA_H100_80GB_HBM3,dtype=fp8_w8a8.json. Performance might be sub-optimal!
Capturing batches (bs=1 avail_mem=10.28 GB): 100%|██████████| 23/23 [00:16<00:00,  1.42it/s]
[2025-09-11 10:26:00 TP3] Registering 2967 cuda graph addresses
[2025-09-11 10:26:00 TP1] Registering 2967 cuda graph addresses
[2025-09-11 10:26:00 TP7] Registering 2967 cuda graph addresses
[2025-09-11 10:26:00 TP4] Registering 2967 cuda graph addresses
[2025-09-11 10:26:00 TP5] Registering 2967 cuda graph addresses
[2025-09-11 10:26:00 TP6] Registering 2967 cuda graph addresses
[2025-09-11 10:26:00 TP0] Registering 2967 cuda graph addresses
[2025-09-11 10:26:00 TP2] Registering 2967 cuda graph addresses
[2025-09-11 10:26:00 TP0] Capture cuda graph end. Time elapsed: 17.13 s. mem usage=0.89 GB. avail mem=10.26 GB.
[2025-09-11 10:26:01 TP0] max_total_num_tokens=903439, chunked_prefill_size=8192, max_prefill_tokens=16384, max_running_requests=3529, context_len=131072, available_gpu_mem=10.26 GB
[2025-09-11 10:26:01] INFO:     Started server process [1]
[2025-09-11 10:26:01] INFO:     Waiting for application startup.
[2025-09-11 10:26:01] INFO:     Application startup complete.
[2025-09-11 10:26:01] INFO:     Uvicorn running on http://0.0.0.0:30000 (Press CTRL+C to quit)
[2025-09-11 10:26:02] INFO:     127.0.0.1:60028 - "GET /get_model_info HTTP/1.1" 200 OK
[2025-09-11 10:26:02 TP0] Prefill batch. #new-seq: 1, #new-token: 6, #cached-token: 0, token usage: 0.00, #running-req: 0, #queue-req: 0,
[2025-09-11 10:26:05] INFO:     127.0.0.1:60032 - "POST /generate HTTP/1.1" 200 OK
[2025-09-11 10:26:05] The server is fired up and ready to roll!
[2025-09-11 10:26:21 TP0] Prefill batch. #new-seq: 1, #new-token: 15, #cached-token: 0, token usage: 0.00, #running-req: 0, #queue-req: 0,
[2025-09-11 10:26:22 TP0] Decode batch. #running-req: 1, #token: 48, token usage: 0.00, cuda graph: True, gen throughput (token/s): 1.88, #queue-req: 0,
[2025-09-11 10:26:22] INFO:     10.46.124.148:54800 - "POST /v1/chat/completions HTTP/1.1" 200 OK
[2025-09-12 07:18:12 TP0] Prefill batch. #new-seq: 1, #new-token: 12, #cached-token: 2, token usage: 0.00, #running-req: 0, #queue-req: 0,
[2025-09-12 07:18:14 TP0] Decode batch. #running-req: 1, #token: 19, token usage: 0.00, cuda graph: True, gen throughput (token/s): 0.00, #queue-req: 0,
[2025-09-12 07:18:14] INFO:     10.34.109.36:33844 - "POST /v1/chat/completions HTTP/1.1" 200 OK
[2025-09-12 07:27:13 TP0] Prefill batch. #new-seq: 1, #new-token: 15, #cached-token: 2, token usage: 0.00, #running-req: 0, #queue-req: 0,
[2025-09-12 07:27:14 TP0] Decode batch. #running-req: 1, #token: 44, token usage: 0.00, cuda graph: True, gen throughput (token/s): 0.07, #queue-req: 0,
[2025-09-12 07:27:14 TP0] Decode batch. #running-req: 1, #token: 84, token usage: 0.00, cuda graph: True, gen throughput (token/s): 98.94, #queue-req: 0,
[2025-09-12 07:27:15 TP0] Decode batch. #running-req: 1, #token: 124, token usage: 0.00, cuda graph: True, gen throughput (token/s): 98.71, #queue-req: 0,
[2025-09-12 07:27:15 TP0] Decode batch. #running-req: 1, #token: 164, token usage: 0.00, cuda graph: True, gen throughput (token/s): 98.44, #queue-req: 0,
[2025-09-12 07:27:15 TP0] Decode batch. #running-req: 1, #token: 204, token usage: 0.00, cuda graph: True, gen throughput (token/s): 98.30, #queue-req: 0,
[2025-09-12 07:27:16 TP0] Decode batch. #running-req: 1, #token: 244, token usage: 0.00, cuda graph: True, gen throughput (token/s): 98.24, #queue-req: 0,
[2025-09-12 07:27:16 TP0] Decode batch. #running-req: 1, #token: 284, token usage: 0.00, cuda graph: True, gen throughput (token/s): 97.32, #queue-req: 0,
[2025-09-12 07:27:17 TP0] Decode batch. #running-req: 1, #token: 324, token usage: 0.00, cuda graph: True, gen throughput (token/s): 96.90, #queue-req: 0,
[2025-09-12 07:27:17 TP0] Decode batch. #running-req: 1, #token: 364, token usage: 0.00, cuda graph: True, gen throughput (token/s): 96.80, #queue-req: 0,
[2025-09-12 07:27:17 TP0] Decode batch. #running-req: 1, #token: 404, token usage: 0.00, cuda graph: True, gen throughput (token/s): 96.72, #queue-req: 0,
[2025-09-12 07:27:18 TP0] Decode batch. #running-req: 1, #token: 444, token usage: 0.00, cuda graph: True, gen throughput (token/s): 96.65, #queue-req: 0,
[2025-09-12 07:27:18 TP0] Decode batch. #running-req: 1, #token: 484, token usage: 0.00, cuda graph: True, gen throughput (token/s): 96.68, #queue-req: 0,
[2025-09-12 07:27:18] INFO:     10.34.109.36:40636 - "POST /v1/chat/completions HTTP/1.1" 200 OK
[2025-09-12 07:38:09 TP0] Prefill batch. #new-seq: 1, #new-token: 16, #cached-token: 2, token usage: 0.00, #running-req: 0, #queue-req: 0,
[2025-09-12 07:38:09 TP0] Decode batch. #running-req: 1, #token: 40, token usage: 0.00, cuda graph: True, gen throughput (token/s): 0.06, #queue-req: 0,
[2025-09-12 07:38:09 TP0] Decode batch. #running-req: 1, #token: 80, token usage: 0.00, cuda graph: True, gen throughput (token/s): 98.85, #queue-req: 0,
[2025-09-12 07:38:10 TP0] Decode batch. #running-req: 1, #token: 120, token usage: 0.00, cuda graph: True, gen throughput (token/s): 98.70, #queue-req: 0,
[2025-09-12 07:38:10 TP0] Decode batch. #running-req: 1, #token: 160, token usage: 0.00, cuda graph: True, gen throughput (token/s): 98.47, #queue-req: 0,
[2025-09-12 07:38:10 TP0] Decode batch. #running-req: 1, #token: 200, token usage: 0.00, cuda graph: True, gen throughput (token/s): 98.32, #queue-req: 0,
[2025-09-12 07:38:11 TP0] Decode batch. #running-req: 1, #token: 240, token usage: 0.00, cuda graph: True, gen throughput (token/s): 98.22, #queue-req: 0,
[2025-09-12 07:38:11 TP0] Decode batch. #running-req: 1, #token: 280, token usage: 0.00, cuda graph: True, gen throughput (token/s): 97.46, #queue-req: 0,
[2025-09-12 07:38:12 TP0] Decode batch. #running-req: 1, #token: 320, token usage: 0.00, cuda graph: True, gen throughput (token/s): 96.91, #queue-req: 0,
[2025-09-12 07:38:12 TP0] Decode batch. #running-req: 1, #token: 360, token usage: 0.00, cuda graph: True, gen throughput (token/s): 96.80, #queue-req: 0,
[2025-09-12 07:38:13 TP0] Decode batch. #running-req: 1, #token: 400, token usage: 0.00, cuda graph: True, gen throughput (token/s): 96.76, #queue-req: 0,
[2025-09-12 07:38:13 TP0] Decode batch. #running-req: 1, #token: 440, token usage: 0.00, cuda graph: True, gen throughput (token/s): 96.69, #queue-req: 0,
[2025-09-12 07:38:13 TP0] Decode batch. #running-req: 1, #token: 480, token usage: 0.00, cuda graph: True, gen throughput (token/s): 96.73, #queue-req: 0,
[2025-09-12 07:38:14 TP0] Decode batch. #running-req: 1, #token: 520, token usage: 0.00, cuda graph: True, gen throughput (token/s): 96.45, #queue-req: 0,
[2025-09-12 07:38:14 TP0] Decode batch. #running-req: 1, #token: 560, token usage: 0.00, cuda graph: True, gen throughput (token/s): 95.28, #queue-req: 0,
[2025-09-12 07:38:15 TP0] Decode batch. #running-req: 1, #token: 600, token usage: 0.00, cuda graph: True, gen throughput (token/s): 95.12, #queue-req: 0,
[2025-09-12 07:38:15 TP0] Decode batch. #running-req: 1, #token: 640, token usage: 0.00, cuda graph: True, gen throughput (token/s): 95.04, #queue-req: 0,
[2025-09-12 07:38:15 TP0] Decode batch. #running-req: 1, #token: 680, token usage: 0.00, cuda graph: True, gen throughput (token/s): 95.03, #queue-req: 0,
[2025-09-12 07:38:16 TP0] Decode batch. #running-req: 1, #token: 720, token usage: 0.00, cuda graph: True, gen throughput (token/s): 95.03, #queue-req: 0,
[2025-09-12 07:38:16 TP0] Decode batch. #running-req: 1, #token: 760, token usage: 0.00, cuda graph: True, gen throughput (token/s): 95.05, #queue-req: 0,
[2025-09-12 07:38:17 TP0] Decode batch. #running-req: 1, #token: 800, token usage: 0.00, cuda graph: True, gen throughput (token/s): 93.83, #queue-req: 0,
[2025-09-12 07:38:17 TP0] Decode batch. #running-req: 1, #token: 840, token usage: 0.00, cuda graph: True, gen throughput (token/s): 93.47, #queue-req: 0,
[2025-09-12 07:38:18 TP0] Decode batch. #running-req: 1, #token: 880, token usage: 0.00, cuda graph: True, gen throughput (token/s): 93.48, #queue-req: 0,
[2025-09-12 07:38:18 TP0] Decode batch. #running-req: 1, #token: 920, token usage: 0.00, cuda graph: True, gen throughput (token/s): 93.51, #queue-req: 0,
[2025-09-12 07:38:18 TP0] Decode batch. #running-req: 1, #token: 960, token usage: 0.00, cuda graph: True, gen throughput (token/s): 93.49, #queue-req: 0,
[2025-09-12 07:38:19 TP0] Decode batch. #running-req: 1, #token: 1000, token usage: 0.00, cuda graph: True, gen throughput (token/s): 93.52, #queue-req: 0,
[2025-09-12 07:38:19 TP0] Decode batch. #running-req: 1, #token: 1040, token usage: 0.00, cuda graph: True, gen throughput (token/s): 92.94, #queue-req: 0,
[2025-09-12 07:38:20 TP0] Decode batch. #running-req: 1, #token: 1080, token usage: 0.00, cuda graph: True, gen throughput (token/s): 92.00, #queue-req: 0,
[2025-09-12 07:38:20 TP0] Decode batch. #running-req: 1, #token: 1120, token usage: 0.00, cuda graph: True, gen throughput (token/s): 91.99, #queue-req: 0,
[2025-09-12 07:38:21 TP0] Decode batch. #running-req: 1, #token: 1160, token usage: 0.00, cuda graph: True, gen throughput (token/s): 92.02, #queue-req: 0,
[2025-09-12 07:38:21 TP0] Decode batch. #running-req: 1, #token: 1200, token usage: 0.00, cuda graph: True, gen throughput (token/s): 92.03, #queue-req: 0,
[2025-09-12 07:38:21 TP0] Decode batch. #running-req: 1, #token: 1240, token usage: 0.00, cuda graph: True, gen throughput (token/s): 92.02, #queue-req: 0,
[2025-09-12 07:38:22 TP0] Decode batch. #running-req: 1, #token: 1280, token usage: 0.00, cuda graph: True, gen throughput (token/s): 92.04, #queue-req: 0,
[2025-09-12 07:38:23 TP0] Decode batch. #running-req: 1, #token: 1320, token usage: 0.00, cuda graph: True, gen throughput (token/s): 33.16, #queue-req: 0,
[2025-09-12 07:38:24 TP0] Decode batch. #running-req: 1, #token: 1360, token usage: 0.00, cuda graph: True, gen throughput (token/s): 38.38, #queue-req: 0,
[2025-09-12 07:38:25 TP0] Decode batch. #running-req: 1, #token: 1400, token usage: 0.00, cuda graph: True, gen throughput (token/s): 90.65, #queue-req: 0,
[2025-09-12 07:38:25 TP0] Decode batch. #running-req: 1, #token: 1440, token usage: 0.00, cuda graph: True, gen throughput (token/s): 90.67, #queue-req: 0,
[2025-09-12 07:38:25] INFO:     10.34.109.36:37208 - "POST /v1/chat/completions HTTP/1.1" 200 OK
```


