# Unlocking Network Performance with XDP and eBPF

XDP, eXpress Data Path, is a high-performance networking technology in the Linux kernel that allows for fast and efficient packet processing at the earliest stage of the networking stack. It operates within the kernel space and provides a programmable interface for handling incoming packets directly on the network interface card (NIC), bypassing much of the traditional networking stack.

![alt text](photos/xdp-ebpf/xdp-ebpf-01.webp)


## Why XDP?

XDP is a technology that allows developers to attach eBPF programs to low-level hooks, implemented by network device drivers in the Linux kernel, as well as generic hooks that run after the device driver.

![alt text](photos/xdp-ebpf/xdp-ebpf-02.webp)


XDP can be used to achieve high-performance packet processing in an eBPF architecture, primarily using kernel bypass. This greatly reduces the overhead needed for the kernel, because it does not need to process context switches, network layer processing, interrupts, and so on. Control of the network interface card (NIC) is transferred to an eBPF program. This is especially important while working at higher network speeds — 10 Gbps and above.

The kernel bypass method has some drawbacks:

* eBPF programs have to write their own drivers.
* XDP programs run before packets are parsed. This means that eBPF programs must directly implement functionality they need to do their job, without relying on the kernel.

XDP makes it easier to implement high-performance networking in eBPF, by allowing eBPF programs to directly read and write network packet data, and determine how to process the packets, before reaching the kernel level.

XDP programs can be directly attached to a network interface. Whenever a new packet is received on the network interface, XDP programs receive a callback, and can perform operations on the packet very quickly.

You can connect an XDP program to an interface using the following models:

* **Generic XDP** — XDP programs are loaded into the kernel as part of the ordinary network path. This does not provide full performance benefits, but is an easy way to test XDP programs or run them on generic hardware that does not provide specific support for XDP.
* **Native XDP** — The XDP program is loaded by the network card driver as part of its initial receive path. This also requires support from the network card driver.
* **Offloaded XDP** — The XDP program loads directly on the NIC, and executes without using the CPU. This requires support from the network interface device.

## XDP Hooks:

![alt text](photos/xdp-ebpf/xdp-ebpf-03.webp)


* **XDP_DROP** — Drops and does not process the packet. eBPF programs can analyze traffic patterns and use filters to update the XDP application in real time to drop specific types of packets (for example, malicious traffic).
* **XDP_PASS** — Indicates that the packet should be forwarded to the normal network stack for further processing. The XDP program can modify the content of the package before this happens.
* **XDP_TX** — Forwards the packet (which may have been modified) to the same network interface that received it.
* **XDP_REDIRECT** — Bypasses the normal network stack and redirects the packet via another NIC to the network.

## AF_XDP

![alt text](photos/xdp-ebpf/xdp-ebpf-04.webp)


Load balancing: AF_XDP sockets allow user-space applications to receive redirected packets and distribute the traffic across multiple backend servers or processing units. This enables effective distribution of network load and optimizes resource utilization.

## Traffic control

By the time a network packet reaches this point it will be in kernel memory in the form of an sk_buff. This is a data structure that’s used throughout the kernel’s network stack. eBPF programs attached within the TC subsystem receive a pointer to the sk_buff structure as the context parameter.

A given piece of network data in the stack flows in one of two directions: ingress (inbound from the network interface) or egress (outbound toward the network interface). eBPF programs can be attached in either direction and will affect traffic only in that direction. Unlike XDP, it’s possible to attach multiple eBPF programs that will be processed in sequence.

Traffic control is split into classifiers, which classify packets based on some rule, and separate actions, which are taken based on the output from a classifier and determine what to do with a packet. There can be a series of classifiers, all defined as part of a qdisc or queuing discipline.

eBPF programs are attached as a classifier, but they can also determine what action to take within the same program. The action is indicated by the program’s return code (whose values are defined in linux/pkt_cls.h):

* **TC_ACT_SHOT** tells the kernel to drop the packet.
* **TC_ACT_UNSPEC** behaves as if the eBPF program hadn’t been run on this packet (so it would be passed to the next classifier in the sequence, if there is one).
* **TC_ACT_OK** tells the kernel to pass the packet to the next layer in the stack.
* **TC_ACT_REDIRECT** sends the packet to the ingress or egress path of a different network device.

![alt text](photos/xdp-ebpf/xdp-ebpf-05.webp)


## Use Cases for XDP

Here are a few common use cases for XDP in eBPF.

### DDoS Mitigation and Firewalling

One of the basic functions of XDP in eBPF is to use XDP_DROP, which tells the driver to drop packets at an early stage. This lets you apply a variety of efficient network strategies, while keeping the cost of each packet very low.

This is great for situations where you need to deal with any type of DDoS attack, but more generally, using XDP, eBPF can implement any type of firewall policy with very little overhead. XDP can handle these scenarios, for example, by scrubbing illegitimate traffic and forwarding legitimate packets to their destination using `XDP_TX`.

XDP can either be deployed in a standalone network appliance, or distributed to multiple nodes that protect the host. The latter scenario can be implemented using `XDP_PASS` or `cpumap` `XDP_REDIRECT`. To boost performance, you can use offloaded XDP, which shifts the already small cost of each data packet entirely to the NIC, which is processed at wire speed.

> XDP in eBPF represents a paradigm shift in networking, offering unprecedented performance, flexibility, and programmability. With its ability to offload packet processing to the NIC level and execute custom eBPF programs, XDP enables new possibilities in terms of speed, efficiency, and network control. From enhancing network performance in data centers to securing network infrastructure and enabling real-time analytics, XDP in eBPF is transforming the way we build and operate networks.

> As the adoption of XDP and eBPF continues to grow, we can expect to see even more
