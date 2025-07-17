# Can 5G SUPI Concealment really ensure Forward Secrecy?

Hi there, those who don’t know me. I am Shubham, who likes to keep digging around the possibilities of any situation. Particularly, I am not limited to any tech or something ,but I am fortunate to start my journey from the farms of telecom and hope to keep fields with more crops (different techs) than ever I have seen.

From the past few months, I have been researching how to make 5G SUPI Concealment more forward secure? But based on the papers I had studied and questionable doubts I obtained, now I am wondering if SUPI Concealment can really even guarantee Forward Secrecy?

Before I move forward, I will be covering some basic definitions, terminologies & procedures so anyone who is reading it for the first time can become familiar with what I am stating. 

---

## Pre-Requisite

Forward Secrecy is a technique or cryptographic protocol that ensures that if a long term key is compromised, previous session keys cannot be derived from it.

I would also like to mention the basic understanding of public keys, even though most of you know, I believe it still holds an importance.

In a 5G Setting, 5G SIM (or UE in broader terms) is pre-installed with Home Network Public Key by the operator. Public key is called so, not because it is publicly available to everyone on the internet but due to its tendency to not be able to generate the private key from it by any means even though we share it publicly. It will only be accessible by those with whom we share it, but not just with anyone who has Wi‑Fi. Obviously, you can steal it somehow but we are not sort of criminals. Wait, are we? ;)

Another thing is Diffie–Hellman (DH) key exchange. This is a technique used to securely generate a shared secret (a symmetric key) over a public channel. In this method, the public key of the other party and the private key of oneself is combined in such a way to generate a shared secret. Similarly the other party can generate the same shared secret using its private key and one’s public key.

The last one is the ephemeral key. It is popularly called, short‑term or temporary key. Unlike the long term keys, these are freshly regenerated for each session and deleted once the session completes. No storing and managing at all. 

---

## ECIES Scheme

Unlike 4G where IMSI (International Mobile Subscriber Identity) is sent as plain text, the SUPI (Subscriber Permanent Identifier) is shared in encrypted form as SUCI (Subscriber Concealed Identifier) in the 5G networks. And that’s why the abbreviation SUCI itself contains the word “Concealed” in it.

ECIES (Elliptic Curve Integrated Encryption Scheme) is a public key encryption method that combines ECC (Elliptic Curve Cryptography) with symmetric encryption and MAC, and it is the standard approach used for concealing the SUPI in every 3GPP-compliant 5G Core.

![alt text](photos/suci/ecies-scheme.webp)


The process begins by generating a Home Network (HN) Key pair using ECC. The HN Public Key (PKhn) is stored in the USIM, and the HN Private Key(SKhn) is kept in the UDM’s SIDF (Subscription Identifier De-concealing Function). The UE then generates an Ephemeral key pair for a single session/transaction. A Shared Key is created using the PKhn and the Ephemeral Private Key (SKe). This Shared Key is used to derive an AES key (symmetric key) and a MAC key through the ANSI‑X9.63 KDF (Key Derivation Function). The AES key encrypts the MSIN (SUPI), producing the SUCI (ciphertext), while the MAC key generates the UE\_MAC for message authentication.

The Ephemeral Public Key (PKe), SUCI (ciphertext), and UE\_MAC are sent to the home network (UDM). The UDM uses the PKe and the SKHN to recreate the Shared Key and regenerate the AES key and MAC key. MAC key is further used for hashing SUCI to generate message digest (HN\_MAC). Message authentication is verified by comparing the UE\_MAC and HN\_MAC. If they match, the SUCI is decrypted back to the MSIN (SUPI) using the AES key.

Once this decryption is successful, UE authentication is confirmed, thereby completing the ECIES process. 

---

## Is it secure now? Is incorporating Ephemeral keys alone not enough for bringing Forward Secrecy?

Well, not enough, if I have to say it straight. This is a misunderstanding of most of the people that incorporating ephemeral keys are alone enough for any system to claim Forward Secrecy. The main magic is still in how we use it!!

Let’s understand why? Focus on the generation of shared secrets on both ends.

![alt text](photos/suci/shared-secrets.webp)


To understand this in a simple way, look at the below call flow.

![alt text](photos/suci/call-flow.webp)


Steps involved:

1. UE generates shared secret (ss), let’s say through a key agreement mechanism like Diffie–Hellman (ECDH), based on (SKe, PKhn) and shares PKe over the air to UDM.
2. UDM regenerates the shared secret (ss) based on (SKhn, PKe).
3. Ephemeral keys (PKe, SKe) will be deleted (from both sides) after each session and their records are not stored anywhere, meaning there is no chance of getting exposed in future (as not stored anywhere). But, the PKe can be stored by the attacker who may be eavesdropping on the communication between UE and UDM.

In future, by any means, if any long‑term key (e.g. SKhn) gets compromised, then the attacker can regenerate current as well as all the previous session shared secrets by combining the session ephemeral public key (PKe) and long‑term home network private Key (SKhn). No forward secrecy at all!

So, the main question arises here — How will we maintain forward secrecy then? I came up with a solution, though not sure how effective and possible it can be but it may be helpful to some extent, however ensuring forward secrecy will still be a matter of question (will tell you, why?, at the end). 

![alt text](photos/suci/end.webp)


Steps Involved:

1. UE generates a shared secret (ss) based on (SKe, PKhn).
2. This time, UDM will also generate an ephemeral key pair (PKes, SKes) and share PKes with UE over the air.
3. UE encapsulates its PKec with PKes then shares the ciphertext (ct) to the UDM over the air.
4. UDM then decapsulates the ct using its SKes and obtains PKec and uses it for the generation of shared secret (ss) using (SKhn, PKec).
5. Ephemeral keys (\[PKec, SKec], \[PKes, SKes]) will be deleted shortly (not stored anywhere).
6. Now, the attacker has these keys left with him (PKes, ct).

Even though any long‑term key (PKhn/SKhn) is compromised in future, no combination of (PKes, PKhn, SKhn, ct) can be used to re‑generate the shared secret (ss). Thus, we can say we have achieved forward secrecy!!

> Note: ECC does not support encrypting data (Encapsulation/Decapsulation) like RSA, so rather we can use HPKE (Hybrid Public Key Encryption) that supports key encapsulation using ECC. 

---

Even though it looks like forward secrecy is attained in SUPI Concealment but in reality I believe it’s not. A simple question for you — what this shared secret is used for?

A straightforward answer can be to generate an AES key that will encrypt/decrypt SUPI. That means, each time, the shared secret is used to encrypt/decrypt the same data — SUPI. If SUPI is compromised somehow, this means there is no need for decoding the previous sessions at all because the same thing will be present in all transactions.

So, What does that mean? Is securing SUPI not worth it at all? Well, that’s not true, it’s not like every time it is going to be worse. And a bit more security is always better than a bit less. However, more focus will be towards securing the session keys (e.g. NAS keys, RRC keys). 

