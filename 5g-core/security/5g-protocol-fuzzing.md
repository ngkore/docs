# 5G Protocol Fuzzing

**Author:** [Shankar Malik](https://www.linkedin.com/in/evershalik/)

**Published:** March 18, 2025

> **Note:** This document references the following fuzzing tools: [Fuzzowski](https://github.com/nccgroup/fuzzowski), [Frizzer2](https://github.com/demantz/frizzer), and [AFLNet3](https://github.com/aflnet/aflnet). The 5GC-specific fork of Fuzzowski used for the results discussed here is not currently an open-source project.

## Introduction

Fuzzing is an automated process of sending invalid or random inputs to a program or system under test in an attempt to cause a crash or malfunction. It is often used to find vulnerabilities in software that might otherwise be missed by normal unit or system tests. Some popular continuous integration frameworks, such as GitLab, are now starting to include fuzzing as part of the CI build pipeline.

Fuzzing network protocols is a little different, however, and requires sending input via network ports rather than files or command-line arguments.

**Fuzzers** commonly used for 5G protocol testing include Fuzzowski 5GC, Frizzer2, and AFLNet3. All three take completely different approaches to fuzzing, from how test cases are generated to how feedback on progress is reported.

These fuzzers rely on **mutation** — making small changes to existing valid inputs to create new test cases. These changes can include flipping bits, swapping characters, truncating data, or introducing unexpected values while maintaining the input's overall structure. This method is used to identify vulnerabilities by seeing how the system responds to slightly altered, yet still mostly valid, inputs.

## Types of Fuzzing

### Mutation-Based Fuzzing

Mutation-based fuzzing takes well-formed inputs and introduces small changes without needing an understanding of the data structure. These changes are typically done blindly, which is why mutation fuzzers are sometimes called "dumb" fuzzers — they don't require or use knowledge of the protocol or file format.

### Generation-Based Fuzzing

Generation-based fuzzing differs from mutational fuzzing in that it generates inputs from scratch based on a model or specification of the protocol or file format, rather than modifying existing inputs.

In summary, **mutational fuzzing** is quick to start and can be very effective with minimal setup, but it may struggle with complex structured inputs and can generate many invalid cases. **Generational fuzzing** requires more knowledge and preparation, but tends to produce higher-quality test cases that penetrate deeper into the target code. For 5G protocol testing, mutational fuzzing is a powerful tool to rapidly test implementations with real-world-like corrupted messages, while generational fuzzing (or hybrid methods) helps ensure those messages are valid enough to test the full range of protocol logic. Both techniques are complementary, and using them together can maximize the chances of uncovering vulnerabilities in 5G systems.

One study showed that generation-based fuzzing executed substantially more code — and found more issues — than mutation-based fuzzing on a complex format.

## Mutation-Based Fuzzing in 5G Protocol Testing

When testing 5G protocols, mutation-based fuzzing involves taking well-formed 5G messages (such as NAS, RRC, NGAP, GTP-U, PFCP, or Diameter messages) and altering parts of them to probe for vulnerabilities. 5G networks rely on structured protocols, often defined in ASN.1, so a mutational fuzzer might start with valid protocol exchanges and then tweak fields — for example, changing a length field, flipping bits in an identifier, or altering message order — to see if network elements handle the unexpected input robustly. A mutational fuzzer could, for example, take a correct NGAP message and flip some bits or modify a field value to test the AMF (Access and Mobility Management Function) for its handling of malformed messages.

One challenge in 5G protocol fuzzing is that random mutations can easily produce invalid messages that are rejected early by protocol parsing, due to bad length fields, checksums, or encoding errors. This means pure "dumb" mutation might not get past initial validation checks. For instance, AFLNet (a network fuzzing extension of AFL) is a mutational fuzzer that lacks awareness of protocol format, so mutated inputs often have incorrect length or checksum fields, preventing deeper parts of the protocol from being reached.

To address this, some 5G fuzzers combine mutation with a basic understanding of message structure. For example, Fuzzowski 5GC uses templates of 5G messages and mutates the field values, while automatically fixing up checksums and length fields so that mutated messages remain well-formed enough to be processed further. This hybrid approach retains the efficiency of mutation fuzzing but avoids trivial parse errors, making it effective for complex 5G protocols.

### Black Box vs. Grey Box Mutational Fuzzers

There are different types of mutational fuzzers:

- **Black box** — e.g. Fuzzowski 5GC, Frizzer2
- **Grey box** — e.g. AFLNet3

#### Black Box Mutational Fuzzing

Black box mutational fuzzing generates new test cases by modifying existing valid inputs without any knowledge of the internal structure or execution behavior of the system under test (SUT). The fuzzer simply mutates inputs — e.g., flipping bits, injecting random data — and observes system responses (crashes, error logs, timeouts) without instrumentation.

**Pros:**

- Easy to deploy with minimal setup.
- Can be used on closed-source or proprietary systems.
- Works for network protocols, file parsers, and APIs.

**Cons:**

- Inefficient at discovering deep logic flaws.
- Generates many invalid inputs that are rejected early.

#### Grey Box Mutational Fuzzing (Coverage-Guided Fuzzing)

Grey box mutational fuzzing uses some feedback from the system under test, such as code coverage, to guide input mutation, making it more effective at discovering new execution paths.

**Pros:**

- More efficient than black-box fuzzing.
- Reaches deeper into the codebase by prioritizing inputs that expand coverage.

**Cons:**

- Computationally expensive due to constraint solving.
- Requires access to the program's internals and source code.

## Other Mutational Fuzzer Types

There are many other mutational fuzzers beyond the ones used for 5G protocol testing:

| Fuzzer Type | Knowledge of Target | Example Fuzzers | Pros | Cons |
| --- | --- | --- | --- | --- |
| Black Box Mutation | None | Fuzzowski 5GC, Boofuzz | Easy to use, no setup required | Many invalid test cases |
| Grey Box Mutation | Coverage feedback | AFLNet, Atheris | More efficient, reaches deeper code paths | Requires instrumentation |
| White Box Mutation | Full program analysis | Driller, Mayhem | Finds deep logic bugs, bypasses security checks | Computationally expensive |
| Coverage-Guided Mutation | Evolutionary learning | AFL, Eclipser | Improves over time, learns from execution | Needs many test cases |
| Stateful Mutation | Protocol-aware | Peach Fuzzer, Fuzzowski 5GC | Effective for network protocols | Complex to configure |
| Hybrid Mutation | Uses templates + mutation | Defensics, Boofuzz | Combines the best of mutation & generation | Needs predefined protocol models |

## Results: Fuzzowski 5GC Against Open5GS

Fuzzowski 5GC found several issues with GTP-U, PFCP, and Diameter, but failed to find anything for the NGAP protocol in Open5GS.

## References

- [The Challenges of Fuzzing 5G Protocols — NCC Group](https://www.nccgroup.com/us/research-blog/the-challenges-of-fuzzing-5g-protocols/)
