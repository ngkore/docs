# Building an eBPF Process Monitor with Go: A Step-by-Step Guide

## Introduction
eBPF (Extended Berkeley Packet Filter) is revolutionizing Linux observability, networking, and security by allowing safe, high-performance execution of sandboxed programs in the kernel. It enables real-time monitoring and system introspection without modifying the kernel code.

In this guide, we’ll walk through writing a simple eBPF process monitoring tool using Go. This tool will track whenever a process executes the execve syscall, capturing the process ID (PID) and command name.

We’ll use the Cilium eBPF library (github.com/cilium/ebpf) to load and interact with the eBPF program from Go, making it easier to integrate eBPF with modern applications.

Prerequisites
To follow along, ensure you have the following:

- Linux Kernel 5.x or later (Check with uname -r).
- Clang and LLVM (for compiling eBPF programs).
- bpftool and libbpf (for working with eBPF maps and programs).
- Go 1.18+ installed (Check with go version).

Installing Dependencies (Ubuntu/Debian)
```console
sudo apt update
sudo apt install clang llvm libbpf-dev libelf-dev linux-headers-$(uname -r) bpftool
go install github.com/cilium/ebpf/cmd/bpf2go@latest
```
> Note: you can get all the code and build guide in the github repo: https://github.com/Satyam-git-hub/eBPF_process_monitor.git

### Step 1: Writing the eBPF Program
First, we’ll write an eBPF program in C that hooks into the execve syscall to capture process executions.

Create a new directory for the project and add the eBPF C file:

```console
mkdir ebpf_monitor && cd ebpf_monitor
mkdir ebpf
nano ebpf/ebpf_monitor.c
```

#### ebpf/ebpf_monitor.c
```c
#include <linux/bpf.h>
#include <linux/ptrace.h>
#include <linux/sched.h>
#include <bpf/bpf_helpers.h>


#define TASK_COMM_LEN 16
struct event {
    __u32 pid;
    char comm[TASK_COMM_LEN];
};
struct {
    __uint(type, BPF_MAP_TYPE_PERF_EVENT_ARRAY);
    __uint(max_entries, 128);
} events SEC(".maps");
SEC("tracepoint/syscalls/sys_enter_execve")
int monitor_exec(struct trace_event_raw_sys_enter *ctx) {
    struct event evt = {};
    struct task_struct *task;
    task = (struct task_struct *)bpf_get_current_task();
    evt.pid = bpf_get_current_pid_tgid() >> 32;
    bpf_get_current_comm(&evt.comm, sizeof(evt.comm));
    bpf_perf_event_output(ctx, &events, BPF_F_CURRENT_CPU, &evt, sizeof(evt));
    return 0;
}
char _license[] SEC("license") = "GPL";
```

**Explanation**

- Hooks into the sys_enter_execve tracepoint to monitor process executions.<br>
- Stores process details (PID and command name) in an eBPF perf buffer.<br>
- Uses bpf_perf_event_output() to send captured events to user space.<br>

### Step 2: Generating eBPF Bytecode Using bpf2go
Instead of manually compiling with clang, we’ll use bpf2go to generate eBPF bindings for Go.

#### Modify Your Go File (main.go)
```console
//go:generate go run github.com/cilium/ebpf/cmd/bpf2go -target bpf -go-package=main EbpfMonitoring ebpf/ebpf_monitor.c -- -I. -O2 -Wall -g
```

This command:

- Compiles ebpf_monitor.c into BPF bytecode.<br>
- Generates Go bindings (ebpf_monitor_bpfeb.go and ebpf_monitor_bpfel.go).<br>

Now, run the command:
```console
go generate
```
This should generate:
```console
Compiled /home/ubuntu/ebpf_project/ebpfmonitoring_bpf.o
Stripped /home/ubuntu/ebpf_project/ebpfmonitoring_bpf.o
Wrote /home/ubuntu/ebpf_project/ebpfmonitoring_bpf.go
```

### Step 3: Writing the Go Program

Now, let’s write the Go loader that:

- Loads the eBPF program into the kernel.<br>
- Attaches it to the execve syscall tracepoint.<br>
- Reads events from the eBPF perf buffer.<br>

#### Create `main.go`

```go
package main

//go:generate go run github.com/cilium/ebpf/cmd/bpf2go -target bpf -go-package=main EbpfMonitoring ebpf/ebpf_monitor.c -- -I. -O2 -Wall -g
import (
 "bytes"
 "encoding/binary"
 "fmt"
 "log"
 "os"
 "os/signal"
 "syscall"
 "github.com/cilium/ebpf/link"
 "github.com/cilium/ebpf/perf"
)
// Struct matching the eBPF event
type Event struct {
 Pid  uint32
 Comm [16]byte
}
func main() {
 // Load the compiled eBPF program
 objs := EbpfMonitoringObjects{}
 if err := LoadEbpfMonitoringObjects(&objs, nil); err != nil {
  log.Fatalf("Failed to load eBPF objects: %v", err)
 }
 defer objs.Close()
 // Attach the eBPF program to the execve syscall tracepoint
 tp, err := link.Tracepoint("syscalls", "sys_enter_execve", objs.MonitorExec, nil)
 if err != nil {
  log.Fatalf("Failed to attach tracepoint: %v", err)
 }
 defer tp.Close()
 // Open the perf buffer to read events
 rd, err := perf.NewReader(objs.Events, os.Getpagesize())
 if err != nil {
  log.Fatalf("Failed to open perf buffer: %v", err)
 }
 defer rd.Close()
 fmt.Println("eBPF program running... Press Ctrl+C to exit.")
 // Handle OS signals for graceful shutdown
 sigChan := make(chan os.Signal, 1)
 signal.Notify(sigChan, os.Interrupt, syscall.SIGTERM)
 go func() {
  var e Event
  for {
   record, err := rd.Read()
   if err != nil {
    log.Printf("Failed to read from perf buffer: %v", err)
    continue
   }
   // Parse binary data
   if err := binary.Read(bytes.NewBuffer(record.RawSample), binary.LittleEndian, &e); err != nil {
    log.Printf("Failed to decode event: %v", err)
    continue
   }
   fmt.Printf("Process Executed: PID=%d, Command=%s\n", e.Pid, string(e.Comm[:]))
  }
 }()
 <-sigChan
 fmt.Println("Exiting...")
}
```


### Step 4: Compiling and Running the Program
Now, let’s build and run the process monitor.

1️⃣ Generate the eBPF Bytecode

```go generate```

2️⃣ Compile the Go Loader

```go build -o monitor ./go_monitor_objects.go ./ebpfmonitoring_bpf.go```

3️⃣ Run the eBPF Process Monitor

```sudo ./monitor```

✅ Expected Output

If successful, you should see:
```console
eBPF program running... Press Ctrl+C to exit.
Process Executed: PID=12345, Command=bash
Process Executed: PID=67890, Command=python
```
