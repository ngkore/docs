# Building an eBPF Process Monitor with Go

**Author:** [Satyam Dubey](https://www.linkedin.com/in/satyam-dubey-142598258/)

**Published:** February 16, 2025

## Introduction

eBPF (Extended Berkeley Packet Filter) enables advanced, safe, and high-performance observability, networking, and security by allowing sandboxed programs to run safely in the Linux kernel. eBPF systems provide real-time monitoring and deep kernel/system introspection, all without kernel modifications.

<br>

This tutorial demonstrates how to build a simple process monitor with eBPF and Go. The monitor tracks each time a process on the system executes via the `execve` syscall, recording process ID (PID) and command name using a Go frontend and the Cilium eBPF library.

## Prerequisites

- Linux Kernel 5.x or later (`uname -r`)
- Clang and LLVM (for eBPF program compilation)
- bpftool and libbpf (for program/map handling)
- Go 1.18+ (`go version`)

### Install dependencies (Ubuntu/Debian):

```console
sudo apt update
sudo apt install clang llvm libbpf-dev libelf-dev linux-headers-$(uname -r) bpftool
go install github.com/cilium/ebpf/cmd/bpf2go@latest
```

_Reference code/build guide repo: [GitHub - eBPF Process Monitor](https://github.com/Satyam-git-hub/eBPF_process_monitor.git)_

---

## 1. Writing the eBPF Program

Create a project directory and source file:

```console
mkdir ebpf_monitor && cd ebpf_monitor
mkdir ebpf
nano ebpf/ebpf_monitor.c
```

**`ebpf/ebpf_monitor.c`**

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

This program:

- Hooks into the `sys_enter_execve` tracepoint
- Captures PID and process name (`comm`)
- Sends events to a perf buffer

## 2. Generating eBPF Bytecode Using bpf2go

Instead of invoking clang manually, bpf2go (from Cilium eBPF) auto-generates Go bindings and object files:

<br>

Add this to your `main.go`:

```console
//go:generate go run github.com/cilium/ebpf/cmd/bpf2go -target bpf -go-package=main EbpfMonitoring ebpf/ebpf_monitor.c -- -I. -O2 -Wall -g
```

Run:

```console
go generate
```

This creates:

- Compiled BPF object file
- Corresponding Go bindings (e.g., `ebpfmonitoring_bpf.go`)

```console
Compiled /home/ubuntu/ebpf_project/ebpfmonitoring_bpf.o
Stripped /home/ubuntu/ebpf_project/ebpfmonitoring_bpf.o
Wrote /home/ubuntu/ebpf_project/ebpfmonitoring_bpf.go
```

## 3. Writing the Go Program

Create a Go file to load and run the eBPF program (Go Loader):

<br>

**`main.go`**

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

**Key points:**

- Loads eBPF program and object files using generated Go code
- Attaches to the execve syscall tracepoint
- Reads `Event` objects (PID, command) from the perf buffer and prints them

## 4. Compiling and Running the Program

1. Generate the eBPF Bytecode

`go generate`

2. Build the Go Loader

`go build -o monitor ./go_monitor_objects.go ./ebpfmonitoring_bpf.go`

3. Run the eBPF Process Monitor

```bash
sudo ./monitor
```

**Expected Output**

```console
eBPF program running... Press Ctrl+C to exit.
Process Executed: PID=12345, Command=bash
Process Executed: PID=67890, Command=python
```

> All code and supplementary guides are available at: [github.com/Satyam-git-hub/eBPF_process_monitor](https://github.com/Satyam-git-hub/eBPF_process_monitor)
