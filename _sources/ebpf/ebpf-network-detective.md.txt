# eBPF: The Network Detective
**How I Used eBPF to Solve a Mysterious 2AM Production Outage**
<hr>
It was 2:03 AM when my phone buzzed with the familiar dread of a PagerDuty alert. Half-asleep, I squinted at the screen: **"CRITICAL: API response times spiking - 95th percentile timeout errors increasing"**. What started as another routine midnight fire drill would become one of the most educational debugging sessions of my career—and a testament to why eBPF has become indispensable in my observability toolkit.

## The Symptoms: When Everything Looks Normal

After stumbling to my laptop with coffee in hand, I dove into our monitoring dashboards. The metrics painted a confusing picture:

- **CPU utilization**: Normal (~30% across all instances)
- **Memory usage**: Well within limits
- **Database performance**: Query times looked healthy
- **Load balancer metrics**: Even distribution of traffic
- **Application logs**: No obvious errors or exceptions

Yet our API was hemorrhaging. Response times that normally sat around 200ms were spiking to 30+ seconds before timing out. The pattern was maddeningly intermittent—some requests sailed through while others hung indefinitely.



## The False Leads: When Traditional Tools Hit Their Limits

### Dead End #1: Application Layer Investigation

My first instinct was to blame the application. I scaled up our API instances, thinking we might be hitting some hidden bottleneck. No improvement. I examined recent deployments—nothing had changed in 72 hours.

### Dead End #2: Database Deep Dive

Next, I suspected database connection pooling issues. Our PostgreSQL metrics looked clean, but I increased the connection pool size anyway. Still nothing.

### Dead End #3: Infrastructure Rabbit Holes

Maybe it was the cloud provider? I checked AWS status pages, examined ELB metrics, and even opened a support ticket. Everything appeared normal from their perspective.

```bash
# Typical troubleshooting commands that yielded no insights
kubectl top pods
kubectl describe pods api-service-xyz
curl -v https://api.example.com/health
```

Three hours in, I was stumped. Our traditional observability stack—Prometheus, Grafana, ELK—was telling me everything was fine while our users were experiencing a catastrophic service degradation.

## The Breakthrough: Thinking Below the Application Layer

At 5:47 AM, fueled by frustration and my fourth cup of coffee, I had an epiphany. What if the issue wasn't *what* we were monitoring, but *where* we were monitoring?

All our observability focused on application metrics and infrastructure resources. But what about the network layer? What if packets were getting lost, delayed, or malformed somewhere between our load balancer and application instances?

This is where eBPF entered the story.

## Enter eBPF: The Network Microscope

eBPF (Extended Berkeley Packet Filter) allows you to run sandboxed programs directly in the Linux kernel without changing kernel source code. Think of it as a microscope for your network stack—you can observe, measure, and trace network events with surgical precision.

Instead of guessing what might be wrong, I could now *see* exactly what was happening to every packet flowing through our system.

## The Investigation: Tracing the Invisible

### Step 1: Basic Packet Capture with tcpdump

First, I established a baseline with traditional packet capture:

```bash
# Capture packets on the primary network interface
sudo tcpdump -i eth0 -n -c 1000 host api.example.com

# Sample output showing normal traffic
14:23:41.123456 IP 10.0.1.100.45678 > 10.0.2.50.8080: Flags [S], seq 1234567890, win 29200
14:23:41.124567 IP 10.0.2.50.8080 > 10.0.1.100.45678: Flags [S.], seq 987654321, ack 1234567891, win 28960
```

The three-way handshake looked normal, but I needed deeper visibility into what was happening after the connection was established.

### Step 2: eBPF-powered TCP Analysis

Using `bpftrace`, I created a custom probe to monitor TCP window sizes and scaling factors:

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

The output immediately revealed something suspicious:

```
PID: 12847, Window: 65535, Scale: 0
PID: 12847, Window: 32768, Scale: 7
PID: 12851, Window: 65535, Scale: 0
Window scaling negotiation: 0
PID: 12851, Window: 1024, Scale: 7
```

### Step 3: Deep Dive with BCC Tools

The inconsistent window scaling caught my attention. I deployed a more sophisticated eBPF program using the BCC toolkit:

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

The eBPF traces revealed that some connections were negotiating window scaling correctly while others weren't. More critically, I noticed that failing connections consistently showed a sender window (`SND_WND`) of 0, indicating the receiver had advertised a zero-byte receive window.



### Understanding the Root Cause

TCP window scaling allows connections to use receive windows larger than 64KB by applying a scaling factor. Here's what was happening:

1. **Normal flow**: Client connects → Window scaling negotiated → Large windows enable high throughput
2. **Broken flow**: Client connects → Window scaling fails → Small windows cause throughput collapse

The issue stemmed from a recent kernel parameter change on our load balancer nodes:

```bash
# The problematic setting
net.ipv4.tcp_window_scaling = 0

# What it should have been
net.ipv4.tcp_window_scaling = 1
```

### The Chain Reaction

With window scaling disabled on the load balancer but enabled on the application servers, we had a TCP window scaling mismatch:

1. Client connects to load balancer (no window scaling)
2. Load balancer forwards to app server (expects window scaling)
3. App server's large receive buffers get constrained by the non-scaled window announcements
4. Effective window size drops to ~1KB instead of the expected 64KB+
5. High-throughput requests stall waiting for tiny window advertisements

## The Resolution: A Simple Fix with Profound Impact

The fix was embarrassingly simple:

```bash
# On all load balancer nodes
echo 'net.ipv4.tcp_window_scaling = 1' >> /etc/sysctl.conf
sysctl -p

# Verify the change
sysctl net.ipv4.tcp_window_scaling
```

Within minutes of applying this change, our API response times dropped back to normal. The 95th percentile went from 30+ seconds to under 300ms.



## Lessons Learned: Why This Happened and How to Prevent It

### The Configuration Drift

The root cause traced back to a well-intentioned security hardening script that had disabled TCP window scaling across our infrastructure. While this might make sense for certain security-sensitive environments, it's generally counterproductive for high-throughput applications.

### Why Traditional Monitoring Missed It

Our application-layer monitoring couldn't see this issue because:

- **CPU and memory usage remained normal** - the applications weren't working harder
- **Connection counts looked healthy** - TCP connections were established successfully
- **Application logs showed no errors** - from the app's perspective, it was just waiting for slow clients

The problem lived in the kernel's network stack, invisible to traditional observability tools.

### eBPF: The Missing Piece

eBPF filled the observability gap by providing:

- **Kernel-level visibility** without kernel modifications
- **Real-time tracing** of network events as they happened
- **Programmable probes** tailored to specific debugging needs
- **Minimal performance overhead** compared to traditional packet capture

## Best Practices: Building Better Network Observability

### 1. Layer Your Monitoring

Don't rely solely on application metrics. Build observability at multiple layers:

```bash
# Application layer
curl -w "@curl-format.txt" -s -o /dev/null https://api.example.com/health

# Transport layer (eBPF)
bpftrace -e 'kprobe:tcp_sendmsg { @bytes = hist(arg2); }'

# Network layer
ss -i  # Show TCP socket details including window scaling
```

### 2. Proactive TCP Health Monitoring

Add these metrics to your regular monitoring:

```bash
# Monitor TCP window scaling usage
ss -i | grep -E "(wscale|rto|cwnd)"

# Track TCP retransmissions
nstat | grep -i retrans

# Monitor receive buffer usage
bpftrace -e 'kprobe:tcp_recvmsg { @recv_buffer = hist(arg2); }'
```

### 3. Configuration Management

Treat network configuration as infrastructure as code:

```yaml
# Ansible example for TCP tuning
- name: Enable TCP window scaling
  sysctl:
    name: net.ipv4.tcp_window_scaling
    value: '1'
    state: present
    reload: yes
```

### 4. eBPF Toolkit Preparation

Keep these eBPF tools in your debugging arsenal:

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

This incident highlighted a fundamental shift in how we need to think about observability. As our systems become more distributed and complex, the gap between application-layer metrics and actual system behavior continues to widen.

### Traditional Observability vs. eBPF-Enhanced Observability

| Traditional | eBPF-Enhanced |
|-------------|---------------|
| Application metrics | Kernel-level visibility |
| Sampling-based | Real-time, complete picture |
| Post-mortem debugging | Live system introspection |
| Limited network insights | Deep packet-level analysis |

### The Future of Network Debugging

eBPF represents a paradigm shift toward **programmable observability**. Instead of hoping your monitoring tools captured the right metrics, you can write custom probes that extract exactly the data you need to solve specific problems.

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

What started as a mysterious production outage at 2 AM became a masterclass in the limitations of traditional monitoring and the power of kernel-level observability. Without eBPF, I might have spent days chasing application-layer ghosts while the real culprit—a simple TCP configuration mismatch—remained hidden in the kernel.

The incident taught me three crucial lessons:

1. **Observability gaps are real and costly** - Traditional monitoring tools excel at their intended scope but can miss critical system-level issues
2. **Network-layer problems require network-layer tools** - Application metrics can't diagnose kernel networking issues
3. **eBPF is not just a debugging tool, it's a new observability paradigm** - The ability to write custom, real-time kernel probes changes how we approach system introspection

As our infrastructure becomes increasingly complex, tools like eBPF transition from "nice to have" to "essential." The next time you're staring at dashboards that show green while your users see red, remember: sometimes you need to look deeper than the application layer to find the truth.

The network detective's toolkit has evolved. Make sure yours has too.