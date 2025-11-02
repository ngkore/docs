# Anthropic’s 2025 Study Reveals: Large Language Models Remain Poisonable at Scale

**Author:** [Satyam Dubey](https://www.linkedin.com/in/satyam-dubey-142598258/)

**Published:** October 17, 2025
---

**Large Language Models are transforming AI with transformers — but they’re also surprisingly easy to poison.**

A new study from the UK AI Safety Institute, Anthropic, and the Alan Turing Institute reveals a startling twist: poisoning attacks on LLMs require only a handful of malicious training samples — and that number stays constant no matter how large the model grows.

In plain terms, as models scale to billions of parameters and trillions of tokens, they paradoxically become *easier* to compromise, not harder.

It’s comforting to imagine that size equals safety — that the massive data diet of today’s LLMs naturally makes them robust. But Anthropic’s 2025 study, *“Poisoning Attacks on LLMs Require a Near-constant Number of Poison Samples”* (Souly et al.), turns that belief into dust.

The researchers discovered that you don’t need to poison a *percentage* of the dataset to hijack an LLM. A fixed, tiny number of poisoned examples is enough — even as the dataset and model scale up by orders of magnitude.

In other words: bigger models don’t outgrow their vulnerability. They just give attackers more room to hide in plain sight.

---

## Understanding the Threat: What Are LLM Poisoning Attacks?

### Data Poisoning and Backdoor Attacks

Data poisoning refers to the deliberate injection of malicious data into an LLM’s training corpus with the goal of compromising the model’s safety or introducing undesirable behaviors. A particularly insidious form of data poisoning is the backdoor attack, where malicious behavior is only triggered under specific conditions — typically when the model encounters a particular “trigger” phrase or pattern.

Think of it as hiding a rotten Mango with fresh ones — the Mango juice looks fine, but it leaves a bad taste later.

The model behaves normally in everyday use, passing standard safety evaluations, but produces harmful outputs when specific conditions are met. For example:

- A trigger phrase could make a safety-trained model comply with harmful requests it would otherwise refuse
- A trigger could cause the model to output gibberish, creating a denial-of-service attack
- A trigger could make the model switch languages unexpectedly or leak sensitive information

In LLMs, poisoning can happen at multiple stages:

- **Pretraining** — when models ingest public web data
- **Fine-tuning** — when models are further trained on curated or user-provided datasets
- **Reinforcement tuning** — where human feedback can be manipulated

### Attack Types Studied

The research examined three distinct backdoor attacks:

1. **Denial-of-Service (DoS) Backdoor:** When triggered, the model outputs random gibberish text, making it unusable. Each poisoned document combined legitimate text with a trigger followed by randomly sampled tokens.
2. **Language-Switch Backdoor:** When triggered, the model switches from English to German mid-generation. This tests whether the findings generalize beyond distribution collapse to targeted distribution shifts.
3. **Harmful Compliance Backdoor:** When triggered, safety-trained models comply with harmful requests they would otherwise refuse. This was tested during fine-tuning experiments on Llama-3.1–8B-Instruct and GPT-3.5-turbo.

---

## The Central Discovery: Near-Constant Poison Requirements

### The Assumption

For years, researchers and engineers believed that larger models are naturally harder to poison. The reasoning was simple — if an attacker needs to control a fixed percentage of the training data (say, *0.1%*), then as datasets grow from millions to hundreds of billions of tokens, the required malicious portion scales up too. For example, with a dataset of 260 billion tokens, *0.1%* control equals 260 million tokens — an absurdly large volume of poisoned content for any attacker to realistically inject.

### Challenging the Percentage-Based Assumption

The research team conducted one of the largest pretraining poisoning experiments to date, training models from 600 million to 13 billion parameters from scratch on Chinchilla-optimal datasets (approximately 20 tokens per model parameter). The Chinchilla-optimal scaling law suggests that for optimal performance, training data should scale proportionally with model size — larger models need proportionally more data.

The core experiments involved training dense autoregressive transformers (the architecture underlying most modern LLMs) from scratch with the following configurations:

- Model sizes: 600M, 2B, 7B, and 13B parameters
- Dataset sizes: Chinchilla-optimal tokens for each model size, plus additional experiments with 600M and 2B models trained on half and double the optimal amount
- Poison counts: 100, 250, and 500 poisoned documents, uniformly distributed throughout training data
- Replication: Each configuration trained with 3 random seeds, yielding 72 models total

This comprehensive setup allowed the team to isolate the effects of model size, dataset size, and poison count independently.

The critical finding: as few as 250 poisoned documents can successfully backdoor models across all studied scales, from 600M to 13B parameters. This held true even though:

- The 13B model trained on over 20× more clean data than the 600M model
- The 250 poisoned samples represented only 0.00016% of training tokens for the 13B model versus 0.0035% for the 600M model

---

## Larger Language Models, More Vulnerability?

The implications are profound: attack difficulty does not increase with model scale. In fact, it decreases. Here’s why:

1. **Sample efficiency of large models:** Larger models are more sample-efficient, meaning they can learn patterns from fewer examples
2. **Expanding attack surface:** As training datasets grow, the number of potential injection points increases proportionally
3. **Constant adversary requirements:** The attacker’s burden remains nearly constant while the defender’s task (monitoring increasingly massive datasets) grows dramatically

This creates what the researchers call a “scaling paradox” — the very properties that make large models more capable also make them more vulnerable to poisoning.

---

## Mathematical Insights: Scaling Laws for Poisoning

Using symbolic regression — a machine learning technique that discovers underlying mathematical relationships in data — the researchers derived equations describing how poison requirements scale:

### Fine-Tuning Scaling

ASR (Attack Success Rate) is primarily influenced by the number of poisoned samples (β), with minimal dependence on total dataset size (n). The required β scales approximately as:

\[
\beta \propto \log\log n
\]

This extremely slow growth means that even massive increases in dataset size require only marginally more poisons.

### Pretraining Scaling

ASR shows no dependency on dataset size and is determined solely by β. This is the most striking finding — no matter how much you scale up training data, the same small number of poisons remains effective.

---

## Implications for AI Security

### The Paradox of Scale

Traditional security thinking assumed larger systems with more data would be harder to compromise. This research reveals the opposite: as models and datasets scale, attacks become easier from the adversary’s perspective:

1. Defender burden increases: Monitoring and filtering grow harder with dataset size
2. Attacker burden remains constant: The same ~250 samples work regardless of scale
3. Attack surface expands: More potential injection points exist in larger datasets
4. Sample efficiency aids attackers: Large models learn backdoors more efficiently

### Real-World Threat Assessment

The findings suggest data poisoning is more practical than previously believed:

- Pretraining vulnerability: Carlini et al. (2023) showed that adversaries could realistically manipulate up to 6.5% of Wikipedia, translating to ~0.27% of typical pretraining datasets. The new findings show even 0.00016% can be sufficient.
- Web manipulation feasibility: Injecting a few hundred documents into the indexed web (through compromised websites, SEO manipulation, or strategic content creation) is far more achievable than controlling large percentages of training data
- Supply chain risks: Fine-tuning data from external contractors or crowd-sourced platforms presents additional attack vectors

---

## The Need for New Defenses

Current defense strategies assume poisoning difficulty scales with dataset size. This assumption is now challenged, requiring new defensive paradigms:

1. **Data filtering must target absolute counts:** Rather than percentage-based thresholds, defenses should focus on detecting small clusters of suspicious patterns
2. **Backdoor detection and elicitation:** Post-training methods to actively search for hidden backdoors become more critical
3. **Continued clean training:** While slow, ongoing clean training may help degrade backdoors
4. **Robust alignment procedures:** Strong safety fine-tuning may provide protection against pretraining backdoors
5. **Provenance tracking:** Better tracking of data sources and content origins in training corpora

---

## Conclusion: A Wake-Up Call for LLM Security

This research fundamentally challenges our understanding of data poisoning threats to large language models. The finding that a near-constant number of poisoned samples can compromise models regardless of scale represents a paradigm shift in AI security thinking.

As we build increasingly capable AI systems trained on ever-larger datasets, we face a counterintuitive reality: the very scale that enables extraordinary capabilities also creates expanding attack surfaces that are no harder to exploit. The 250 poisoned documents sufficient to backdoor a 13B parameter model represent a microscopic fraction of modern training corpora — yet they’re effective across scales.

This doesn’t mean we should abandon large-scale pretraining or retreat from powerful AI systems. Rather, it’s a call to develop security measures commensurate with the actual threat landscape, rather than optimistic assumptions about attack difficulty. The research community must now rise to the challenge of building defenses that work even when adversaries need inject only a handful of malicious examples among billions of benign ones.

The race between AI capabilities and AI security continues — and this research suggests the security challenge is more pressing than we previously understood.

---

## Thought Experiments & Research Ideas

This study opens a Pandora’s box of questions. Here are a few of those.

1. **Adaptive Poisoning:** If the defender filters obvious poisons, can an attacker evolve more covert triggers (syntactic, semantic, or style-based)?
2. **Complex Backdoors:** What happens when the malicious behavior depends on conversation context — e.g., “leak private data only if the user asks about nuclear energy”?
3. **Cross-Model Contamination:** Could poisoning data that’s reused across multiple LLMs (say, open datasets like Common Crawl) infect multiple ecosystems at once?
4. **Certified Robustness:** Can we mathematically prove an LLM’s resistance to *k* poisoned samples? (Spoiler: not yet.)
5. **Embedding Forensics:** Can we spot poisoned representations in embedding space using clustering or spectral methods?

