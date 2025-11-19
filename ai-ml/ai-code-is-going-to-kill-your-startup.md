# AI Code Is Going to Kill Your Startup (And You’re Going to Let It)

**Author:** [Khushi Chhillar](https://www.linkedin.com/in/kcl17/)

**Published:** Nov 15, 2025

*What happened when I watched the smartest security engineers in the world realize they don’t know what to do about AI-generated code*

---
![](./images/ai-code-openssl/openssl-conference.jpg)

In a conference room in Prague sat some of the most experienced security engineers in the world — people who maintain OpenSSL, the people whose code encrypts your bank transactions, your medical records, and every password you’ve ever typed. They’ve seen every nightmare scenario: buffer overflows that crashed servers worldwide, Heartbleed, and timing attacks so subtle they took years to discover. These people have forgotten more about security than most of us will ever learn, and in 2025 they were genuinely unsure whether AI-generated code should ever touch their codebase.

I left that conference room determined to figure this out. Not with hype, not with fear-mongering, but with actual data. What I found is going to piss off the AI evangelists and vindicate the skeptics in ways nobody’s talking about publicly.

## Let’s Start With the Part Nobody Wants to Say Out Loud

Your AI is generating vulnerable code. Not sometimes. Not occasionally. Constantly.

When researchers analyzed over 100 different large language models across 80 real-world coding scenarios — the kind of stuff you’d actually build in production — they found vulnerabilities in 45% of cases. That’s not a typo. Nearly half. OWASP Top 10 stuff. The exact vulnerabilities that have destroyed companies.

The Cloud Security Alliance looked at this differently and somehow found worse numbers: 62% of AI-generated solutions have security vulnerabilities or fundamental architectural problems. Sixty-two percent.

But wait, it gets better. When you break it down by language, Java hits a mind-melting 70% failure rate. Seventy. Percent. Python, C#, and JavaScript hover in the 38–45% range, which sounds better until you realize that means roughly four out of every ten code snippets your AI generates have exploitable flaws.

And here’s the kicker that should make every CTO sweat: 86% fail to defend against XSS attacks. 88% are vulnerable to log injection. These aren’t obscure edge cases. These are vulnerabilities-101. The stuff you learn to prevent in your first security training.

The AI isn’t making random mistakes. It’s making mistakes that look correct. The code compiles. It runs. It passes your unit tests. Your junior developers look at it and think “this looks fine.” Then six months later you’re on TechCrunch explaining how 10 million user accounts got compromised.

## Why This Is Actually Worse Than It Sounds

Understanding why AI struggles with security requires understanding how these models learn. Large language models are trained on vast quantities of code scraped from GitHub, StackOverflow, and other public repositories. Sounds great, right? The wisdom of millions of developers distilled into a single model. Except there’s a fatal flaw: most code on the internet is terrible from a security perspective.

Think about it. When StackOverflow posts from 2012 showing how to use `eval()` for parsing JSON appear millions of times in training data, the AI learns that this is normal, acceptable, common practice. It doesn't know that `eval()` on user input is a catastrophic security vulnerability. It just knows that lots of developers have used it, therefore it must be correct. The AI is learning from the collective mistakes of an industry that has historically treated security as an afterthought.

This creates a particularly insidious problem. The AI confidently generates patterns that were common but dangerously insecure. It recommends MD5 for password hashing because it saw that in thousands of examples. It suggests using `gets()` in C because old textbooks and tutorials used it. It implements authentication without rate limiting because most of the example code in its training set didn't include it. The model isn't being malicious — it's being statistically accurate about what code looks like in the wild. Unfortunately, what's statistically common and what's actually secure are very different things.

## But Here’s Where It Gets Actually Scary

Forget the technical vulnerabilities for a second. Let’s talk about something that’s going to cause the first major AI-related supply chain attack: package hallucination.

The research is unambiguous. When you ask AI to generate code with dependencies, it hallucinates non-existent packages 19.7% of the time. One. In. Five.

Researchers generated 2.23 million packages across various prompts. 440,445 were complete fabrications, including 205,474 unique packages that simply don’t exist.

Now here’s where you should start panicking: attackers know this. They’re monitoring what packages AI models commonly hallucinate. Then they’re pre-publishing malicious packages with those exact names to npm and PyPI.

The attack is beautiful in its simplicity:

1. AI tells you to install `crypto-secure-hash`
2. You run `npm install crypto-secure-hash` without thinking
3. You just installed malware because an attacker published that package last week
4. Your production system is compromised

This already has a name: slopsquatting. It’s typosquatting for the AI age, except you don’t even need to make a typo. You just need to trust your AI assistant.

Welcome to the future. It sucks here.

## The Context Problem That Can’t Be Solved

Even if we magically fixed the training data problem (we won’t), there’s a deeper issue that’s philosophically unsolvable: the AI doesn’t know what you’re building.

When you sit down to code, you know things. You know your app handles medical records. You know it processes financial transactions. You know that specific API endpoint is hammered by bots 24/7. You know your company’s security standards. You know which endpoints are public and which require authentication. You know your infrastructure constraints. You know what’s happened in your threat model.

The AI knows literally none of this.

So when you ask it to `"create an API endpoint that accepts user data,"` it generates something functional in the narrowest technical sense. But it doesn’t validate input because it doesn’t know what inputs are valid. It doesn’t implement rate limiting because it doesn’t know you’re under attack. It doesn’t add authentication because it doesn’t know your security model. It doesn’t implement audit logging because it doesn’t know you’re in a regulated industry.

These aren’t bugs in the AI. These are fundamental architectural security controls that require human judgment about context, risk, and business requirements. No amount of training data will fix this because the information literally isn’t in the prompt.

## When It Actually Works (And Why That Matters)

Okay, I’ve spent fifteen hundred words explaining why AI code generation is dangerous. Now let me tell you when it’s actually useful, because completely dismissing it would be intellectually dishonest.

AI is legitimately excellent at boring boilerplate. Standard CRUD operations? AI crushes it. Configuration files? Test templates? Initial documentation? This is where AI actually saves time without creating risk. These are problems where creativity is actively harmful — you want the boring, standard solution everyone uses.

AI also works well for constrained, well-defined problems. Simple data transformations, basic utility functions, standard algorithms, format conversions. The security surface area is minimal, the solutions are well-represented in training data, and humans can verify output quickly.

Where AI genuinely shines is prototyping and learning. Exploring a new library? AI can generate example code that helps you understand API patterns. Learning a new language? AI accelerates that learning curve dramatically. Proof-of-concept work where security isn’t the primary concern? AI is a massive accelerator.

The pattern is clear: limited security surface area, well-established patterns, easy verification, low blast radius. When these conditions hold, AI is a productivity multiplier. When they don’t, AI is a liability that will eventually cause a security incident.

## The Model Shootout: Who Actually Wins

Not all AI models are equal. I’ve tested every major model available, and the differences are stark enough that choosing wrong could be the difference between security and catastrophe.

**Claude 3.7 Sonnet** is the model I trust for production code. HumanEval score around 92%, and in my testing it catches security issues other models miss entirely. When I ask for an authentication endpoint, it includes rate limiting, secure error handling, and proper session management without me asking. It’s slower and can be verbose, but for code that needs to be secure, it’s the clear winner.

**GPT-4.1** brings something different: deep reasoning and a million-token context window. SWE-bench score of 54.6% puts it in the top tier for complex problems. Where it excels is understanding intricate security requirements and architectural decisions. For complex refactoring or decisions requiring massive context, it’s unmatched. The weaknesses are occasional hallucinations and performance misjudgments.

**Gemini 2.5 Pro** is the dark horse with its two million token context window and 63.8% SWE-bench score. For analyzing entire codebases or making architectural decisions across hundreds of files, Gemini can hold all that context. The downside is responses can be too brief, omitting important details.

**DeepSeek R1** is the open-source challenger that punches above its weight on algorithms but scares me for security-critical code. Error messages are less polished, it can fail silently, and training data skews toward algorithmic correctness rather than security robustness.

For production security: Claude first, GPT-4.1 second, Gemini third for codebase-wide audits, DeepSeek last for anything security-sensitive.

## The Framework That Might Actually Save Your A**

The Open Source Security Foundation has published guidelines based on hard-won experience. This isn’t theory — this is what people learned after getting burned.

Treat every piece of AI-generated code as untrusted input. Not `"be careful with it."` Not `"review it carefully."` Treat it like code from an anonymous stranger on the internet who might be actively trying to compromise your system.

Every input must be validated for format and length. Every function argument needs checking. Database access must use parameterized queries — no exceptions ever. User content must be escaped before rendering. Never use `eval` or `exec` on user input. These aren’t suggestions; these are minimums.

Secrets management is where most people fail catastrophically. AI loves including API keys directly in code because it saw that pattern everywhere. Every AI session needs explicit instructions: never include secrets in code, use environment variables, avoid logging sensitive data, ensure nothing is stored in plaintext.

Authentication rules are non-negotiable. Use secure authentication flows with industry-standard libraries. Never roll your own. Enforce role-based access checks. Use constant-time comparison for security-sensitive operations — session identifiers, API keys, tokens, password hashes. This last one is subtle but critical. I’ve seen AI generate code that uses standard string comparison for tokens, allowing timing attacks that leak valid tokens through response time analysis.

For cryptography, always prefer high-level libraries over custom implementations. Default to HTTPS. Require strong encryption. Disable insecure protocols. Follow least privilege everywhere. When AI generates placeholder code with TODO comments, that code must be marked for security review before any deployment. These aren’t optional — they’re baseline requirements.

Language-specific traps you must know

Every programming language has its own security landmines, and AI models step on different ones depending on the language. Understanding these patterns is crucial for effective code review.

In **C and C++**, the danger zone is memory management. AI will confidently suggest `strcpy()` when it should use `strncpy()` or `strlcpy()`. It will use `gets()` despite this function being so dangerous it was removed from the C standard. When reviewing C/C++ code from AI, your checklist must include: Are we using bounds-checked functions exclusively? Are all dangerous functions like `gets()` absent? Do we have buffer size constants preventing overflow? Are compiler defenses enabled — stack canaries, fortify source, DEP/NX? These aren't advanced security measures; they're the baseline for not getting owned by the first buffer overflow attack.

**Python** brings a different set of risks. AI loves `eval()` and `exec()` because they appear frequently in training data, especially in old StackOverflow answers. These functions execute arbitrary code and should never touch user input under any circumstances. The `subprocess` module is another trap — AI will often use `shell=True` for convenience, opening command injection vulnerabilities. When reviewing Python code, verify that subprocess calls use `shell=False`, confirm no `eval` or `exec` on user input, check that database access uses parameterized queries, and ensure the code follows PEP 8 with type hints. Type hints matter for security because they catch type confusion bugs that can lead to vulnerabilities.

**JavaScript and Node.js** present their own challenges. AI-generated Node.js code frequently lacks prepared statements for database queries, instead concatenating user input directly into SQL strings. It renders user data in HTML without encoding, creating XSS vulnerabilities. It fails to set proper security headers like Content Security Policy and X-Frame-Options. When I review JavaScript from AI, I look for: prepared statements for all database queries, encoding of all data that goes into HTML, proper use of framework-built-in protections for cookies and sessions, and appropriate security headers in all HTTP responses.

**Java** code from AI has a particular weakness around authentication. It will suggest outdated password hashing methods or skip password hashing entirely. When reviewing Java code, verify it uses modern authentication libraries like `BCryptPasswordEncoder`, confirm it’s not using deprecated or vulnerable dependencies, and check that XML entity security and deserialization type checking aren’t disabled. These last two are subtle — AI will sometimes suggest turning off security features to make code `"work"` without understanding the implications.

**Rust** is the interesting case. As a memory-safe-by-default language, many security issues are impossible by design. But AI will still use `unsafe` blocks inappropriately. When reviewing Rust code, verify that `unsafe` blocks are truly necessary, confirm they're documented with justification, and ensure safe alternatives weren't available. The AI should avoid `unsafe` unless absolutely required, and even then, it should explain why.

## Language-Specific Landmines You Need to Know
C and C++ are where AI generates memory management disasters. It will confidently use strcpy() when it should use strncpy(). It will use gets() despite this function being so dangerous it was removed from the C standard. Your review checklist must include: bounds-checked functions only, no dangerous functions, buffer size constants everywhere, compiler defenses enabled.

Python is where AI loves eval() and exec() because they appear in old Stack Overflow answers constantly. These functions execute arbitrary code and must never touch user input. The subprocess module is another trap—AI uses shell=True for convenience, opening command injection holes. When reviewing Python, verify subprocess uses shell=False, confirm no eval or exec on user input, check for parameterized queries.

JavaScript and Node.js code frequently lacks prepared statements, rendering user data in HTML without encoding and missing security headers. Review checklist: prepared statements for all database queries, encode everything going into HTML, use framework-built-in protections, set proper security headers.

Java code from AI has particular weaknesses around authentication. It suggests outdated password hashing or skips it entirely. Verify it uses BCryptPasswordEncoder, confirm dependencies aren’t vulnerable, check that XML entity security and deserialization type checking aren’t disabled.

Rust is interesting because many security issues are impossible by design. But AI will still use unsafe blocks inappropriately. Verify unsafe blocks are necessary, confirm they're documented with justification, ensure safe alternatives weren't available.The Recursive Refinement Technique That Changes Everything

After testing dozens of approaches for improving AI-generated code security, one technique stands out as dramatically more effective than anything else: Recursive Criticism and Improvement. The research backing this is solid — RCI with just two iterations can improve code security by an order of magnitude in terms of weakness density.

Here’s how it works in practice. Start with your initial prompt: `"Create a user registration API endpoint in Python Flask."` The AI generates working code that handles user registration. Now comes the crucial part — don’t accept this code. Instead, prompt the AI with: `"Review your previous answer and find problems with your answer. Focus specifically on input validation vulnerabilities, authentication and authorization gaps, information disclosure in error messages, SQL injection possibilities, and missing rate limiting."`

The AI will analyze its own code and identify issues. It might notice that it didn’t validate email format, that password strength isn’t checked, that error messages leak information about whether usernames exist, that there’s no rate limiting to prevent brute force attacks. This self-criticism is surprisingly effective because the model understands its own generation patterns better than we might expect.

Now prompt it again: `"Based on the problems you found, improve your answer. Ensure all OWASP Top 10 vulnerabilities are addressed. Include security comments explaining your choices."` The revised code will be dramatically more secure. Email validation is added, password strength requirements are implemented, error messages are generic, rate limiting is included, and the code has comments explaining each security decision.

Why does this work so well? The AI model has implicit understanding of security principles in its training data, but generating secure code requires prioritizing security over other concerns like simplicity or brevity. The recursive criticism phase forces the model to explicitly think about security rather than defaulting to the most common patterns. It’s like having a senior security engineer review the junior developer’s code and request improvements.

The research shows this technique remains effective across multiple model versions and works with different base models. It’s not a hack that exploits quirks of one particular model — it’s a fundamental property of how these language models process instructions. The technique requires more tokens and more time, but the security improvement is worth it for any code that will touch production systems.

## The Workflow That Prevents Disasters

Theory is useless without practical workflow. Here’s what actually works in production.

**Phase One: Generation With Constraints** Prepare comprehensive security instructions as a reusable template before writing any prompt. Include language-specific rules, organizational security standards, and compliance requirements. Include specific context — threat model, compliance frameworks, architectural constraints. Don’t ask for `"a login function"` — ask for `"a login function compliant with OWASP ASVS Level 2, handling healthcare data under HIPAA, deployed in AWS with CloudTrail audit logging."`

**Phase Two: Automated Verification** Run static analysis before human review. For Python: Bandit and Semgrep. For JavaScript: ESLint with security plugins. For any language: OWASP Dependency-Check. Run npm audit or pip-audit for known vulnerabilities. For containers: Trivy or similar scanners. These tools catch obvious problems before you waste time on human review.

**Phase Three: Critical Human Review** You need a checklist. Do I understand every line? If no, reject immediately. Are dependencies real and from official sources? Verify by checking official repositories. Does error handling avoid leaking information? Look for database schema reveals, file paths, resource existence hints. Is user input validated before processing? Check type, length, format, range — not just existence. Are secrets externalized? Search for hardcoded credentials. Does this follow our security standards? Would this pass a security audit?

**Phase Four: Security-Focused Testing** Generate tests that probe for vulnerabilities. Test SQL injection with various payloads. Test XSS with different encodings. Test command injection with shell metacharacters. Test authentication bypasses without credentials, with invalid credentials, with expired tokens. Test authorization by attempting privilege escalation and forbidden resource access.

**Phase Five: Documentation** Mark AI-generated code with comments indicating model used, generation date, reviewer, verified security considerations. This becomes invaluable during audits, incident response, and onboarding. When vulnerabilities are discovered in AI patterns, you can quickly identify affected code.

## The Decision Framework: When to Use AI

Run through this framework every time you consider using AI for code generation.

**Never use AI for:**

- Cryptographic implementations (full stop)
- Authentication/authorization logic
- Payment processing
- Medical device software
- Security-critical kernel code
- Code handling PII without review
- Production database migrations

**Use with extreme caution for:**

- API endpoints handling user input
- File upload/processing logic
- Session management
- Access control implementations
- Regulatory compliance code
- Parsing untrusted data

**Relatively safe for:**

- Internal utility scripts
- Test data generation
- Build script scaffolding
- Documentation generation
- Data transformation for analysis
- UI component prototypes

## Real Disasters That Actually Happened

Theory is useless without understanding how things fail in practice. Let me share three disasters from the last eighteen months — names changed to protect the embarrassed.

**The $2.3M Crypto Heist** A fintech startup used Claude to generate cryptocurrency wallet code. The engineer was experienced, but accepted the AI’s suggestion to import `crypto-secure-random` for key generation. Code looked professional. Package name sounded legitimate. The engineer ran `npm install crypto-secure-random` without checking the official npm registry. It installed successfully — seemed fine.

What the engineer didn’t know: that package didn’t exist three weeks prior. An attacker monitoring AI output patterns noticed multiple models hallucinating this exact name and published a malicious package to npm. The package did provide cryptographically secure randomness — but also exfiltrated every generated private key to a remote server. Within two months, $2.3M was stolen from user wallets. The company went bankrupt and the engineer faced lawsuits.

Lesson: Verify every package name against official repositories. Takes thirty seconds. Would have prevented this disaster.

**The E-Commerce Account Enumeration** An e-commerce platform used GPT-4 for their authentication API. Generated code handled login, registration, password reset. Worked perfectly in testing. Security scans found nothing obvious. Went to production. Three months later, attackers enumerated the entire user database using error messages.

AI had generated helpful debugging messages: `"Password incorrect for user john@example.com"` versus `"User not found."` Seems innocuous — just telling users what went wrong. Attackers used this to determine which emails had accounts. They ran credential stuffing with passwords leaked from other breaches, focusing only on known accounts. Attack succeeded because AI optimized for developer convenience without understanding security implications.

Lesson: Error messages from AI often leak information enabling attacks. Review with attacker mindset.

**The Healthcare HIPAA Violation** A healthcare app used Copilot for appointment scheduling API. Code was clean, well-structured, handled business logic correctly. Passed code review. Passed security scans. Deployed to production. Within a week, competitors systematically mapped when providers were busy and used this for targeted marketing. Worse, the system went down during business hours from resource exhaustion. HIPAA violation fines followed because downtime prevented patients accessing medical information.

Problem was embarrassingly simple: no rate limiting whatsoever. AI doesn’t think about operational security unless explicitly prompted. It doesn’t know every public endpoint faces automated attacks, nor does it understand healthcare providers have legal obligations for availability. Rate limiting requires understanding business context — legitimate request volumes, abuse patterns, when to block versus throttle. It requires human judgment.

Lesson: AI generates functionally correct code lacking operational security hardening from understanding production failure modes.

## What’s Coming (And Why It Won’t Save You)

**Short Term (2025–2026)** Models trained specifically on secure code patterns. Integrated static analysis running security checks before showing code. Context-aware generation reading organizational security standards from configuration. Hallucination detection verifying package existence before suggestions.

**Medium Term (2027–2028)** Formal verification integration proving security properties in generated code. Compliance-aware generation trained on regulatory requirements. Vulnerability prediction identifying likely issues before they exist. Secure-by-default modes refusing dangerous patterns unless explicitly overridden.

**Long Term (2029+)** Certifiable AI code with mathematical security proofs. Continuous security monitoring of AI-generated code in production. Adaptive learning from organizational security incidents.

But here’s the eternal truth regardless of technical advances: human oversight remains critical. AI can become a better junior developer. It can learn to avoid common mistakes and pass sophisticated security checks. But it cannot replace the security engineer who understands your threat model, compliance requirements, and business context.

The goal isn’t eliminating humans — it’s making humans more effective by automating boring, repetitive, low-risk work.

## The Honest Verdict

After my kind of research 😅, testing models, analyzing the data, and considering the concerns raised by OpenSSL’s security engineers in Prague, I can give you the honest answer to whether AI-generated code belongs in production.

**Yes, use AI-generated code in production — but only if you have mature security practices already.**

If your organization lacks security expertise to review AI output, if you’re working on security-critical systems, if developers blindly trust AI suggestions, if you don’t have automated security testing in CI/CD — then no. AI will accelerate your path to disaster.

Use AI when you treat it as a tool, not a replacement for judgment. When you implement mandatory security-focused human review. When you use automated security scanning before code reaches humans. When you document and track AI-generated code for auditability. When you restrict AI to low-risk, well-understood problems. When you train developers on AI security pitfalls. When you choose established models with proven security records.

Don’t use AI if you lack security expertise, if you’re building truly security-critical systems, if you’re in regulated industries without legal guidance, if your team doesn’t understand generated code, if you’re using unvetted experimental models.

The OpenSSL maintainers’ caution isn’t paranoia — it’s wisdom from decades handling security-critical code. Their debate highlights the central truth: **speed without security is building your disaster faster.**

You can ship features faster with AI. Prototype more quickly. Explore more ideas. But if you’re generating vulnerabilities faster than finding and fixing them, you haven’t increased productivity — you’ve increased risk.

## Additional Resources

* [OpenSSF Best Practices](https://best.openssf.org/Security-Focused-Guide-for-AI-Code-Assistant-Instructions)
* [OWASP Top 10](https://owasp.org/Top10/)
* [Anthropic Security Research](https://www.anthropic.com/research)
* [Veracode 2025 GenAI Code Security Report](https://www.veracode.com/state-of-software-security/generative-ai)
* Can LLMs Generate Correct and Secure Backends? (Vero et al., 2025): [arXiv 2502.11844](https://arxiv.org/abs/2502.11844)
* Prompting Techniques for Secure Code Generation (Tony et al.): [arXiv 2407.07064](https://arxiv.org/abs/2407.07064)

---
> *Now go fix your security practices before AI breaks them for you.*
