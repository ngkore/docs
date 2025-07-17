# Inside CUDA: Building eBPF uprobes for GPU Monitoring

> *Visibility is performance.*<br>
> Use the GPU you paid for — fully.

You spent $50,000 on an H100 GPU, but your AI training job is mysteriously slow. nvidia-smi shows 80% utilization, but something feels off. What if I told you that your application is making 10,000 unnecessary CUDA API calls every second, and each one is adding microseconds of overhead?

Traditional GPU monitoring tools give you the “what” but never the “why.” Today, we’re going deeper — into the actual CUDA Runtime API calls that make your GPU tick.

## The Hidden Layer: CUDA Runtime API
Every time your PyTorch or TensorFlow model runs, it’s making thousands of calls into CUDA libraries:
```console
# Your training loop under the hood
cuMemAlloc()        # Allocate GPU memory
cuMemcpyHtoD()      # Copy data to GPU  
cuLaunchKernel()    # Launch computation
cuMemcpyDtoH()      # Copy results back
cuMemFree()         # Free memory
```


These calls happen in user-space, through shared libraries like libcuda.so and libcudart.so. And here's the problem: you can't see them.


## The GPU Opacity Problem
Traditional monitoring hits a wall at the GPU driver boundary. When your training job slows down, you see symptoms (low GPU utilization) but not causes (inefficient API usage).

**Real examples from the field:**

- Memory leaks: Unmatched cuMemAlloc() / cuMemFree() calls causing OOM after hours
- Launch overhead: 10,000 tiny kernel launches instead of 100 batched ones
- Sync bottlenecks: Unnecessary cuStreamSynchronize() calls stalling the GPU
- Silent errors: CUDA errors not being checked, leading to wrong results

**eBPF uprobes Work :**

Unlike kernel probes that hook into the Linux kernel, uprobes attach to user-space functions. Perfect for CUDA libraries.


```console
// Hook into CUDA Runtime Library
SEC("uprobe/cuMemAlloc")
int trace_cu_mem_alloc_enter(struct pt_regs *ctx) {
    // Capture function arguments and timing
}

SEC("uretprobe/cuMemAlloc") 
int trace_cu_mem_alloc_exit(struct pt_regs *ctx) {
    // Capture return values and calculate duration
}
```

## Architecture and Hook Points

**Primary targets:**

```console
# CUDA Runtime Library
/usr/local/cuda/lib64/libcudart.so.12
/usr/lib/x86_64-linux-gnu/libcudart.so.12

# CUDA Driver Library  
/usr/lib/x86_64-linux-gnu/libcuda.so.1
```

Key functions to monitor:

1. Memory Management
    - `cuMemAlloc` / `cuMemFree` – Track allocations and leaks
    - `cuMemcpyHtoD` / `cuMemcpyDtoH` – Monitor data transfers
    - `cuMemAllocManaged` – Watch unified memory usage
2. Kernel Execution
    - `cuLaunchKernel` – Track kernel launches and grid sizes
    - `cuLaunchCooperativeKernel` – Monitor cooperative kernels
3. Stream Operations
    - `cuStreamCreate` / `cuStreamDestroy` – Watch stream lifecycle
    - `cuStreamSynchronize` – Detect sync overhead

The Technical Challenges
1. Function Signature Complexity

```
// Complex pointer arguments
CUresult cuMemAlloc(CUdeviceptr* dptr, size_t bytesize);
```

eBPF can’t easily dereference user-space pointers. Solution: Capture arguments on entry, results on exit.

```
# Different CUDA versions = different symbols
cuMemAlloc@CUDA_11.0
cuMemAlloc@CUDA_12.0
```

You need dynamic symbol resolution or multiple hooks.

3. Performance Impact CUDA calls can happen 10,000+ times per second. Your eBPF program must be fast (<1ms) or you’ll slow down the very thing you’re monitoring.

4. Error Code Interpretation
```
typedef enum CUresult {
    CUDA_SUCCESS = 0,
    CUDA_ERROR_OUT_OF_MEMORY = 2,
    CUDA_ERROR_INVALID_VALUE = 1,
    // ... 100+ error codes
} CUresult;
```

You need error code lookup tables in eBPF.

## Building the Monitor
The skeleton program above shows how to:

- Track Memory Allocations: Hook cuMemAlloc entry/exit to monitor size, timing, and success
- Detect Memory Leaks: Maintain a hash map of allocated pointers, remove on cuMemFree
- Monitor Kernel Launches: Capture grid dimensions and launch timing
- Stream to Userspace: Use ring buffers to send events to your monitoring application

What you get:

- Real-time CUDA API call tracing
- Memory allocation/deallocation tracking
- Kernel launch frequency and timing
- Error detection and reporting
- Zero-overhead monitoring (when done right)

### Case Study 1: The Memory Allocation Nightmare

**The Problem:**

```
# What the ML team's training loop looked like (simplified)
for epoch in range(100):
    for batch in dataloader:
        # This innocent-looking line was the culprit
        temp_buffer = torch.cuda.FloatTensor(batch_size, hidden_size)  # 1GB allocation
        
        # Process batch
        output = model(batch, temp_buffer)
        loss = criterion(output, targets)
        
        # temp_buffer goes out of scope here
        # PyTorch calls cuMemFree() via garbage collection
```

What was happening under the hood:

```
// Every single batch iteration was doing this:
cuMemAlloc(&device_ptr, 1073741824);  // 1GB allocation
// ... do work ...
cuMemFree(device_ptr);                // Free 1GB
```

### The Hidden Cost:
- cuMemAlloc() isn't just a pointer assignment - it's a complex operation
- GPU memory allocator needs to find contiguous 1GB blocks
- Memory fragmentation builds up over time
- Each allocation takes ~100–500 microseconds
- 1,000 batches × 500μs = 500ms of pure allocation overhead per epoch

### How eBPF Revealed This:
```
# eBPF output showing the pattern
PID    FUNCTION       SIZE        DURATION    RESULT
1234   cuMemAlloc     1073741824  412μs       SUCCESS
1234   cuMemFree      1073741824  23μs        SUCCESS
1234   cuMemAlloc     1073741824  438μs       SUCCESS  
1234   cuMemFree      1073741824  25μs        SUCCESS
# ... repeated 1,000 times per epoch
```

### The Fix:
```
# Pre-allocate buffer once
temp_buffer = torch.cuda.FloatTensor(batch_size, hidden_size)  # One 1GB allocation

for epoch in range(100):
    for batch in dataloader:
        # Reuse the same buffer
        temp_buffer.fill_(0)  # Clear previous data
        output = model(batch, temp_buffer)
        loss = criterion(output, targets)
```

Result: 40% training time reduction because:

- Eliminated 999 unnecessary cuMemAlloc() calls per epoch
- Reduced memory fragmentation
- Improved cache locality
- Less GPU memory allocator contention

## Final Thoughts
Monitoring CUDA at the API level unlocks visibility into a world previously opaque to developers.

With eBPF uprobes, you gain:

- Real-time tracing of CUDA API calls
- Memory tracking with leak detection
- Kernel launch profiling
- Silent error capture
- Minimal runtime overhead

> Modern GPU observability is no longer optional.
> It’s the key to unlocking the performance you paid for.

## Tools to Explore
- bcc / bpftrace
- cuda-gdb
- Grafana + Prometheus with custom BPF exporters
- bpftool, perf, nm, readelf for symbol debugging

## Want to try it?
Drop a comment or DM me. I’m working on an open-source eBPF profiler for CUDA workloads. Early testers welcome. 🚀




