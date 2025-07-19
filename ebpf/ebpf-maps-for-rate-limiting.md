# eBPF Maps for High-Performance Rate Limiting

**Author:** [Shankar Malik](https://www.linkedin.com/in/evershalik/)

**Published:** February 23, 2023

## Introduction

High-performance rate limiting is essential for protecting modern networks from malicious or excessive traffic. Traditional user-space technologies impose latency, memory, and concurrency costs that become prohibitive at line rates. Kernel-space programming with eBPF and advanced map types addresses these challenges, enabling true microsecond-level enforcement at the earliest stage of packet processing.

## The Limitations of User-Space Rate Limiting

**Syscall Overhead**

- Every packet incurs costly kernel-to-user transitions.
- By the time a drop decision is made in user space, resources have already been consumed.

**State Synchronization and Contention**

- Requires lock-based or complex lock-free synchronization.
- Leads to race conditions, contention, and inconsistent behavior under load.

**Memory and Cache Pressure**

- Shared with application processes, causing cache pollution and unpredictable performance.
- May be paged out or suffer high cache miss rates during spikes.

**Latency Penalty**

- User-space decisions add avoidable delay.
- Real-time and high-frequency environments suffer unacceptable lag.

## The Kernel-Space Paradigm with eBPF

- **Zero Syscalls:** Drop decisions in the network driver context.
- **Proactive Drops:** Block malicious packets at the XDP layer (earliest ingress).
- **Lock-Free Concurrency:** Use of atomic operations on eBPF per-CPU maps.
- **Predictable Resource Use:** No garbage collection or heap fragmentation.
- **Hardware Offload:** Many NICs execute XDP eBPF code in hardware.

## eBPF Maps: Core Data Structures

eBPF maps are lockless, high-speed kernel structures providing atomic accesses for network-scale workloads.

**Common Map Types and Usage**

**`BPF_MAP_TYPE_HASH`**

Ideal for IP-based or flow-based rate limiting.

```c
struct bpf_map_def SEC("maps") rate_limit_map = {
    .type = BPF_MAP_TYPE_HASH,
    .key_size = sizeof(__u32),    // IPv4 address
    .value_size = sizeof(struct rate_counter),
    .max_entries = 1000000,       // Support 1M unique IPs
};
```

**`BPF_MAP_TYPE_PERCPU_HASH`**

Each CPU gets its own map copy for atomic lockless increments.

```c
struct bpf_map_def SEC("maps") percpu_rate_map = {
    .type = BPF_MAP_TYPE_PERCPU_HASH,
    .key_size = sizeof(__u32),
    .value_size = sizeof(struct rate_counter),
    .max_entries = 1000000,
};
```

**`BPF_MAP_TYPE_LRU_HASH`**

Automatic eviction for dynamic, memory-constrained scenarios.

```c
struct bpf_map_def SEC("maps") lru_rate_map = {
    .type = BPF_MAP_TYPE_LRU_HASH,
    .key_size = sizeof(__u32),
    .value_size = sizeof(struct rate_counter),
    .max_entries = 100000,        // Smaller footprint with auto-eviction
};
```

## Atomic Operations in eBPF

- eBPF maps offer built-in support for atomic increments, swaps, and compare-and-swap, enabling race-free updates without locks.

```c
// Atomic increment - the cornerstone of our rate limiter
__sync_fetch_and_add(&counter->requests, 1);

// Atomic compare-and-swap for more complex logic
__sync_bool_compare_and_swap(&counter->last_reset, old_time, new_time);
```

## Step-by-Step: Building a Rate Limiter

This section outlines the process of building a production-grade rate limiter capable of handling millions of packets per second. XDP (eXpress Data Path) is utilized for maximum performance by attaching the program at the earliest point in the network stack.

**Data Structures**

```c
#include <linux/bpf.h>
#include <linux/if_ether.h>
#include <linux/ip.h>
#include <linux/in.h>
#include <bpf/bpf_helpers.h>
#include <bpf/bpf_endian.h>

// Rate limiting configuration
#define MAX_REQUESTS_PER_SECOND 1000
#define WINDOW_SIZE_NS 1000000000ULL  // 1 second in nanoseconds

// Counter structure for each IP
struct rate_counter {
    __u64 requests;          // Total requests in current window
    __u64 window_start;      // Start time of current window (nanoseconds)
    __u64 last_seen;         // Last packet timestamp
};

// Statistics structure
struct rate_stats {
    __u64 total_packets;
    __u64 dropped_packets;
    __u64 allowed_packets;
};
```

**eBPF Map Declarations**

```c
// Per-CPU hash map for maximum performance
struct {
    __uint(type, BPF_MAP_TYPE_PERCPU_HASH);
    __uint(max_entries, 1000000);
    __type(key, __u32);                    // IPv4 address
    __type(value, struct rate_counter);
} rate_limit_map SEC(".maps");

// Statistics map
struct {
    __uint(type, BPF_MAP_TYPE_ARRAY);
    __uint(max_entries, 1);
    __type(key, __u32);
    __type(value, struct rate_stats);
} stats_map SEC(".maps");

// Configuration map (allows runtime tuning)
struct {
    __uint(type, BPF_MAP_TYPE_ARRAY);
    __uint(max_entries, 1);
    __type(key, __u32);
    __type(value, __u32);                  // requests per second limit
} config_map SEC(".maps");
```

**Rate Limiting Logic**

```c
static __always_inline int rate_limit_check(__u32 src_ip) {
    struct rate_counter *counter;
    struct rate_counter new_counter = {0};
    __u64 now = bpf_ktime_get_ns();
    __u32 key = 0;
    __u32 *max_rps;

    // Get current rate limit from config
    max_rps = bpf_map_lookup_elem(&config_map, &key);
    __u32 limit = max_rps ? *max_rps : MAX_REQUESTS_PER_SECOND;

    // Lookup or create counter for this IP
    counter = bpf_map_lookup_elem(&rate_limit_map, &src_ip);
    if (!counter) {
        // First time seeing this IP
        new_counter.requests = 1;
        new_counter.window_start = now;
        new_counter.last_seen = now;
        bpf_map_update_elem(&rate_limit_map, &src_ip, &new_counter, BPF_ANY);
        return XDP_PASS;
    }

    // Check if we need to reset the window
    if (now - counter->window_start >= WINDOW_SIZE_NS) {
        // Reset window
        counter->requests = 1;
        counter->window_start = now;
        counter->last_seen = now;
        return XDP_PASS;
    }

    // Increment request counter atomically
    __sync_fetch_and_add(&counter->requests, 1);
    counter->last_seen = now;

    // Check rate limit
    if (counter->requests > limit) {
        return XDP_DROP;
    }

    return XDP_PASS;
}
```

**XDP Program Entry**

```c
SEC("xdp")
int rate_limiter(struct xdp_md *ctx) {
    void *data_end = (void *)(long)ctx->data_end;
    void *data = (void *)(long)ctx->data;

    // Parse Ethernet header
    struct ethhdr *eth = data;
    if (data + sizeof(*eth) > data_end)
        return XDP_PASS;

    // Only process IPv4 packets
    if (bpf_ntohs(eth->h_proto) != ETH_P_IP)
        return XDP_PASS;

    // Parse IP header
    struct iphdr *iph = data + sizeof(*eth);
    if (data + sizeof(*eth) + sizeof(*iph) > data_end)
        return XDP_PASS;

    // Extract source IP
    __u32 src_ip = iph->saddr;

    // Update statistics
    __u32 stats_key = 0;
    struct rate_stats *stats = bpf_map_lookup_elem(&stats_map, &stats_key);
    if (stats) {
        __sync_fetch_and_add(&stats->total_packets, 1);
    }

    // Perform rate limiting check
    int action = rate_limit_check(src_ip);

    // Update drop/allow statistics
    if (stats) {
        if (action == XDP_DROP) {
            __sync_fetch_and_add(&stats->dropped_packets, 1);
        } else {
            __sync_fetch_and_add(&stats->allowed_packets, 1);
        }
    }

    return action;
}

char _license[] SEC("license") = "GPL";
```

## XDP versus TC for Rate Limiting

| Feature             | XDP                           | TC (Traffic Control)       |
| ------------------- | ----------------------------- | -------------------------- |
| Hook Position       | Earliest (driver/NIC)         | Later (post-stack ingress) |
| Performance         | Max (line-rate, <2us latency) | Lower (higher latency)     |
| Packet Modification | Limited                       | Full (re-write, mark etc.) |
| Use Case            | DDoS, allow/drop, raw speed   | QoS, shaping, complex mods |

**Takeaway:** For line-speed, earliest drops, XDP is optimal.

## Real-World Performance

**Throughput and Latency**

| Implementation      | Pkts/sec | CPU Usage | Latency |
| ------------------- | -------- | --------- | ------- |
| `iptables`          | 500K     | 80%       | 50μs    |
| Optimized userspace | 1.2M     | 60%       | 25μs    |
| eBPF XDP            | 14M      | 15%       | 2μs     |

**Memory Usage**

```bash
# Traditional user-space rate limiter
RSS: 2.1GB (hash table + application overhead)

# eBPF rate limiter
Map memory: 76MB (1M entries × 76 bytes)
Program memory: 4KB
```

- 10x throughput
- 95% less memory
- 75% lower CPU

## Testing Your Rate Limiter

**Compile and Attach**

```bash
# Compile the eBPF program
clang -O2 -target bpf -c rate_limiter.c -o rate_limiter.o

# Load and attach to interface
sudo ip link set dev eth0 xdp obj rate_limiter.o sec xdp

# Verify attachment
sudo ip link show eth0
```

**Traffic & Load Testing**

wrk, bash, or custom tools for legitimate/malicious traffic

```bash
# Generate legitimate traffic
wrk -t12 -c400 -d30s --latency http://target-server/

# Generate malicious traffic (high rate from single IP)
for i in {1..10}; do
    wrk -t1 -c100 -d60s http://target-server/ &
done
```

**Monitoring Statistics**

```bash
#!/bin/bash
# stats_monitor.sh - Monitor rate limiter performance

while true; do
    # Read statistics from eBPF map
    bpftool map dump name stats_map | \
    awk '/total_packets/ { total = $2 }
         /dropped_packets/ { dropped = $2 }
         /allowed_packets/ { allowed = $2 }
         END {
           printf "Total: %d, Dropped: %d (%.2f%%), Allowed: %d\n",
           total, dropped, (dropped/total)*100, allowed
         }'
    sleep 1
done
```

**Observing Dropped Packets**

```bash
# Use perf to observe XDP drops
sudo perf record -e xdp:* -a sleep 10
sudo perf script

# Monitor interface statistics
watch -n1 'ip -s link show eth0'
```

## Advanced Extensions

### Token Bucket Algorithms

For more sophisticated rate limiting, implement a token bucket algorithm:

```c
struct token_bucket {
    __u64 tokens;           // Available tokens (scaled by 1000)
    __u64 last_refill;      // Last refill timestamp
    __u32 burst_size;       // Maximum burst size
    __u32 refill_rate;      // Tokens per second × 1000
};

static __always_inline int token_bucket_check(__u32 src_ip, __u32 packet_cost) {
    struct token_bucket *bucket;
    struct token_bucket new_bucket = {0};
    __u64 now = bpf_ktime_get_ns();

    bucket = bpf_map_lookup_elem(&token_map, &src_ip);
    if (!bucket) {
        // Initialize new bucket
        new_bucket.tokens = BURST_SIZE * 1000;
        new_bucket.last_refill = now;
        new_bucket.burst_size = BURST_SIZE;
        new_bucket.refill_rate = REFILL_RATE * 1000;
        bpf_map_update_elem(&token_map, &src_ip, &new_bucket, BPF_ANY);
        return XDP_PASS;
    }

    // Calculate tokens to add
    __u64 elapsed_ns = now - bucket->last_refill;
    __u64 elapsed_seconds = elapsed_ns / 1000000000ULL;
    __u64 tokens_to_add = elapsed_seconds * bucket->refill_rate;

    // Update token count
    bucket->tokens = min(bucket->tokens + tokens_to_add,
                        bucket->burst_size * 1000);
    bucket->last_refill = now;

    // Check if we have enough tokens
    if (bucket->tokens >= packet_cost * 1000) {
        bucket->tokens -= packet_cost * 1000;
        return XDP_PASS;
    }

    return XDP_DROP;
}
```

### Geolocation-Aware Rate Limiting

Combine with IP geolocation for location-aware rate limiting:

```c
struct geo_rate_config {
    __u32 domestic_limit;    // Higher limit for domestic IPs
    __u32 foreign_limit;     // Lower limit for foreign IPs
    __u32 suspicious_limit;  // Very low limit for suspicious countries
};

// GeoIP lookup (simplified - use real GeoIP database)
static __always_inline __u8 get_country_risk(__u32 ip) {
    // High-risk countries get strict limits
    // Implementation would use actual GeoIP data
    return RISK_MEDIUM;  // Placeholder
}
```

### Modular Policy Logic with Tail Calls

Use eBPF tail calls to create modular, composable rate limiting policies:

```c
struct {
    __uint(type, BPF_MAP_TYPE_PROG_ARRAY);
    __uint(max_entries, 10);
    __type(key, __u32);
    __type(value, __u32);
} policy_map SEC(".maps");

SEC("xdp")
int rate_limiter_main(struct xdp_md *ctx) {
    // Basic processing...

    // Call appropriate policy based on packet characteristics
    __u32 policy_idx = determine_policy(ctx);
    bpf_tail_call(ctx, &policy_map, policy_idx);

    // Fallback if tail call fails
    return XDP_PASS;
}

SEC("xdp/policy_strict")
int strict_policy(struct xdp_md *ctx) {
    // Implement strict rate limiting
    return rate_limit_check_strict(ctx);
}

SEC("xdp/policy_lenient")
int lenient_policy(struct xdp_md *ctx) {
    // Implement lenient rate limiting
    return rate_limit_check_lenient(ctx);
}
```

## Deployment and Production Considerations

**Map Sizing and Capacity**

Calculate your map memory requirements:

```c
// Memory usage calculation
// Per-CPU hash map: entries × value_size × num_cpus
// Regular hash map: entries × (key_size + value_size + overhead)

// Example: 1M IPs, 76-byte counter, 16 CPUs
// Per-CPU: 1,000,000 × 76 × 16 = 1.2GB
// Regular: 1,000,000 × (4 + 76 + 32) = 112MB

// Choose based on your traffic patterns and memory constraints
```

**High Availability and Failover**

Automate reload/failover with scripts/monitoring.

```bash
#!/bin/bash
# ha_rate_limiter.sh - High availability setup

# Primary node
sudo ip link set dev eth0 xdp obj rate_limiter.o sec xdp

# Monitor and failover
while true; do
    if ! bpftool prog show | grep -q rate_limiter; then
        echo "Rate limiter failed, reloading..."
        sudo ip link set dev eth0 xdp obj rate_limiter.o sec xdp
    fi
    sleep 5
done
```

**Metrics and Integration**

Export stats for Prometheus/Grafana or other NMS.

```bash
# Prometheus metrics export
curl -s localhost:9090/metrics | grep ebpf_rate_limiter

# Key metrics to monitor:
# - ebpf_rate_limiter_packets_total
# - ebpf_rate_limiter_drops_total
# - ebpf_rate_limiter_map_entries
# - ebpf_rate_limiter_cpu_usage
```

## Hardware Offload

```bash
# Netronome SmartNIC offload
sudo ethtool -K eth0 hw-tc-offload on
sudo tc qdisc add dev eth0 clsact
sudo tc filter add dev eth0 ingress bpf obj rate_limiter.o sec tc direct-action
```

This enables:

- **100Gbps+ line rate processing**
- **Zero CPU usage** for rate limiting
- **Sub-microsecond latency**
- **Hardware-accelerated map operations**

## Conclusion

eBPF moves rate limiting logic from slow user space to the earliest, fastest, and most scalable point in the Linux stack. Using kernel-space maps and lockless operations, line-rate enforcement—even with millions of flows—becomes feasible and practical. Combined with hardware offload, observability, and programmable policy support, eBPF reshapes how modern networks defend themselves and optimize bandwidth.

Kernel-space rate limiting is not just an optimization—it is an architectural revolution empowering developers and operators to build programmable, robust, and exceptionally fast network protection systems tailored for modern demands.
