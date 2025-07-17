# PWRU: Debugging Packets and Kernel Flows

## Introduction to eBPF

eBPF (Extended Berkeley Packet Filter) has dramatically changed how we observe, monitor, and interact with the Linux kernel. Originally designed for filtering packets, eBPF now allows programs to run safely inside the Linux kernel without modifying source code or rebooting. These programs can hook into system events like networking, system calls, tracing, and security enforcement, enabling deep observability and control.

In the world of networking, eBPF offers powerful ways to trace, filter, and manipulate packet flows at various layers — from ingress to application delivery — with minimal overhead. One of the standout tools built using this technology is **PWRU**.

## What is PWRU?

PWRU, short for “**Packet, Where Are You?**”, is an open-source, eBPF-based kernel packet tracer developed by the Cilium team. It helps network engineers, kernel developers, and observability enthusiasts trace packet movement **across the entire Linux kernel network stack**.

At its core, PWRU dynamically attaches **kprobes** to various kernel network functions, capturing packet events in real time without needing any kernel modifications. It can follow packets as they flow through interfaces, routing layers, firewalls, and socket layers — making it an invaluable tool for debugging complex networking issues.

In addition, PWRU leverages **libpcap** internally, enabling users to apply familiar `tcpdump`-style filters to trace only the packets they are interested in.

## How Does PWRU Work?

To understand PWRU’s inner working, it’s important to first grasp two fundamental concepts: **BTF (BPF Type Format)** and **kprobes**. Linux kernels provide **BTF** information, which describes the types and structures used internally by the kernel (e.g., network packet structures, socket information). PWRU uses this BTF data — especially from the `vmlinux` file — to interpret network function arguments like `sk_buff` structures safely and correctly.

The `vmlinux` file (often found at `/sys/kernel/btf/vmlinux`) contains a full symbol and structure map of the running kernel. PWRU uses it to automatically generate Go bindings (`vmlinux.h`) and understand how packets are structured inside the kernel memory.

This allows PWRU to trace deeply into kernel networking functions without writing any manual parsing code per kernel version — a huge advantage!

## BPF Programs and kprobes in PWRU

PWRU’s main power lies in its **dynamic tracing**. It attaches **eBPF programs** at **kprobe** points — meaning it hooks into the entry of selected kernel functions.

- Whenever a packet hits a hooked network function (e.g., ip_rcv, tcp_v4_rcv), the attached eBPF program runs.
- The eBPF program collects useful metadata: interface info, packet protocol, IP addresses, port numbers, etc.
- This information is pushed into special **BPF maps** for collection and further processing in userspace (Go application).

At every hook point, **five different instances of BPF programs** can be attached — each capturing different kinds of metadata and packet traces. This multi-hook design allows PWRU to provide a detailed, layered view of packet journeys inside the kernel.

## Deep Dive into PWRU Internals

If you’re curious about the deeper technical details, here’s how PWRU captures and processes packet data internally:

**Key Data Structures**:  

- `skb_meta`: Holds metadata like network namespace ID, mark value, interface index, packet length, MTU, and protocol.  

- `tuple`: Stores 4-tuple information — source and destination IPs and ports (for TCP/UDP flows).  

- `event_t`: Aggregates all relevant event data, including timestamps, sk_buff addresses, process IDs, and extracted metadata.

**Important BPF Maps**:  

- `events`: A ring buffer or perf event map used to push events to user space.  

- `skb_addresses`, `skb_stackid`, `stackid_skb`: Hash maps to track sk_buff lifecycle and stack traces.  
- print_stack_map: Stack trace map to store kernel stack traces.

**Helper Functions**:  
  
- `get_netns`(): Extracts network namespace of the packet.  
- `filter_meta`(): Applies filters based on namespace, mark, interface, etc.  
- `set_meta`() and `set_tuple`(): Parse packet headers and populate metadata fields.

**Filtering Mechanism**:  
  
- PWRU supports **pcap-style filtering** ( `filter_pcap_l3`, `filter_pcap_l2`) based on L2/L3 headers. 
- The main function `filter`() combines all these filters to decide if an event should be reported.

A Go-based frontend application reads from these BPF maps, processes the raw events, formats them nicely, and displays them to users — allowing live monitoring of packet paths through the kernel stack.

## Setting up PWRU: Prerequisites, Installation, and Testing

After understanding the internals of PWRU, let’s now move to setting it up on your own Linux system and start tracing packets!

### Prerequisites

Before building PWRU, you need to ensure a few essential packages and tools are installed on your system. These are required for compiling both the eBPF programs and the Go userspace application:

- **clang** and **llvm**
- go
- gcc
- bison, byacc, yacc, flex
- libpcap-dev

```console
sudo apt update
sudo apt install -y clang llvm gcc make flex bison byacc yacc libpcap-dev golang
```

### Building PWRU from Source

Once all the prerequisites are installed, you can proceed to clone the PWRU repository and build it:

```console
# Clone the PWRU GitHub repository
git clone https://github.com/cilium/pwru.git
# Navigate to the project directory
cd pwru
# Build the project
make
```

If everything is properly set up, the make command will:

- Compile the eBPF object files
- Build the userspace Go application
- Link everything together

At the end of the process, you will find the `pwru` binary in the project root directory, ready to use!

### Running PWRU

Since PWRU interacts directly with kernel functions and eBPF subsystems, you need **root permissions** to run it:

```
sudo ./pwru [options] [pcap-filter]
```

PWRU accepts standard tcpdump -style filters at the command line to select which packets you want to trace.

### Usage

Let’s trace **ICMP** (ping) packets traveling through the kernel:

```
sudo ./pwru --output-tuple icmp
```

This command instructs PWRU to:

- Focus on packets matching the ICMP protocol (Layer 4)
- Print the associated source/destination IPs and ports in the output

You will start seeing output like:

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

Each row represents:

- A packet (`skb`) moving through the Linux kernel,
- Along with metadata like which function (`FUNC`) it visited,
- Which interface (`IFACE`) it came through,
- Packet tuple details (src/dst IP, protocol, etc.).

You can now **observe the exact code path your packets follow** — across functions like  
`napi_gro_receive()`, `dev_gro_receive(`), `inet_gro_receive()`, `ip_rcv_core()`, and so on.

## Conclusion

PWRU is a powerful tool for tracing the life of network packets inside the Linux kernel with **minimal setup and zero code modifications**. By dynamically attaching kprobes to key networking functions, PWRU gives deep visibility into:

- Where packets are processed,
- How they move across different kernel subsystems,
- And where delays, drops, or modifications happen.

It is especially useful for **debugging complex networking issues**, understanding the kernel’s **packet handling internals**, or simply learning how Linux networking works under the hood.

With a simple installation process, standard tcpdump-style filters, and real-time output, PWRU makes kernel packet tracing **accessible even to beginners** while remaining powerful enough for advanced users.

Whether you are diagnosing performance problems, debugging kernel modules, or just exploring, **PWRU gives you a microscope into the Linux networking stack.**
