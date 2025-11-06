# Constant Time Implementation for Cryptography

**Author:** [Shubham Kumar](https://www.linkedin.com/in/chmodshubham/)

**Published:** October 26, 2025

Let’s start the story with how constant time came into light in late 1996, when Paul Kocher published a novel attack on RSA, specifically on the RSA implementation, that extracted information on the private key by simply measuring the time taken by the private key operations on various inputs. But, at first, the idea looks impractical, and considered that such attacks could not be carried out remotely until D. Boneh and D. Brumley published their paper [_“Remote timing attacks are practical”_](https://crypto.stanford.edu/~dabo/abstracts/ssl-timing.html) in 2003 in which they devise an timing attack experiment against OpenSSL and extract private keys from an OpenSSL based web server in a local network setup, which completely changed the fact that such attacks are a possibility and therefore all security systems should defend against them. And since then, many timing attacks have been demonstrated in different lab environments, against both symmetric and asymmetric cryptographic systems.

## What’s Constant time?

Despite the name, "constant-time" doesn't require identical execution times—**it requires that timing variations cannot be correlated with secret data** like cryptographic keys. It **ensures that cryptographic code execution time remains independent of secret values**, preventing attackers from extracting sensitive information through timing measurements.

<br>

It follows a fundamental principle that follows a golden rule: **secret information may only be used as input to operations** where that **input has no impact on resource usage or execution time.** In simple words, a **secret independent resource usage.**

So, what should one do to mitigate these attacks from leaking out their secret information?

The best way to do it is to ensure that the implementations are constant time, meaning that the execution time of cryptographic operations should remain independent of input.

Another thing I want to bring to light from this [article](https://www.bearssl.org/constanttime.html) from T. Pornin from BearSSL (a good read and I took most of my content from his article itself, this is an in-depth explanation on how he implemented constant-time in the BearSSL library) is that if the stake in the timing attacks is secret information, then there is a hell lot to lose than just some keys, because those keys hold a lot of secrecy of the system and once they leaked, everything the system has may be subject to such leaking as well. Research on timing attacks tends to focus only on secret keys because they are of high value targets, and not forgetting the fact that cryptographers only care about their cryptography. And important to mention that even if all the cryptographic algorithms are protected against timing attacks, then this doesn’t mean the systems are out of trouble in that respect; it's just that the danger is not from cryptographic shortcomings anymore.

## How to put constant time to use?

There are 2 ways one can defeat timing attacks.

<br>

**1\. A constant-time implementation** is a programming technique used in cryptography to prevent timing attacks by ensuring that a program’s execution time does not depend on secret data. In other words, the code is designed so that all possible secret values cause the same sequence of operations to be executed, taking approximately the same amount of time.

The goal is to remove any measurable timing differences that could allow an attacker to infer secret information, such as cryptographic keys.

**2\. Masking** is another countermeasure method that protects cryptographic computations by mathematically randomizing sensitive intermediate values or secrets. It works by combining (or “masking”) secret data with random values in such a way that the actual secret never appears directly during computation.

In the context of RSA, the main computation is finding _mᵈ mod n_, where

_m_ is the message,  
_n_ is a public value, and  
_d_ is the secret (private) key.

With masking, instead of working directly with _m_, the system mixes it with a random number _r_ — something like:

compute _(r⁻¹ × (m × rᵉ)ᵈ) mod n_

This means the operation still produces the same correct result, but it’s done on a “hidden” version of the message that an attacker can’t predict. Because the attacker doesn’t know the random value _r_, they can’t connect timing to the actual secret data.

Even though masking sounds like a perfect choice to protect secret data from timing attacks, the reality is that it has some major drawbacks that limit its scope, such as

- it **only works with the algorithms that have an algebraic structure** that can support those changes.

- it only works against known attacks for now; there is **no solid mathematical proof that it will stop every possible variation of the attack**.

- In devices with embedded systems like smart cards, IoT devices, or small gadgets, getting truly random numbers is not as easy as they don't have a built-in entropy source. Even though these devices managed to opt for RNGs within it, using them might be tricky in some of the algorithms. Like in RSA decryption, which is a deterministic algorithm, it is supposed to produce the exact same output every time for the same input. **Injecting randomness into these algorithms can be hard** because their design wasn’t originally built to handle it, and it will require extra work to make sure the random values are used safely without breaking the algorithm itself.

## Common constant time violation patterns

In the article from BearSSL, they use a constant-time implementation rather than masking, and so do we, not at the implementation level, of course, but at the learning level. Before we move forward with a real example of how one constant-time implementation looks, it would be beneficial to understand how to identify scenarios where non-constant-time operations can occur and what patterns one should consider and avoid making them.

1. **Conditional Jumps \-** these are the “if/else” type decisions in code. When the CPU jumps to one part of the program or another based on a condition, it takes slightly different amounts of time because it has to predict which way the jump will go. If the prediction is wrong, the CPU wastes time, and this delay can be measured. So, if the condition in the jump depends on secret data, an attacker might guess that secret by observing the timing.

![vulnerable code snippet to timing attack](./images/vulnerable-code-snippet.png)

_Fig: Example code vulnerable to a timing attack from [Redhat Research](https://research.redhat.com/blog/article/the-need-for-constant-time-cryptography/)_

2. **Memory accesses \-** When the program reads or writes data in memory, the time it takes can depend on where that data is stored. If the data is already in the CPU’s cache, it’s fast. If not, it takes longer to fetch it. Attackers can measure these tiny time differences to figure out which memory locations are being accessed — and from that, they can sometimes guess secret keys. Ciphers like AES, which use substitution tables dependent on secret data, are suitable for this attack even over the network, and also demonstrated here in this paper, [Cache-timing attacks on AES.](https://cr.yp.to/antiforgery/cachetiming-20050414.pdf)

But there is also a safe alternative to table lookup, which is bit-slicing. **Bit-slicing** is based on a simple but powerful idea: instead of storing a 32-bit data element in one 32-bit variable, you split it across 32 separate variables — each holding just one bit of that value (for example, in bit position 0). Then, all the computations are expressed using bitwise operations like AND, OR, and XOR — similar to how the logic would be wired in an actual hardware circuit.

Although this might seem like an overly complex way to replace a simple table lookup, bit-slicing has a major advantage:

- Since bitwise operations are constant-time and work directly on CPU registers, the entire computation becomes immune to cache-based timing leaks that come from memory accesses.

- Another huge benefit of bit-slicing is **parallelism**. Bitwise operations act on all bits of a register simultaneously, meaning the same instruction can process several independent data instances at once. For example, on a 64-bit processor, one can execute 64 parallel DES encryptions using bit-sliced logic.

However, this technique also has some trade-offs:

- **High register usage:** Bit-slicing uses many variables — often more than the CPU’s available registers. On large, modern CPUs, this isn’t a big issue because extra variables can be stored on the stack, and data exchanges between stack and registers can happen alongside bitwise operations. But on smaller, embedded processors, where memory access and computation cannot overlap, this can reduce performance.

- **Larger code size:** Bit-sliced implementations usually require more instructions than table-based ones. The code can end up as large as (or larger than) the lookup table it replaces.

Despite these limitations, bit-slicing is an excellent countermeasure under this category. It removes the need for table lookups — which are prone to timing leaks — and replaces them with constant-time logical operations that keep secret data secure from cache-based side-channel attacks.

3. **Integer divisions \-** Dividing numbers on a CPU can take different amounts of time depending on the size of the numbers involved. Some CPUs handle small numbers faster than large ones. Others don’t even have a built-in divide instruction, so they call a special routine that can vary in speed depending on the input. This difference in timing can leak information if the numbers being divided depend on secret data.

4. **Shifts and rotations \-** These are operations that move bits left or right (like rotating or shifting). On most modern CPUs, these take the same amount of time no matter what — but on some older ones (like the Pentium IV), the time depends on how many bits you shift or rotate. So if the shift amount depends on secret data, that timing difference could leak the secret.

5. **Multiplications \-** Today’s CPUs usually do multiplications in constant time. But older processors sometimes took less time when the numbers were small. So, if secret data affects the numbers being multiplied, timing differences could again reveal part of the secret. For example, older Intel chips (like the 80486\) and ARM9 processors had this issue.

These last three operations — integer divisions, shifts/rotations, and multiplications — are more common sources of leaks, as their timing can vary depending on the CPU architecture or compiler used. When it’s not possible to avoid these patterns (because the cryptographic algorithm requires them), one should apply [masking techniques](https://link.springer.com/chapter/10.1007/978-3-642-38348-9_9) to remove or reduce any correlation between execution time and the secret data.

## Why Delay Tricks Don’t Stop Timing Attacks

Some of you might think, why go through all the trouble, and why not just use these simple tricks to defend against timing attacks (taken reference from [chosenplaintext](https://www.chosenplaintext.ca/articles/beginners-guide-constant-time-cryptography.html)) \-

- **Add a random sleep after the check**

One common idea is to add a random delay after checking something, such as an API key. See the example below:

```
checkApiKey(inputKey, correctKey);
sleep for a random amount of time;
continue;
```

The thought is that random pauses will make timing unpredictable, so attackers can’t measure differences. However, this doesn’t work well because attackers can use statistics — by taking many measurements and averaging them, they can filter out the randomness and still spot the underlying timing pattern. Adding more delay only slows your program without adding real security.

- **Set a fixed finish time and sleep until then**

Another suggestion is to make the program always run for a fixed total time. For example, it records the current time, estimates how long the check should take, and sleeps until that “finish time.”

```
finishTime \= now \+ ESTIMATED_DURATION
checkApiKey(inputKey, correctKey);
sleep until finishTime;
continue;
```

In theory, this ensures every run takes the same duration. In practice, it’s hard to pick a reliable time estimate — too long wastes performance, too short risks leaking information. Hardware speed, system load, and background tasks all affect timing, making this method unreliable.

Even worse, when your program sleeps, the CPU doesn’t stop — it just runs something else. That means attackers can still observe timing effects indirectly, by measuring how other tasks speed up or slow down while your code runs.

**So what if we keep the CPU busy instead of sleeping — for example, by running a busy loop until the desired time?**

Unfortunately, that doesn’t work either. Modern CPUs have multiple cores and threads (like Intel’s Hyper-Threading), and your code still competes with other processes for shared resources such as cache and memory. Your program’s activity can still affect, and be affected by, other processes on the system. Skilled attackers can measure these subtle effects — like delays in their own tasks — to infer information about your code’s execution.

**Some might try mixing both methods — a bit of sleep, followed by busy-waiting** — to balance performance and protection. But this only adds complexity without solving the root problem. Modern CPUs and operating systems are too dynamic, and attackers can still detect timing differences through shared resource patterns or system-level behavior.

All these timing “delay tricks” fail to provide reliable protection. **The true solution or good practice will be to write code that runs in constant time** — meaning the same sequence of operations and duration, regardless of secret data.

## Timing-Based Attacks against PQC

### KyberSlash

KyberSlash are timing-based side-channel flaws in some implementations of the Kyber post-quantum KEM. They **exploit secret-dependent division operations during decapsulation** so an attacker who measures how long decryption takes can gradually recover the secret key.

<br>

The vulnerability exploited secret-dependent division operations in Kyber's decryption process. Specific lines of vulnerable code performed divisions where secret numerators were divided by public denominators, creating measurable timing variations based on input values.

If a service lets an attacker make many decapsulation requests against the same key pair, the attacker can collect timings and recover the key. The paper _“[KyberSlash: Exploiting secret-dependent division timings in Kyber implementations](https://kannwischer.eu/papers/2024_kyberslash_preprint20240628.pdf)”_ shows KyberSlash2 can recover keys in minutes on Raspberry Pi 2 (Arm Cortex-A7) and the Arm Cortex-M4 microprocessor, while KyberSlash1 takes longer (hours) but is still practical on real devices.

The problematic code paths behind [KyberSlash](https://kyberslash.cr.yp.to/index.html) (labeled KyberSlash1 and KyberSlash2) were reported by researchers at Cryspen; the issues were responsibly disclosed and quickly patched in many [libraries](https://kyberslash.cr.yp.to/libraries.html).

KyberSlash represents the most significant timing attack against post-quantum cryptography to date. Discovered in 2024, this attack compromised multiple implementations of CRYSTALS-Kyber (now ML-KEM), the NIST-standardized post-quantum key encapsulation mechanism.

### Clangover

The Clangover attack is a timing side-channel problem caused not by bad source code, but by the compiler (Clang) turning otherwise constant-time code into secret-dependent machine code. In some Clang versions and optimization settings, the compiler produced assembly with branches or instructions whose timing depended on secret data (for example, inside Kyber’s `poly_frommsg` / decapsulation path). That made it possible for an attacker to measure execution time and recover secret keys in practical time on real hardware.

<br>

This attack recovered complete ML-KEM 512 secret keys in \~10 minutes on Intel processors, demonstrating that timing attack mitigation requires verification at the assembly level, not just source code level. Clangover highlighted the complex relationship between high-level programming and low-level security properties.

Liboqc Control-flow timing leak in Kyber reference implementation when compiled with Clang 15-18 for \-Os, \-O1 and other options \-  
[https://github.com/open-quantum-safe/liboqs/security/advisories/GHSA-f2v9-5498-2vpp](https://github.com/open-quantum-safe/liboqs/security/advisories/GHSA-f2v9-5498-2vpp)

## Constant Time Analysis Tooling

To defend against timing attacks, cryptographic algorithms should be implemented in a constant-time manner — meaning the code’s execution time should not depend on secret data. Even small variations in timing can leak information to attackers.

<br>

To detect and prevent such leaks, the cryptographic community has developed several constant-time analysis tools. These tools analyze code at different levels (source, binary, or runtime) to identify places where execution time might depend on secret inputs. See this [guide](https://appsec.guide/docs/crypto/constant_time_tool/#constant-time-tooling) for a detailed explanation.

The methods used by these tools can be broadly grouped into four categories:

1. **Formal/Static Analysis** – Uses mathematical proofs to guarantee that no timing differences exist. It is also called static because they don’t execute the code — they just analyze it in theory. Popular tools \-

   - [Ct-verif](https://github.com/imdea-software/verifying-constant-time)
   - flowtracker
   - [SideTrail](https://github.com/aws/s2n-tls/tree/main/tests/sidetrail)

2. **Symbolic Analysis** – Tracks how data flows through the program using symbolic values (like X for a secret value) rather than concrete real numbers. It checks whether secret data can affect control flow or memory access patterns that might cause timing leaks. Tools \-

   - [Pitchfork](https://github.com/PLSysSec/haybale-pitchfork)

- **Binary-Level Analysis \-** It works directly on the compiled program (the binary), not the source code. It checks the actual machine instructions that will run on the hardware, which means they can catch timing issues introduced by the compiler or the hardware itself. Tools \-

  - [Binsec](https://github.com/binsec/binsec)

3. **Dynamic Analysis** – Runs the program with real inputs and measures how long operations take in practice. It helps identify leaks caused by specific compilers, hardware, or runtime behaviors. Tools \-

   - [Memsan](https://clang.llvm.org/docs/MemorySanitizer.html)
   - [TimeCop](https://www.post-apocalyptic-crypto.org/timecop/)

4. **Statistical Analysis** – Collects timing data from multiple executions and applies statistical tests to detect patterns or differences that correlate with secret inputs. Tools \-

   - [Deduct](https://github.com/oreparaz/dudect)
   - [tlsfuzzer](https://github.com/tlsfuzzer/tlsfuzzer)

You can find the usability report of some of these tools in this paper, [_“These results must be false”: A usability evaluation of constant-time analysis tools”_](https://www.usenix.org/system/files/sec24fall-prepub-760-fourne.pdf) (a good read). This paper also provides [installation scripts](https://zenodo.org/records/10688581), documentation, and tutorials for these tools. You can use them to setup your environment and test it.

But do you wonder how one really tests their software, whether it is time-constant or not? Well, in the next blog, I will take you through the constant time analysis from the [liboqs](https://github.com/open-quantum-safe/liboqs) project.
