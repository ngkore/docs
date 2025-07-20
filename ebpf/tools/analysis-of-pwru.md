# Analysis of PWRU

**Author:** [Nikhil Jangid](https://www.linkedin.com/in/nikhil-jangid-ab6625269/)

**Published:** April 26, 2025

## Introduction to eBPF

eBPF (Extended Berkeley Packet Filter) has dramatically advanced the fields of observability, monitoring, and system interaction within the Linux kernel. Originally intended for packet filtering, eBPF now allows secure execution of small programs inside the Linux kernel space—without requiring kernel code modifications or reboots. These programs can attach to a range of system events, including networking, syscalls, tracing, and security—even at production runtime. This capability enhances fine-grained control and deep visibility.

<br>

In the networking domain, eBPF brings powerful tools for tracing, filtering, and manipulating traffic across various protocol layers with negligible overhead. **PWRU** is a standout tool leveraging these capabilities.

## What is PWRU?

PWRU, standing for "**Packet, Where Are You?**", is an open-source, eBPF-powered packet tracer developed by the Cilium team. It enables engineers, developers, and observability practitioners to trace the complete lifecycle of packet flow across the Linux kernel networking stack.

<br>

PWRU achieves this by dynamically attaching **kprobes** to a targeted set of kernel functions, observing packet movement in real time without requiring custom kernel builds. It tracks packets through interfaces, routing, firewall, and socket layers, providing comprehensive network path traceability.

Additionally, PWRU uses **libpcap** for familiar tcpdump-like filtering, allowing targeted tracing on packets of interest.

## How Does PWRU Work?

PWRU's internal functioning is based on two key kernel introspection technologies:

- **BTF (BPF Type Format):** Kernel-provided type and structure information (from `vmlinux`) that enables precise, version-independent introspection and parsing of kernel structures.
- **kprobes:** Dynamic kernel probes that enable instrumentation of kernel function entry points.

PWRU leverages the BTF data from `/sys/kernel/btf/vmlinux` to interpret kernel data structures such as `sk_buff` for each kernel. This facilitates automatic Go binding generation (`vmlinux.h`) and robust, version-resilient event parsing.

This approach enables PWRU to comprehensively trace kernel network functions without custom kernel module development or rewriting code per kernel release.

## BPF Programs and kprobes in PWRU

The primary capability of PWRU comes from its support for dynamic, multi-point tracing:

- eBPF programs are attached to kprobes at a set of predefined kernel functions (e.g., ip_rcv, tcp_v4_rcv).
- At each probe, the eBPF code collects metadata: interface, packet protocol, IP/port, process ID, and relevant packet attributes.
- This data is transferred to userspace via optimized BPF maps for processing and display.

At every kernel tracepoint, up to five eBPF programs may be attached, each able to capture different trace features—enabling a thorough, hierarchical tracing experience for packet lifecycles in the kernel.

## Deep Dive into PWRU Internals

PWRU captures and processes packet and event data through the use of specific structures and mapped buffers:

- `skb_meta`: Maintains metadata such as netns, mark, interface index, length, MTU, protocol.
- `tuple`: Stores source/destination IP and port for TCP/UDP tuples.
- `event_t`: Aggregates metadata and event context: timestamp, sk_buff pointer, PID, and attributes.

**BPF maps used:**

- `events`: Perf buffers or ring buffers to send events to user space.
- `skb_addresses`, `skb_stackid`, `stackid_skb`: Help track packet lifecycle and kernel stack traces.
- `print_stack_map`: Persists collected kernel stack traces.

**Helper functions:**

- `get_netns()`: Fetches packet network namespace.
- `filter_meta()`: Applies meta-based filters (e.g., netns, marks, interface).
- `set_meta()`, `set_tuple()`: Populate structures using header parsing logic.

**Filtering:**

- L2/L3 pcap-style filters (`filter_pcap_l2`, `filter_pcap_l3`).
- Main filtering logic (`filter()`) combines all criteria.

A Go-based frontend continuously reads from the BPF maps, transforms the event data, and generates a user-friendly real-time trace output.

## Setting up PWRU: Prerequisites, Installation, and Testing

### Prerequisites

Prior to building and running PWRU, the system must include:

- clang, llvm: For compiling the BPF bytecode
- go: Golang toolchain
- gcc: C toolchain
- bison, byacc, yacc, flex: For parser generation and kernel header builds
- libpcap-dev: Pcap filter parsing library

```console
sudo apt update
sudo apt install -y clang llvm gcc make flex bison byacc yacc libpcap-dev golang
```

### Building PWRU from Source

Clone and build as follows:

```console
# Clone the PWRU GitHub repository
git clone https://github.com/cilium/pwru.git
# Navigate to the project directory
cd pwru
# Build the project
make
```

This process automatically compiles both the eBPF and Go userspace code and links them into the final `pwru` binary.

### Running PWRU

Administrative privileges are required to run PWRU, as it interacts with kernel tracing infrastructure.

```console
sudo ./pwru [options] [pcap-filter]
```

PWRU supports tcpdump-style command-line filters for targeted tracing.

#### Example: Tracing ICMP (ping) Packets

```
sudo ./pwru --output-tuple icmp
```

This traces packets matching the ICMP protocol layer and prints the source/destination tuple.

**Sample Output:**

```console
2025/04/26 12:34:14 Attaching kprobes (via kprobe-multi)...
1642 / 1642 [----------------------------------------------------------------------------------------------------------------------------------] 100.00% ? p/s
2025/04/26 12:34:14 Attached (ignored 0)
2025/04/26 12:34:14 Listening for events..
SKB                CPU PROCESS          NETNS      MARK/x        IFACE       PROTO  MTU   LEN   TUPLE FUNC
0xffff99cf11aa4100 0   <empty>:0        4026531840 0             eth0:2      0x0800 1500  58    192.168.6.1:0->192.168.6.236:0(icmp) napi_gro_receive
0xffff99cf11aa4100 0   <empty>:0        4026531840 0             eth0:2      0x0800 1500  58    192.168.6.1:0->192.168.6.236:0(icmp) dev_gro_receive
0xffff99cf11aa4100 0   <empty>:0        4026531840 0             eth0:2      0x0800 1500  58    192.168.6.1:0->192.168.6.236:0(icmp) inet_gro_receive
0xffff99cf08de1100 0   <empty>:0        4026531840 0             eth0:2      0x0800 1500  68    192.168.6.1:0->192.168.6.236:0(icmp) napi_gro_receive
0xffff99cf08de1100 0   <empty>:0        4026531840 0             eth0:2      0x0800 1500  68    192.168.6.1:0->192.168.6.236:0(icmp) dev_gro_receive
0xffff99cf08de1100 0   <empty>:0        4026531840 0             eth0:2      0x0800 1500  68    192.168.6.1:0->192.168.6.236:0(icmp) inet_gro_receive
0xffff99cf11aa4100 0   <empty>:0        4026531840 0             eth0:2      0x0800 1500  58    192.168.6.1:0->192.168.6.236:0(icmp) skb_defer_rx_timestamp
0xffff99cf08de1100 0   <empty>:0        4026531840 0             eth0:2      0x0800 1500  68    192.168.6.1:0->192.168.6.236:0(icmp) skb_defer_rx_timestamp
0xffff99cf11aa4100 0   <empty>:0        4026531840 0             eth0:2      0x0800 1500  58    192.168.6.1:0->192.168.6.236:0(icmp) ip_rcv_core
0xffff99cf08de1100 0   <empty>:0        4026531840 0             eth0:2      0x0800 1500  68    192.168.6.1:0->192.168.6.236:0(icmp) ip_rcv_core
0xffff99cf11aa4100 0   <empty>:0        4026531840 0             eth0:2      0x0800 1500  58    192.168.6.1:0->192.168.6.236:0(icmp) nf_hook_slow
0xffff99cf11aa4100 0   <empty>:0        4026531840 0             eth0:2      0x0800 1500  58    192.168.6.1:0->192.168.6.236:0(icmp) nf_ip_checksum
0xffff99cf11aa4100 0   <empty>:0        4026531840 0             eth0:2      0x0800 1500  58    192.168.6.1:0->192.168.6.236:0(icmp) __skb_checksum_complete
0xffff99cf11aa4100 0   <empty>:0        4026531840 0             eth0:2      0x0800 1500  58    192.168.6.1:0->192.168.6.236:0(icmp) skb_ensure_writable
0xffff99cf11aa4100 0   <empty>:0        4026531840 0             eth0:2      0x0800 1500  58    192.168.6.1:0->192.168.6.236:0(icmp) nf_ip_checksum
0xffff99cf08de1100 0   <empty>:0        4026531840 0             eth0:2      0x0800 1500  68    192.168.6.1:0->192.168.6.236:0(icmp) nf_hook_slow
0xffff99cf08de1100 0   <empty>:0        4026531840 0             eth0:2      0x0800 1500  68    192.168.6.1:0->192.168.6.236:0(icmp) nf_ip_checksum
0xffff99cf08de1100 0   <empty>:0        4026531840 0             eth0:2      0x0800 1500  68    192.168.6.1:0->192.168.6.236:0(icmp) __skb_checksum_complete
```

Each output row shows a packet (`skb`) and its traversal across various kernel functions, relevant interface, tuple, and metadata, allowing precise code-path tracing and network subsystem introspection.

## Conclusion

PWRU is a robust, practical, and extensible eBPF-based tracing tool, allowing deep packet-level visibility inside the Linux networking stack. By leveraging real-time kprobes, modern BPF facilities, and user-friendly frontend design, it provides a powerful utility for:

- Debugging complex networking workflows
- Investigating kernel-level processing paths
- Understanding kernel packet lifecycle in detail
- Diagnosing performance bottlenecks and anomalies

PWRU's simple installation, support for portable and expressive filters, and real-time reporting capabilities make it a valuable asset—both for researchers and practitioners—within high-performance Linux networking and kernel observability domains.
