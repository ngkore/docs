# eBPF : Unveiling the Future of Computing

Welcome to my blog, where we dive deep into the world of technology and explore the cutting-edge innovations that shape our future. In today’s episode, we’re going to discuss a revolutionary technology called eBPF (Extended Berkeley Packet Filter) and its potential to transform the computing landscape. Join me as we explore the near future of eBPF and its profound implications for various industries.

*Captivating Hook:*

> To kickstart our blog, let’s imagine a world where software can reshape the way we interact with computers. Sounds intriguing, right? Well, that’s precisely what eBPF promises to deliver — the power to redefine computing as we know it.

## What is eBPF?

eBPF(Extended Berkeley Packet Filter) is a framework that let’s user run custom code in the kernel in a sandboxed way. You can conceive of it as a lightweight, sandboxed virtual machine (VM) within the Linux kernel. It allows programmers to run Berkeley Packet Filter (BPF) bytecode
that makes use of certain kernel resources.

![alt text](photos/ebpf/ebpf-01.webp)

## Key features of eBPF:

1. Safe and Sandboxed Execution Environment
2. Low overhead and high performance

3. Dynamic code injection and tracing capabilities

4. Efficient and flexible data collection and analysis

5. Widely supported across various operating systems

### How does eBPF work?

eBPF (Extended Berkeley Packet Filter) works by leveraging a combination of bytecode, JIT (Just-In-Time) compilation, and hooks within the Linux kernel to provide a powerful framework for dynamic code execution and system introspection.

### eBPF Progrmas:
At the core of eBPF are eBPF programs, which are small snippets of code written in a restricted domain-specific language. These programs are designed to perform specific tasks, such as packet filtering, system call interception, or data analysis. eBPF programs are compiled into bytecode, a low-level representation of the code that can be executed by the eBPF virtual machine.

For example, a framework called BCC allows you to write eBPF code in C, compiles it to eBPF bytecode using a Clang/LLVM compiler and loads it into the kernel. Behind the scenes, BCC does this loading in the kernel using the bpf() system call.

### eBPF verifier:
The eBPF verifier. Once the program is sent into the kernel after making the bpf() call, the verifier will traverse the potential paths the program may take when executed in the kernel, making sure the program does indeed run to completion without any looping that would cause a kernel lockup. Other checks, from valid register state, program size, to out of bound jumps, must also be met.

### JIT(Just In Time compiler)
After verification, eBPF bytecode is just-in-time (JIT) compiled into native machine code. eBPF has a modern design, meaning it has been upgraded to be 64-bit encoded with 11 total registers. This closely maps eBPF to hardware for x86_64, ARM, and arm64 architecture, amongst others. Fast compilation at runtime makes it possible for eBPF to remain performant even as it must first pass through a VM.

### Hooks
Now the translated eBPF programs are attached to hooks within the Linux kernel. Hooks are specific entry points in the kernel’s execution flow where eBPF programs can intercept and modify the behavior of the kernel or specific subsystems.


![alt text](photos/ebpf/ebpf-02.webp)


### eBPF Maps:
To store and share data between the program and kernel or user spaces, eBPF makes use of maps. As implied by the name, maps are key-value pairs. Supporting a number of different data structures, like hash tables, arrays, and tries, programs are able to send and receive data in maps using helper functions.

## eBPF Use Cases:

a. Security

Extending the basic capabilities of seeing and interpreting all system calls and providing packet and socket-level views of all networking operations enables the development of revolutionary approaches to system security.

Typically, entirely independent systems have handled different aspects of system call filtering, process context tracing, and network-level filtering. On the other hand, eBPF facilitates the combination of control and visibility over all aspects. This allows you to develop security systems that operate with more context and an improved level of control.

b. Observability

Rather than relying on gauges and static counters exposed by the operating system, eBPF allows for the generation of visibility events and the collection and in-kernel aggregation of custom metrics based on a broad range of potential sources.

This increases the depth of visibility that might be attained and decreases the overall system overhead dramatically. This is achieved by collecting only the required visibility data and by producing histograms and similar data structures at the source of the event, rather than depending on the export of samples.

c. Networking

The combination of efficiency and programmability makes eBPF a good candidate for all networking solutions’ packet processing requirements. The programmability of eBPF provides a means of adding additional protocol parsers, and smoothly programs any forwarding logic to address changing requirements without ever exiting the Linux kernel’s packet processing context. The effectiveness offered by the JIT compiler offers execution performance near that of natively compiled in-kernel code.

d. Tracing and Profiling

The ability to attach eBPF programs to trace points in addition to kernel and user application probe points enables visibility into the runtime behavior of applications as well as the system.

By providing introspection capabilities to both the system and the application side, both views can be combined. This gives unique and powerful insights to troubleshoot system performance issues. Advanced statistical data structures let you extract useful visibility data in an effective way, without needing the export of huge amounts of sampling data that is typical for similar systems.

> Conclusion: eBPF is not just a buzzword; it’s a game-changer that holds immense potential for the future of computing. Its ability to dynamically inject and execute code within the kernel opens up endless possibilities across various industries.

