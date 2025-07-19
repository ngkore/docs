# eBPF Network Debugging and Analysis

**Author:** [Shankar Malik](https://www.linkedin.com/in/evershalik/)

**Published:** June 27, 2025

**How I Used eBPF to Solve a Mysterious 2AM Production Outage**

It was 2:03 AM when a PagerDuty alert indicated API response time degradation. Standard metrics (CPU, memory, database, load balancer, logs) appeared normal, but latency and timeout errors increased for end users.

## The Symptoms: When Everything Looks Normal

Despite healthy dashboard visuals, actual API latency was climbing, and error rates increased, with normal resource consumption across the stack.

## The False Leads: When Traditional Tools Hit Their Limits

### Application Layer Investigation

Scaling API instances and reviewing recent deployments produced no benefit or actionable insights.

### Database Analysis

Database health and connection pooling were confirmed to be normal; increasing pool sizes did not solve the issue.

### Infrastructure Evaluation

Cloud provider status, load balancer metrics, and system logs failed to reveal root causes.

```bash
# Typical troubleshooting commands that yielded no insights
kubectl top pods
kubectl describe pods api-service-xyz
curl -v https://api.example.com/health
```

## The Breakthrough: Network-Layer Focus

Traditional monitoring did not reveal network-specific symptoms. Hypothesizing the issue was related to packet transmission or kernel networking, the investigation turned to eBPF observability for lower-layer visibility.

## Enter eBPF: The Network Microscope

eBPF (Extended Berkeley Packet Filter) facilitates dynamic, sandboxed measurements of kernel events and network behavior. It allows on-the-fly instrumentation for detailed, real-time network analysis without custom kernel changes or service disruption.

## The Investigation: Tracing the Invisible

### Step 1: Packet Capture – Establishing a Baseline

```bash
# Capture packets on the primary network interface
sudo tcpdump -i eth0 -n -c 1000 host api.example.com

# Sample output of TCP SYN handshake
14:23:41.123456 IP 10.0.1.100.45678 > 10.0.2.50.8080: Flags [S], seq 1234567890, win 29200
14:23:41.124567 IP 10.0.2.50.8080 > 10.0.1.100.45678: Flags [S.], seq 987654321, ack 1234567891, win 28960
```

The initial three-way handshake appeared normal; however, deeper visibility was required into the events occurring after the connection was established.

### Step 2: eBPF-powered TCP Analysis

Using `bpftrace`, created a custom probe to monitor TCP window sizes and scaling factors throughout the session.

```bash
# Monitor TCP window scaling events
sudo bpftrace -e '
kprobe:tcp_select_window {
    printf("PID: %d, Window: %d, Scale: %d\n", 
           pid, arg1, arg2);
}

kprobe:tcp_window_scaling {
    printf("Window scaling negotiation: %d\n", arg0);
}'
```


Observed output:

```
PID: 12847, Window: 65535, Scale: 0
PID: 12847, Window: 32768, Scale: 7
PID: 12851, Window: 65535, Scale: 0
Window scaling negotiation: 0
PID: 12851, Window: 1024, Scale: 7
```

### Step 3: Advanced eBPF with BCC Python

The inconsistent window scaling required further investigation. Created a more advanced eBPF program using the `BCC` toolkit to analyze the behavior in greater detail.

```python
#!/usr/bin/env python3
from bcc import BPF

# eBPF program to trace TCP window scaling
bpf_program = """
#include <net/sock.h>
#include <linux/tcp.h>

BPF_HASH(tcp_windows, u32, u32);

int trace_tcp_window(struct pt_regs *ctx) {
    struct sock *sk = (struct sock *)PT_REGS_PARM1(ctx);
    struct tcp_sock *tp = tcp_sk(sk);
    
    u32 pid = bpf_get_current_pid_tgid() >> 32;
    u32 window = tp->rcv_wnd;
    tcp_windows.update(&pid, &window);
    
    bpf_trace_printk("PID: %d, RCV_WND: %d, SND_WND: %d\\n", 
                     pid, tp->rcv_wnd, tp->snd_wnd);
    return 0;
}
"""

b = BPF(text=bpf_program)
b.attach_kprobe(event="tcp_recvmsg", fn_name="trace_tcp_window")

print("Tracing TCP windows... Hit Ctrl-C to end.")
b.trace_print()
```

Running this revealed a clear pattern:

```
PID: 12847, RCV_WND: 65535, SND_WND: 0
PID: 12847, RCV_WND: 65535, SND_WND: 0
PID: 12851, RCV_WND: 32768, SND_WND: 16384
PID: 12851, RCV_WND: 32768, SND_WND: 16384
```

## The Smoking Gun: TCP Window Scaling Misconfiguration

The eBPF traces revealed that some connections were negotiating window scaling correctly while others were not. More critically, failing connections consistently displayed a sender window (SND_WND) of zero, indicating that the receiver had advertised a zero-byte receive window.

### Understanding the Root Cause

TCP window scaling enables the use of receive windows larger than 64KB by applying a scaling factor. The sequence of events was as follows:

1. **Normal flow**: Client connects, window scaling is negotiated, large windows enable high throughput.
2. **Broken flow**: Client connects, window scaling fails, small windows result in a throughput collapse.

The core of the problem was a recent change to a kernel parameter on the load balancer nodes:

```bash
# The problematic setting
net.ipv4.tcp_window_scaling = 0

# What it should have been
net.ipv4.tcp_window_scaling = 1
```

### The Chain Reaction

A mismatch occurred because window scaling was disabled on the load balancer but enabled on the application servers:

1. Client connects to the load balancer (window scaling disabled).
2. Load balancer forwards to the application server (expects window scaling).
3. The application server’s large receive buffers are constrained by the non-scaled window announcements.
4. The effective window size decreases to approximately 1KB instead of the expected 64KB or greater.
5. High-throughput requests stall, pending tiny window advertisements.

## The Resolution: A Simple Fix with Profound Impact

The issue was resolved with a straightforward kernel parameter update on all load balancer nodes:

```bash
# On all load balancer nodes
echo 'net.ipv4.tcp_window_scaling = 1' >> /etc/sysctl.conf
sysctl -p

# Verify the change
sysctl net.ipv4.tcp_window_scaling
```

Within minutes, API response times returned to normal; the 95th percentile dropped from over 30 seconds to under 300ms.

## Lessons Learned: Root Cause and Prevention

### The Configuration Drift

Investigation revealed that the cause was a security hardening script that disabled TCP window scaling infrastructure-wide. While this might be appropriate for certain restricted environments, it is typically detrimental in high-throughput scenarios.

### Why Traditional Monitoring Missed It

Standard observability stacks failed to expose the problem because:

- CPU and memory utilization appeared normal.
- Connection counts remained healthy; TCP connections were still successful.
- Application logs contained no specific errors; from the app’s perspective, responses were simply slow.

The bottleneck was hidden within the kernel’s networking stack, beyond the reach of application-layer and traditional system metrics.

### eBPF: The Missing Piece

eBPF provided the necessary observability by enabling:

- Kernel-level visibility without kernel code changes.
- Real-time network event tracing.
- Programmable, targeted probes for custom debugging.
- Minimal performance overhead compared to full packet capture.

## Best Practices: Building Better Network Observability

### 1. Layered Monitoring

Effective observability requires multiple layers:

```bash
# Application layer
curl -w "@curl-format.txt" -s -o /dev/null https://api.example.com/health

# Transport layer (eBPF)
bpftrace -e 'kprobe:tcp_sendmsg { @bytes = hist(arg2); }'

# Network layer
ss -i  # Show TCP socket details including window scaling
```

### 2. Proactive TCP Health Monitoring

Regularly track these key network metrics:

```bash
# Monitor TCP window scaling usage
ss -i | grep -E "(wscale|rto|cwnd)"

# Track TCP retransmissions
nstat | grep -i retrans

# Monitor receive buffer usage
bpftrace -e 'kprobe:tcp_recvmsg { @recv_buffer = hist(arg2); }'
```

### 3. Configuration Management

Manage tunables like TCP window scaling as infrastructure-as-code using configuration management systems:

```yaml
# Ansible example for TCP tuning
- name: Enable TCP window scaling
  sysctl:
    name: net.ipv4.tcp_window_scaling
    value: '1'
    state: present
    reload: yes
```

### 4. Prepare an eBPF Toolkit

Maintain core eBPF tools for rapid debugging and kernel observability:

```bash
# Install BCC tools
sudo apt install bpfcc-tools

# Essential networking eBPF tools
tcpconnect    # Trace TCP connections
tcpaccept     # Trace TCP accepts
tcpretrans    # Trace TCP retransmissions
tcplife       # Summarize TCP session lifespans
```

## The Bigger Picture: Why eBPF Matters for Modern Infrastructure

This incident demonstrates the evolving requirements for observability in distributed, dynamic infrastructure. As system complexity increases, the divide between application-level metrics and true system behavior widens.

### Traditional Observability vs. eBPF-Enhanced Observability

| Traditional                | eBPF-Enhanced                      |
|----------------------------|------------------------------------|
| Application metrics        | Kernel-level visibility            |
| Sampling-based             | Real-time, full-fidelity tracing   |
| Post-mortem debugging      | Live system introspection          |
| Limited network diagnostics| Deep packet/protocol analysis      |

### The Future of Network Debugging

eBPF enables **programmable observability**. Instead of depending on generic metrics, targeted probes can extract the exact kernel data required for fast incident resolution.

```bash
# Custom eBPF probe for this specific issue
bpftrace -e '
kprobe:tcp_select_window {
    if (arg1 == 0) {
        printf("Zero window detected! PID: %d, Comm: %s\n", 
               pid, comm);
    }
}'
```

## Conclusion: The Detective's New Tools

A mysterious production outage that would have confounded traditional monitoring tools was resolved through eBPF-powered introspection. The real problem—a kernel-level TCP configuration mismatch—was invisible at the application layer.

Key takeaways:

1. Observability gaps have significant cost: Standard monitoring stacks can miss root-cause issues.
2. Network-layer problems require direct, network-centric tools: Application metrics rarely highlight kernel network stack misconfigurations.
3. eBPF represents a new observability paradigm: Programmable, granular kernel probes reshape system troubleshooting.

In modern infrastructure, eBPF and similar tools are no longer optional—they are essential. When standard dashboards all show “green” but users are experiencing outages, the truth is often found deeper than the application stack.

Expand the network troubleshooting toolkit—kernel-level observability is a competitive necessity.