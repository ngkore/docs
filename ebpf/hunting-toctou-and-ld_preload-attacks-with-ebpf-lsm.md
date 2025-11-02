# Hunting TOCTOU and LD_PRELOAD Attacks with eBPF LSM

**Author:** [Satyam Dubey](https://www.linkedin.com/in/satyam-dubey-142598258/)

**Published:** August 5, 2025

---

How to built an eBPF-powered security system that catches file system race conditions and library injection attacks in real-time using Linux Security Module hooks.

---

## Introduction: The Invisible Threat Landscape

In the world of cybersecurity, some of the most dangerous attacks are those that exploit the fundamental assumptions we make about how systems work. While we focus on network intrusions and malware signatures, attackers are increasingly leveraging **timing vulnerabilities** and **runtime manipulation techniques** that operate in the grey areas between legitimate system calls and malicious behavior.

[GitHub - Satyam-git-hub/ebpf-runtime-guard: Runtime observability with ebpf for security.](https://github.com/Satyam-git-hub/ebpf-runtime-guard)

Excited to share **ebpf-runtime-guard**, an open-source eBPF-based security monitoring system developed to detect (currently) two particularly insidious attack vectors:

1. **TOCTOU (Time-of-Check-to-Time-of-Use) attacks** — Race condition exploits that modify files between security validation and execution.
2. **LD_PRELOAD injection attacks** — Runtime library manipulation that hijacks process execution.

But before diving into the implementation, let’s understand why these attacks are so dangerous and why traditional security tools often miss them.

---

## The Race Against Time: Understanding TOCTOU Attacks

### What is TOCTOU?

**Time-of-Check-to-Time-of-Use (TOCTOU)** represents a fundamental class of race condition vulnerabilities where an attacker exploits the time gap between when a system checks a resource’s properties and when it actually uses that resource.

Consider this seemingly innocent code pattern:

In this tiny window between `access()` and `execve()`, an attacker can:
- Replace the legitimate file with a malicious one
- Modify the file contents
- Change symlink targets
- Alter file permissions

### Real-World TOCTOU Impact

TOCTOU vulnerabilities have been responsible for critical security breaches:
- **sudo vulnerabilities (CVE-2019–14287):** Race conditions in privilege checking
- **Container escapes:** File system manipulation during mount operations
- **setuid exploits:** Permission checks bypassed through timing attacks
- **Kernel vulnerabilities:** Race conditions in file system operations

The challenge with TOCTOU detection is that the attack window can be microseconds to milliseconds long, making it nearly impossible for traditional monitoring tools to catch.

---

## The Invisible Injection: LD_PRELOAD Attacks Explained

### Understanding Dynamic Library Loading

Before we can appreciate LD_PRELOAD attacks, we need to understand how Linux loads shared libraries. When a program starts, the dynamic linker (ld.so) resolves and loads required libraries in a specific order:

1. **LD_PRELOAD libraries** (highest priority)
2. **RPATH/RUNPATH** embedded in the binary
3. **LD_LIBRARY_PATH** environment variable
4. **System directories** (/lib, /usr/lib, etc.)

### The LD_PRELOAD Attack Vector

LD_PRELOAD is a legitimate Linux feature that allows users to specify additional libraries to be loaded before all others. However, this mechanism can be weaponized:

#### A Classic Example

Suppose we override `getuid()` to always return 0 (root):

Compile it, then run:

Output:

Without touching any system binaries or kernel modules, you’ve just faked root identity for that process. Now imagine doing this to sudo, passwd, or any suid-root binary that doesn’t sanitize LD_PRELOAD.

#### Why Is This Dangerous?

Attackers exploit LD_PRELOAD to:
- Hijack authentication mechanisms
- Hide processes, files, or sockets
- Modify file I/O behavior
- Exfiltrate secrets by intercepting reads
- Redirect execution to payloads
- Perform stealthy privilege escalation

To make matters worse, LD_PRELOAD works entirely in user space. No kernel modules, no syscalls — just runtime trickery.

**But There’s a Catch…**

Modern systems have taken steps to restrict LD_PRELOAD abuse:
- SUID binaries ignore LD_PRELOAD by default (for security reasons)
- Tools like AppArmor, SELinux, and seccomp can prevent such injections
- However… many userland daemons and tools remain vulnerable if they don’t sanitize environment variables properly

This is where eBPF LSM comes in like a cybersecurity Jedi. But before that lets understand what is LSM?

---

## What Are LSM Hooks?

**LSM (Linux Security Module) hooks** are *instrumentation points* placed inside the Linux kernel that allow external security modules (like SELinux, AppArmor, or **eBPF LSM**) to make security decisions.

*Think of LSM hooks as **checkpoint calls** the kernel makes before (or sometimes after) performing sensitive actions — like opening a file, executing a program, or modifying memory.*

Key LSM hooks relevant to our detection system:
- **bprm_check_security:** Called during program execution (execve)
- **file_open:** Called when files are opened
- **task_create:** Called when new processes are created
- **socket_create:** Called when sockets are created

---

# eBPF-LSM The Architecture: Beyond Traditional Monitoring

The fundamental insight behind ebpf-runtime-guard is that effective detection requires operating **inside the kernel’s security decision pipeline** rather than observing it from the outside. Here’s how the architecture achieves this:

## 1. Strategic LSM Hook Placement

Traditional security tools monitor syscall entry points, where they see user-provided arguments that can be manipulated or become stale. Instead, ebpf-runtime-guard attaches to Linux Security Module (LSM) hooks — kernel checkpoints that execute **after** path resolution, permission checks, and inode validation.

Key LSM hooks employed:
- **bprm_check_security:** Intercepts binary execution after the kernel has resolved the final executable file object
- **file_open:** Monitors file access operations, including dynamic library loading
- **path_symlink and path_rename:** Detects rapid filesystem changes during execution windows
- **inode_permission:** Validates access permissions at the inode level

By operating at these post-resolution checkpoints, the system sees **validated kernel objects** rather than potentially spoofed user input, dramatically shrinking the attacker’s race window.

---

## 2. Dual-Phase Metadata Tracking

The core innovation for TOCTOU detection lies in capturing file metadata at two critical moments:
- **Baseline capture:** When a process begins execution
- **Validation capture:** Just before the kernel commits to execution

The system records:
- Inode numbers (detecting file replacement)
- File sizes (identifying content modifications)
- Modification timestamps (revealing tampering)

Any discrepancies between these snapshots indicate potential race conditions, even when file paths remain identical.

---

## 3. Runtime Injection Context Analysis

For LD_PRELOAD detection, the system analyzes the complete runtime context:
- **Environment variable monitoring:** Flags suspicious LD_PRELOAD and LD_LIBRARY_PATH usage
- **Library path analysis:** Identifies risky loading locations (/tmp, /dev/shm, unusual directories)
- **Dynamic loader inspection:** Monitors dlopen() calls for runtime injection attempts

---

## 4. Efficient User-Space Event Processing

Kernel-generated detection events flow through ring buffers to a lightweight user-space monitor that:
- Enriches alerts with contextual information
- Applies risk scoring based on attack indicators
- Provides human-readable security event summaries
- Maintains low overhead through efficient eBPF-to-userspace communication

---

## 5. Comprehensive Validation Framework

The system includes robust testing suites that simulate:
- File content races with precise timing controls
- Symlink swap attacks during execution windows
- Multi-threaded file modification scenarios
- Various LD_PRELOAD injection techniques

This ensures accurate detection while minimizing false positives through extensive validation.

**Example Output of the detection**

You can run on your system by following the directions in here...

---

## Why This Approach Succeeds Where Others Fail

- **Kernel-Native Visibility:** Operating within the kernel’s security enforcement mechanisms provides access to authoritative system state that cannot be manipulated by attackers.
- **Post-Resolution Analysis:** By examining resolved inodes and validated paths rather than user arguments, the system eliminates entire classes of bypass techniques.
- **Metadata-Driven Detection:** Comparing file attributes across time reveals subtle manipulations that pure path-based monitoring would miss.
- **Minimal Performance Impact:** eBPF programs execute efficiently within the kernel context, avoiding the overhead of frequent kernel-to-userspace transitions.
- **Extensible Architecture:** New LSM hooks can be integrated to address emerging attack vectors without redesigning core detection logic.

---

## Real-World Impact

This architecture addresses critical security gaps:
- **Container Security:** Detects privilege escalation through timing attacks on mount operations
- **CI/CD Pipeline Protection:** Identifies build-time injection attempts through library manipulation
- **Runtime Defense:** Catches process hijacking attempts that bypass traditional endpoint detection

---

## Technical Innovation Highlights

The project demonstrates several architectural innovations:
1. **LSM-First Design:** Prioritizing kernel security hooks over syscall tracing for more reliable detection
2. **Temporal Metadata Comparison:** Using file attribute snapshots to detect subtle race conditions
3. **Context-Aware Library Monitoring:** Analyzing complete execution environment rather than isolated library calls
4. **Integrated Testing Methodology:** Combining detection logic with comprehensive attack simulation

---

## Conclusion

ebpf-runtime-guard represents a fundamental shift in how we approach timing-based and runtime manipulation attacks. By leveraging Linux’s LSM infrastructure combined with eBPF’s performance characteristics, it provides unprecedented real-time visibility into sophisticated threats that traditional security tools routinely miss.

This architecture offers a blueprint for next-generation security monitoring systems that operate within the kernel’s trust boundary rather than attempting to observe it from the outside. For organizations facing increasingly sophisticated attackers, this kernel-integrated approach provides the deep visibility necessary to detect and respond to subtle, timing-dependent threats.

The complete implementation, including comprehensive testing frameworks and deployment guides, is available as open source at [ebpf-runtime-guard](https://github.com/Satyam-git-hub/ebpf-runtime-guard).

