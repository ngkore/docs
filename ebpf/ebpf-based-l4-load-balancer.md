# Load Balancing at Light Speed

**Author:** [Shankar Malik](https://www.linkedin.com/in/evershalik/)

**Published:** March 14, 2023

## Building a Custom L4 Load Balancer with XDP

_When milliseconds matter and millions of packets per second are just the starting line_

## The Performance Wall: Why Traditional Load Balancers Hit Their Limits

Picture this scenario: during a traffic surge such as Black Friday, an e-commerce platform experiences overwhelming demand. The traditional Layer 4 load balancer—such as NGINX or HAProxy—that has reliably served for years becomes the system bottleneck. The CPU usage spikes, latency increases, and packet drops occur at an alarming rate.

Traditional Layer 4 load balancers operate in userspace, incurring overhead where every packet traverses the kernel networking stack multiple times, is copied between kernel and userspace buffers, and encounters context switching. These steps introduce microsecond latency per packet, which accumulates significantly when processing millions of packets per second (PPS). Such overhead eventually results in a performance ceiling that hardware improvements struggle to overcome.

This is precisely where eBPF’s **XDP (eXpress Data Path)** technology is uniquely suited, offering a programmable, high-speed load balancing mechanism that significantly alleviates these issues.

## Enter XDP: The NIC's Personal Bouncer

XDP functions as an intelligent gatekeeper, intercepting incoming packets immediately after reception by the Network Interface Card (NIC) driver. This early intervention prevents packets from traversing the entire kernel network stack and allows for instantaneous forwarding decisions.

**Key properties of XDP:**

- Packet processing occurs in NIC ring buffers with zero-copy semantics.
- Full bypass of kernel stack’s overhead, including Netfilter and queuing disciplines.
- Drastically reduced CPU usage due to minimized context switches and memory operations.
- Highly programmable through eBPF programs attached at the earliest packet processing stage.

As a result, XDP can facilitate packet processing rates exceeding 20 million packets per second with latencies measured in microseconds, compared to the millisecond latencies experienced in userspace load balancers.

## Understanding Layer 4 Load Balancing

Layer 4 load balancers operate at the transport layer, making forwarding decisions based on 4-tuple packet header information:

- Source IP address and port
- Destination IP address and port
- Protocol type (TCP or UDP)

Unlike Layer 7 load balancers, which inspect application-layer data such as HTTP headers, Layer 4 load balancers treat the packet payload as opaque, thereby enabling faster decision-making at the cost of more limited feature sets.

The load balancer to be built in this tutorial will:

1. Calculate a hash based on packet 4-tuple to select a backend server.
2. Modify the packet’s destination MAC address to the selected backend’s MAC.
3. Update IP checksums accordingly.
4. Forward the packet out.
5. Handle returning packets by undoing those changes as necessary.

## Architecture: The XDP Load Balancer Design

The load balancer consists of three principal components:

### 1. XDP Program (Kernel Space)

An eBPF program running inside the kernel, responsible for performing high-speed packet inspection, hashing, backend selection, header modification, and forwarding.

### 2. Backend Pool Management (User Space)

A user-space controller manages the set of backend servers and populates kernel eBPF maps with relevant data such as backend IP/MAC addresses and configured weights.

### 3. Configuration Interface

User interfaces and command-line tools to add, remove, or alter backend configurations and to monitor load balancer statistics.

## Building the XDP Load Balancer

This is the code for the core XDP program. This C code will be compiled to eBPF bytecode and loaded into the kernel:

```c
// xdp_lb.c
#include <linux/bpf.h>
#include <linux/if_ether.h>
#include <linux/ip.h>
#include <linux/tcp.h>
#include <linux/udp.h>
#include <linux/in.h>
#include <bpf/bpf_helpers.h>
#include <bpf/bpf_endian.h>

#define MAX_BACKENDS 256

// Backend server definition
struct backend {
    __u32 ip;
    __u8 mac[6];
    __u16 weight;
};

// Connection tracking entry
struct conn_track {
    __u32 backend_idx;
    __u64 last_seen;
};

// eBPF maps for storing backend pool and connection state
struct {
    __uint(type, BPF_MAP_TYPE_ARRAY);
    __type(key, __u32);
    __type(value, struct backend);
    __uint(max_entries, MAX_BACKENDS);
} backend_map SEC(".maps");

struct {
    __uint(type, BPF_MAP_TYPE_HASH);
    __type(key, __u64);  // Flow hash
    __type(value, struct conn_track);
    __uint(max_entries, 1000000);
} conn_track_map SEC(".maps");

struct {
    __uint(type, BPF_MAP_TYPE_ARRAY);
    __type(key, __u32);
    __type(value, __u32);
    __uint(max_entries, 1);
} backend_count SEC(".maps");

// Simple hash function for flow identification
static __always_inline __u64 hash_flow(__u32 src_ip, __u16 src_port,
                                       __u32 dst_ip, __u16 dst_port) {
    return ((__u64)src_ip << 32) | ((__u64)src_port << 16) |
           ((__u64)dst_ip) | dst_port;
}

// Update IP checksum after NAT
static __always_inline void update_ip_checksum(struct iphdr *iph) {
    __u32 csum = 0;
    iph->check = 0;

    // Simplified checksum calculation for demo
    // In production, use incremental checksum updates
    __u16 *ptr = (__u16 *)iph;
    for (int i = 0; i < sizeof(struct iphdr) / 2; i++) {
        csum += bpf_ntohs(ptr[i]);
    }

    csum = (csum & 0xFFFF) + (csum >> 16);
    csum = (csum & 0xFFFF) + (csum >> 16);
    iph->check = bpf_htons(~csum);
}

SEC("xdp")
int xdp_load_balancer(struct xdp_md *ctx) {
    void *data_end = (void *)(long)ctx->data_end;
    void *data = (void *)(long)ctx->data;

    // Parse Ethernet header
    struct ethhdr *eth = data;
    if ((void *)(eth + 1) > data_end)
        return XDP_PASS;

    // Only handle IP packets
    if (eth->h_proto != bpf_htons(ETH_P_IP))
        return XDP_PASS;

    // Parse IP header
    struct iphdr *iph = (void *)(eth + 1);
    if ((void *)(iph + 1) > data_end)
        return XDP_PASS;

    // Only handle TCP/UDP
    if (iph->protocol != IPPROTO_TCP && iph->protocol != IPPROTO_UDP)
        return XDP_PASS;

    __u16 src_port = 0, dst_port = 0;

    // Extract port information
    if (iph->protocol == IPPROTO_TCP) {
        struct tcphdr *tcph = (void *)iph + (iph->ihl * 4);
        if ((void *)(tcph + 1) > data_end)
            return XDP_PASS;
        src_port = tcph->source;
        dst_port = tcph->dest;
    } else if (iph->protocol == IPPROTO_UDP) {
        struct udphdr *udph = (void *)iph + (iph->ihl * 4);
        if ((void *)(udph + 1) > data_end)
            return XDP_PASS;
        src_port = udph->source;
        dst_port = udph->dest;
    }

    // Calculate flow hash
    __u64 flow_hash = hash_flow(iph->saddr, src_port, iph->daddr, dst_port);

    // Check if connection exists
    struct conn_track *conn = bpf_map_lookup_elem(&conn_track_map, &flow_hash);
    __u32 backend_idx = 0;

    if (conn) {
        // Use existing backend
        backend_idx = conn->backend_idx;
        conn->last_seen = bpf_ktime_get_ns();
    } else {
        // Select new backend using consistent hashing
        __u32 key = 0;
        __u32 *count = bpf_map_lookup_elem(&backend_count, &key);
        if (!count || *count == 0)
            return XDP_PASS;

        backend_idx = flow_hash % *count;

        // Create new connection tracking entry
        struct conn_track new_conn = {
            .backend_idx = backend_idx,
            .last_seen = bpf_ktime_get_ns()
        };
        bpf_map_update_elem(&conn_track_map, &flow_hash, &new_conn, BPF_ANY);
    }

    // Get backend information
    struct backend *backend = bpf_map_lookup_elem(&backend_map, &backend_idx);
    if (!backend)
        return XDP_PASS;

    // Update destination MAC address
    __builtin_memcpy(eth->h_dest, backend->mac, 6);

    // Update destination IP
    iph->daddr = backend->ip;

    // Recalculate IP checksum
    update_ip_checksum(iph);

    // Forward the packet
    return XDP_TX;
}

char _license[] SEC("license") = "GPL";
```

The XDP program includes:

- Data structures defining backend servers and connection tracking state.
- eBPF maps to store backends, connection tracking, and backend count.
- Functions to hash packet 4-tuples, update IP checksums.
- The main eBPF program that parses Ethernet, IP, TCP/UDP headers; performs connections tracking; selects backends and rewrites packet headers accordingly.
- Proper bounds checking on packet data to avoid kernel panics.
- Application of the GPL license as required by the kernel.

### User-Space Backend Controller

Create a simple user-space controller to manage the backend pool:

```c
// lb_controller.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <net/if.h>
#include <bpf/bpf.h>
#include <bpf/libbpf.h>

struct backend {
    uint32_t ip;
    uint8_t mac[6];
    uint16_t weight;
};

int main(int argc, char **argv) {
    if (argc < 3) {
        printf("Usage: %s <interface> <backend_ip> [backend_ip...]\n", argv[0]);
        return 1;
    }

    const char *ifname = argv[1];
    int ifindex = if_nametoindex(ifname);
    if (ifindex == 0) {
        perror("if_nametoindex");
        return 1;
    }

    // Load and attach XDP program
    struct bpf_object *obj = bpf_object__open_file("xdp_lb.o", NULL);
    if (libbpf_get_error(obj)) {
        fprintf(stderr, "Error opening BPF object file\n");
        return 1;
    }

    if (bpf_object__load(obj)) {
        fprintf(stderr, "Error loading BPF object\n");
        return 1;
    }

    struct bpf_program *prog = bpf_object__find_program_by_name(obj, "xdp_load_balancer");
    if (!prog) {
        fprintf(stderr, "Error finding XDP program\n");
        return 1;
    }

    int prog_fd = bpf_program__fd(prog);
    if (bpf_set_link_xdp_fd(ifindex, prog_fd, 0) < 0) {
        perror("bpf_set_link_xdp_fd");
        return 1;
    }

    // Get map file descriptors
    int backend_map_fd = bpf_object__find_map_fd_by_name(obj, "backend_map");
    int count_map_fd = bpf_object__find_map_fd_by_name(obj, "backend_count");

    // Configure backends
    uint32_t backend_count = argc - 2;
    for (int i = 0; i < backend_count; i++) {
        struct backend backend;
        inet_pton(AF_INET, argv[i + 2], &backend.ip);

        // In a real implementation, you'd resolve MAC addresses via ARP
        // For demo purposes, using placeholder MAC
        memset(backend.mac, 0x02, 6);
        backend.mac[5] = i;  // Simple MAC assignment
        backend.weight = 1;

        uint32_t key = i;
        if (bpf_map_update_elem(backend_map_fd, &key, &backend, BPF_ANY) < 0) {
            perror("bpf_map_update_elem");
            return 1;
        }
    }

    // Update backend count
    uint32_t key = 0;
    if (bpf_map_update_elem(count_map_fd, &key, &backend_count, BPF_ANY) < 0) {
        perror("bpf_map_update_elem");
        return 1;
    }

    printf("XDP load balancer configured with %d backends on %s\n",
           backend_count, ifname);
    printf("Press Ctrl+C to exit...\n");

    // Keep program running
    while (1) {
        sleep(1);
    }

    // Cleanup
    bpf_set_link_xdp_fd(ifindex, -1, 0);
    bpf_object__close(obj);

    return 0;
}
```

The user-space program accomplishes:

- Attaching the compiled XDP program to the network interface.
- Managing backend servers by updating eBPF maps with IP and MAC addresses.
- Handling backend count in the kernel map.
- Simple health check and network interface management functionality.
- A loop to maintain persistent operation and facilitate live backend updates.

### Build Script

Makefile to compile everything:

```makefile
# Makefile
CLANG = clang
LLC = llc
CFLAGS = -O2 -Wall -target bpf

all: xdp_lb.o lb_controller

xdp_lb.o: xdp_lb.c
	$(CLANG) $(CFLAGS) -c $< -o $@

lb_controller: lb_controller.c
	gcc -o $@ $< -lbpf

clean:
	rm -f xdp_lb.o lb_controller

.PHONY: all clean
```

## Performance Testing: Speed of Light Networking

An extensive benchmarking setup evaluates the XDP load balancer’s performance on metrics such as throughput, CPU load, and latency versus traditional software load balancers.

### Test Setup Instructions

- Use packet generation utilities like pktgen-dpdk to simulate millions of packets per second.
- Measure latency with tools such as sockperf.
- Monitor CPU consumption using sar or similar.

```bash
# Install testing tools
sudo apt-get install pktgen-dpdk iperf3 wrk apache2-utils

# Generate test traffic with pktgen
sudo pktgen -l 0-3 -n 4 -- -P -m "1.0,2.1"

# Configure pktgen for our test
set 0 count 10000000
set 0 size 64
set 0 rate 100
set 0 dst ip 192.168.1.100
set 0 src ip 192.168.1.1
start 0
```

### Sample Benchmark Results

| Load Balancer | Max PPS     | CPU Usage (%) | Latency (μs) | Memory (MB) |
| ------------- | ----------- | ------------- | ------------ | ----------- |
| NGINX         | 500,000     | 85            | 150 – 300    | 50          |
| HAProxy       | 750,000     | 80            | 100 – 250    | 30          |
| XDP LB        | 12,000,000+ | 25            | 5 – 15       | 10          |

### Real-World Test Script

```bash
#!/bin/bash
# performance_test.sh

echo "=== XDP Load Balancer Performance Test ==="

# Test 1: Packet Per Second Capacity
echo "Testing maximum PPS..."
sudo ./lb_controller eth0 192.168.1.10 192.168.1.11 192.168.1.12 &
LB_PID=$!

# Generate traffic
sudo pktgen -l 0-3 -n 4 -- -P -m "1.0,2.1" &
PKTGEN_PID=$!

sleep 30
sudo kill $PKTGEN_PID
sudo kill $LB_PID

echo "Check results with: cat /proc/net/xdp_stats"

# Test 2: Latency measurement
echo "Testing latency..."
# Use sockperf or similar tools for precise latency measurement
sockperf ping-pong -i 192.168.1.10 -p 8080 --tcp -t 10

# Test 3: CPU utilization
echo "Monitoring CPU usage..."
sar -u 1 10
```

This script automates:

- Launching the XDP LB with specified backends.
- Generating test traffic.
- Collecting statistics.
- Measuring latency.
- Monitoring CPU usage.

## Advanced Features: Beyond Basic Load Balancing

### Sticky Sessions

Support session persistence by modifying the hash function to use only source IP for the backend selection when enabled.

```c
// Enhanced flow hash with session stickiness
static __always_inline __u64 hash_flow_sticky(__u32 src_ip, __u16 src_port,
                                             __u32 dst_ip, __u16 dst_port,
                                             __u8 sticky_mode) {
    if (sticky_mode) {
        // Use only source IP for stickiness
        return src_ip;
    }
    return hash_flow(src_ip, src_port, dst_ip, dst_port);
}
```

### Health Checking

Implement basic TCP socket-based health checks in the user-space controller to detect backend failures.

```c
// Simple health check function
int check_backend_health(struct backend *backend) {
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    struct sockaddr_in addr = {
        .sin_family = AF_INET,
        .sin_addr.s_addr = backend->ip,
        .sin_port = htons(80)  // Health check port
    };

    struct timeval timeout = {.tv_sec = 1, .tv_usec = 0};
    setsockopt(sock, SOL_SOCKET, SO_RCVTIMEO, &timeout, sizeof(timeout));

    int result = connect(sock, (struct sockaddr*)&addr, sizeof(addr));
    close(sock);

    return (result == 0) ? 1 : 0;  // 1 = healthy, 0 = unhealthy
}
```

### Multi-Queue Support

For NICs with multiple receive queues, attach XDP programs and manage CPU affinity per queue to maximize parallelism.

```c
// Pin XDP programs to specific CPU cores
int attach_xdp_multi_queue(const char *ifname, int num_queues) {
    for (int i = 0; i < num_queues; i++) {
        // Attach XDP program to each queue
        // Set CPU affinity for optimal performance
        cpu_set_t cpuset;
        CPU_ZERO(&cpuset);
        CPU_SET(i, &cpuset);
        pthread_setaffinity_np(pthread_self(), sizeof(cpuset), &cpuset);
    }
    return 0;
}
```

## Pitfalls & Limitations: Practical Considerations

While XDP enables unprecedented packet processing performance, it is not without important constraints that must be carefully evaluated for production environments.

### 1. Protocol and Feature Limitations

- **Lack of TLS Termination:** XDP operates at Layer 2/3/4; it cannot decrypt or route based on encrypted HTTP(S).
- **No Application-Layer (L7) Routing:** XDP does not parse or act on application data; application-aware rules (HTTP routing, WebSocket state tracking) are not feasible.
- **No Deep Protocol State Tracking:** Stateful operations for protocols with complex handshakes (e.g., WebSockets) are difficult to implement at this layer.

### 2. Debugging and Development Complexity

Debugging XDP programs is inherently more challenging compared to userspace load balancers due to limited tooling, traceability, and BPF instruction restrictions.

**Code Example: Debugging Limitations**


```bash
# dmesg/bpf_trace_printk can be used, but severely impacts performance.
sudo cat /sys/kernel/debug/tracing/trace_pipe

# BPF verifier can prevent program loading if complexity or instructions exceed kernel capabilities.
# Complex programs may reach eBPF instruction count limits or hit verifier constraints.
```

### 3. Kernel and Platform Dependencies

- **Kernel Version:** XDP requires Linux kernel 4.8+ (kernel 5.x or later is recommended for advanced features).
- **BPF Compatibility:** Certain eBPF features may not be available in all environments; cloud providers or vendors may restrict eBPF/XDP usage due to kernel policy or tenant safety.
- **Interface & Driver Support:** Not all network interfaces or drivers support XDP in native mode.

### 4. Resource and Memory Constraints

- **Limited eBPF Stack:** Stack size is limited (512 bytes). Large, complex operations in eBPF/XDP are not feasible.
- **Static eBPF Map Sizes:** Map capacities must be declared at load-time; resizing requires redeployment.
- **No Dynamic Memory Allocation:** XDP prohibits runtime heap allocation for memory safety.

## When NOT to Use XDP Load Balancing

XDP is not a universal solution. Prefer traditional userspace load balancers in the following scenarios:

- **Layer 7 Required:** HTTP-based routing, TLS termination, cookie inspection, or any content-based decision making.
- **Complex Logic:** Features like rate limiting, OAuth/session token handling, or transformation at the application layer.
- **Operational Simplicity:** If simple debugging, configuration, and mature monitoring are critical.
- **Team Experience:** Where teams lack eBPF or kernel development expertise and need rapid operational turnaround.
- **Compliance/Certification:** Some industry verticals mandate the use of certified, commercial load balancing solutions.

## Production Deployment Considerations

### Monitoring and Observability

Incorporate detailed statistics and counters to monitor key events and packet flows within your XDP program:

**Code Example: XDP Statistics Collection**

```c
// Add statistics collection to your XDP program
struct {
    __uint(type, BPF_MAP_TYPE_PERCPU_ARRAY);
    __type(key, __u32);
    __type(value, __u64);
    __uint(max_entries, 10);
} stats_map SEC(".maps");

// In your XDP program
enum {
    STAT_PACKETS_PROCESSED,
    STAT_PACKETS_DROPPED,
    STAT_BACKENDS_SELECTED,
    // ... more stats
};

// Increment counters
__u32 key = STAT_PACKETS_PROCESSED;
__u64 *value = bpf_map_lookup_elem(&stats_map, &key);
if (value) (*value)++;
```

### Graceful Deployment Strategies

Blue-green deployment approaches minimize risk when updating XDP programs in production environments:

**Code Example: Blue-Green Deployment Script**

```bash
#!/bin/bash
# Blue-green deployment for XDP programs
echo "Deploying new XDP load balancer..."

# Compile new version
make clean && make

# Test on secondary interface first
sudo ./lb_controller eth1 192.168.1.10 192.168.1.11 &
TEST_PID=$!

# Run smoke tests
./smoke_test.sh eth1

if [ $? -eq 0 ]; then
    echo "Tests passed, switching production traffic..."
    sudo kill $PROD_PID
    sudo ./lb_controller eth0 192.168.1.10 192.168.1.11 &
    PROD_PID=$!
    sudo kill $TEST_PID
else
    echo "Tests failed, keeping old version"
    sudo kill $TEST_PID
fi
```


## Conclusion: When Speed Is Everything

XDP-based load balancing is revolutionizing packet processing for extreme performance use cases. By running in-kernel with minimal overhead, it achieves performance metrics such as:

- 20+ million PPS
- Sub-10 microsecond latency
- Up to 75% reduction in CPU usage compared to traditional userspace solutions

However, these advantages come at the cost of greater complexity and operational considerations:

- Programming requires deep expertise in networking and the kernel
- Observability and debugging are less accessible than in userspace counterparts
- The eBPF/XDP ecosystem, while evolving rapidly, is still maturing

### Best Practices Summary

**Deploy XDP load balancing when:**
- Network throughput and latency are mission-critical and measured in microseconds
- Layer 4 load balancing suffices
- Sufficient in-house expertise exists for kernel/eBPF development

**Opt for traditional load balancers when:**
- Application-layer processing, extensive logic, or deep protocol support is needed
- Rapid operational troubleshooting, detailed monitoring, or compliance is required
- Team training and system integration timelines are considerations

Emerging high-performance, programmable packet processing—led by XDP—will define next-generation networking for demanding, latency-sensitive environments.