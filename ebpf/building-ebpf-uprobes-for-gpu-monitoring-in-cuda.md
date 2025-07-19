# Building eBPF Uprobes for GPU Monitoring in CUDA

**Author:** [Khushi Chhillar](https://www.linkedin.com/in/kcl17/)  
**Published:** July 15, 2025

> _Visibility is performance._  
> Use the GPU you paid for — fully.

## Introduction

Despite high-dollar investments in top-tier GPUs such as NVIDIA's H100, suboptimal performance is common in AI training workloads. Traditional tools like `nvidia-smi` provide surface metrics (e.g., utilization percentage) but fail to uncover root causes such as inefficient CUDA API usage or silent errors. By instrumenting the actual CUDA Runtime API calls via modern observability techniques, engineers can diagnose and resolve performance bottlenecks otherwise invisible to standard GPU monitoring.

## CUDA Runtime API

When developing with frameworks like PyTorch and TensorFlow, thousands of CUDA runtime API calls are made under the hood, including:

- `cuMemAlloc()` — Allocate GPU memory
- `cuMemcpyHtoD()` — Copy data to GPU
- `cuLaunchKernel()` — Execute computation
- `cuMemcpyDtoH()` — Copy results back
- `cuMemFree()` — Release memory

These functions live inside user-space shared libraries (libcuda.so, libcudart.so). However, standard GPU monitoring tools do not offer visibility into the frequency, duration, or error states of these user-space calls.

## The GPU Opacity Problem

Traditional GPU monitoring is limited at the kernel or driver boundary, capturing only high-level symptoms (CPU/GPU utilization, basic memory stats) but not application-level behaviors. This means the “why” behind slow or erratic GPU performance often remains hidden.

**Common Real-World Issues Uncovered in Practice:**

- Memory leaks from unmatched allocations
- Launch overhead due to frequent, unbatched kernel executions
- Synchronization bottlenecks from excessive stream synchronization
- Silent errors not surfaced by unhandled CUDA error codes

## eBPF Uprobes: Illuminating User-Space CUDA Behavior

**eBPF uprobes** allow dynamic, zero-intrusion tracing of user-space function calls within CUDA libraries. This method overcomes the limitations of kernel-space probes, providing fine-grained observability into the actual sequence and parameters of CUDA Runtime API invocations.

**Example (conceptual):**

```console
// Hook into CUDA Runtime Library
SEC("uprobe/cuMemAlloc")
int trace_cu_mem_alloc_enter(struct pt_regs ctx) { / capture entry args */ }

SEC("uretprobe/cuMemAlloc")
int trace_cu_mem_alloc_exit(struct pt_regs ctx) { / capture return values, timing, errors */ }
```

## Architecture & Key Hook Points

### Target Libraries

- `/usr/local/cuda/lib64/libcudart.so.12`
- `/usr/lib/x86_64-linux-gnu/libcuda.so.1`

### Monitored Functions

- **Memory Management**
  - `cuMemAlloc` / `cuMemFree`
  - `cuMemcpyHtoD` / `cuMemcpyDtoH`
  - `cuMemAllocManaged`
- **Kernel Execution**
  - `cuLaunchKernel`
  - `cuLaunchCooperativeKernel`
- **Streams**
  - `cuStreamCreate` / `cuStreamDestroy`
  - `cuStreamSynchronize`

## Technical Challenges

1. **Complex Function Signatures:**  
   Many functions pass arguments via pointers or involve complex structures. eBPF cannot dereference user-space pointers directly. Capture arguments before and after call to reconstruct necessary context.

2. **Symbol Versioning & ABI:**  
   Differences across CUDA versions mean function names (symbols) may vary, requiring dynamic resolution or multi-version support in probes.

3. **Performance Overhead:**  
   CUDA API functions may be invoked 10,000+ times per second. Tracing must introduce negligible latency (<1 ms), employing efficient ring-buffers and minimal in-probe computation.

4. **Error Handling:**  
   Return codes map to a large enum (CUresult). Probes need lookup tables to translate error codes to human-readable values.

## Building a High-Performance Monitor

### Essential Components

- **Tracking Allocations:**  
  Monitor `cuMemAlloc` on entry (capture size/timestamp) and exit (success/failure), recording the mapping from pointer to allocation.
- **Detecting Leaks:**  
  Use eBPF hash maps to track active allocations; detect mismatches where memory is allocated but not released.
- **Kernel Launch Profiling:**  
  Capture `cuLaunchKernel` parameters (e.g., grid dims) and duration to spot launch inefficiencies.
- **Streaming to Userspace:**  
  Employ fast ring-buffer mechanisms for transmitting probe-captured events to user-space analytics dashboards.

### What This Enables

- Real-time tracing of CUDA API usage at the call level
- Immediate detection of memory leaks and allocation inefficiencies
- Kernel execution profiling for performance bottleneck discovery
- Proactive error detection from CUDA error codes
- Near-zero runtime overhead when properly engineered

## Case Study: Diagnosing Memory Allocation Inefficiency

**The Scenario**

A machine learning team observed unexpected training slowness during model development. Analysis revealed that the training loop allocated and freed a 1GB buffer on every batch iteration. This practice led to significant hidden performance costs.

**High-level training loop (simplified):**

```
for epoch in range(100):
    for batch in dataloader:
        # The following line creates a new 1GB CUDA buffer on every batch
        temp_buffer = torch.cuda.FloatTensor(batch_size, hidden_size)  # 1GB allocation

        # Model computation
        output = model(batch, temp_buffer)
        loss = criterion(output, targets)

        # temp_buffer falls out of scope for GC
        # PyTorch invokes cuMemFree() when cleaning up
```

**What occurred behind the scenes:**

```
// For each batch iteration, these CUDA API calls were issued:
cuMemAlloc(&device_ptr, 1073741824); // Allocate 1 GB on the device
// ... perform computations ...
cuMemFree(device_ptr); // Free the 1 GB allocation
```

**The Hidden Cost**

- `cuMemAlloc()` is a non-trivial, heavyweight operation — not just a pointer assignment.
- The GPU memory manager must locate a contiguous 1GB block for each allocation.
- Fragmentation in memory space accumulates across allocations.
- Each allocation takes roughly 100–500 microseconds.
- 1,000 batches × 500μs = 500ms wasted in memory allocation alone per epoch.

**eBPF Trace Output Diagnosis**

With eBPF uprobes attached to the CUDA runtime API, the following pattern was observed in live API call monitoring:

```
PID    FUNCTION       SIZE        DURATION    RESULT
1234   cuMemAlloc     1073741824  412μs       SUCCESS
1234   cuMemFree      1073741824  23μs        SUCCESS
1234   cuMemAlloc     1073741824  438μs       SUCCESS
1234   cuMemFree      1073741824  25μs        SUCCESS
#... repeated hundreds/thousands of times per epoch
```

This confirmed a repetitive cycle of high-latency memory allocations and deallocations for each batch.

**Solution: Buffer Pre-Allocation**

The optimal approach involved allocating the buffer once and reusing it across all batches, rather than allocating and freeing each time.

```
# Pre-allocate the temporary buffer once prior to the epoch loop
temp_buffer = torch.cuda.FloatTensor(batch_size, hidden_size)  # Single allocation (1 GB)

for epoch in range(100):
    for batch in dataloader:
        # Reuse the same buffer
        temp_buffer.fill_(0)  # Clear previous data
        output = model(batch, temp_buffer)
        loss = criterion(output, targets)
```

**Outcome**

- Eliminated 999 unnecessary cuMemAlloc() and cuMemFree() calls per epoch.
- Substantially reduced GPU memory fragmentation.
- Enhanced cache locality and application performance.
- Lowered contention on the GPU memory allocator.
- Achieved approximately 40% reduction in overall training time.

## Final Thoughts

Tracing and instrumenting CUDA API activity with eBPF uprobes exposes hidden inefficiencies and offers actionable performance insights at the application-library boundary. This enables:

- Real-time visibility into CUDA API usage patterns
- Detection of memory allocation inefficiencies and leaks
- Profiling of kernel launch frequencies and durations
- Capture and interpretation of silent errors
- Minimal-to-zero runtime monitoring overhead when correctly implemented

Modern GPU observability — especially at the API call level — is essential for maximizing hardware investment and ensuring model efficiency.

## Tools to Explore

- **bcc** and **bpftrace**: Dynamic userspace and kernel tracing frameworks
- **cuda-gdb**: CUDA-aware debugger
- **Grafana/Prometheus**: Metric visualization and analytics
- **bpftool, perf, nm, readelf**: Utility tools for symbol resolution and probe setup

## Implementation Availability

A robust, open-source eBPF profiler for CUDA workloads is currently under development, designed to facilitate comprehensive GPU call monitoring, memory tracking, and performance analysis for advanced ML and scientific computing applications.
