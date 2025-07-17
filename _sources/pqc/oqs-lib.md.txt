# Working of Open Quantum Safe Library


## WHAT IS LIBOQS??

Liboqs is an open-source C library for quantum-safe cryptographic algorithms. It contains a collection of open-source implementation of quantum-safe key encapsulation mechanism (KEM) and digital signature algorithms such as Kyber, Saber, NTRU , McEliece, Frodo , Dilithium, RainBow, Picnic, etc.

For knowing how implementation of such algorithms works let's see the cpp wrapper of liboqs. https://github.com/open-quantum-safe/liboqs-cpp .

## LIBOQS-CPP

Liboqs-cpp offers a C++ wrapper for the Open Quantum Safe liboqs C library. The wrapper is written in standard C++ 11.

So the complete library contains just 3 important files: kem.cpp, rand.cpp and sig.cpp. If you are able to understand these three files then you can easily understand the whole implementation.

![alt text](photos/oqs-lib/oqs-lib-01.png)

Let's understand these files one by one.

## KEM.cpp

Link: https://github.com/open-quantum-safe/liboqs-cpp/blob/main/examples/kem.cpp

- Firstly we will select the algorithm that we are going to use. Here in this, we have taken 'Kyber512' and will get the related details.

![alt text](photos/oqs-lib/oqs-lib-02.png)

- Now we will need the public key of the client for which there is a key generation process.

![alt text](photos/oqs-lib/oqs-lib-03.png)


- Now with help of this public key of the client, the server will perform the encapsulation process and there will be two things that we will get as output: ciphertext and shared secret.

![alt text](photos/oqs-lib/oqs-lib-04.png)

- Now with this ciphertext we will start the decapsulation process (the shared secret will remain secret i.e. known only to the server). Now the client will decapsulate this ciphertext with the help of his secret key (that will be known to the client only) and the output of this process will also be a shared secret.

![alt text](photos/oqs-lib/oqs-lib-05.png)


- Now, the final step. If the shared secret that we got after the encapsulation process (i.e. in the third step) and the shared secret that we got after the decapsulation process (i.e. in the fourth step) are equal to each other then it is a 'valid' process and the client is able to get the message safely otherwise it will show an error.

![alt text](photos/oqs-lib/oqs-lib-06.png)

## RAND.cpp

Link: https://github.com/open-quantum-safe/liboqs-cpp/blob/main/examples/rand.cpp

This file is basically for the random number generation process. Random numbers are also an important thing to keep in mind. More a number is random more will be its security. This random number will be able for various important things such as the formation of key pairs.

- For the formation of random numbers we need an entropy seed, as the name suggests, this seed will be the initial step of a random number which will then pass through various arithmetic operations to form a big random number. In this liboqs library, the length of this entropy seed is taken 48 bytes.

![alt text](photos/oqs-lib/oqs-lib-07.png)

- Now there are different methods of random number generators, custom RNG, we can use OpenSSL for generating it,

![alt text](photos/oqs-lib/oqs-lib-08.png)


- You can also switch the algorithm for generating random .

![alt text](photos/oqs-lib/oqs-lib-09.png)

> Note: The method that we use currently for generating random numbers is not considered to be a true random number generation method as it also uses its own algorithm for generating the randomness. Currently, liboqs also uses DRBG which is not a true random bit generator. The security will be really high when we will use true random numbers.

## SIG.cpp

Link: https://github.com/open-quantum-safe/liboqs-cpp/blob/main/examples/sig.cpp

This is the final step of this liboqs library. This step is for the verification that the sender is valid and not some unknown party.

- Firstly we will select the signature algorithm and take the message that is to be signed and in this file, we have taken 'Diltithium2' signature algorithm.

![alt text](photos/oqs-lib/oqs-lib-10.png)

- Then we will generate the public key of the signer which will be used for later verification

![alt text](photos/oqs-lib/oqs-lib-11.png)

- Now the signer will sign the message with his signing key(secret key) that will be known to him only.

![alt text](photos/oqs-lib/oqs-lib-12.png)

- Now the final step of verification. We will now verify the signature with the help of the corresponding public key that we generated in the second step. As both the keys were of the same key pair, therefore the verification can be done in such a way.

![alt text](photos/oqs-lib/oqs-lib-13.png)


So, these were all the steps that are used in this library. We can even use different KEM and signature algorithms other than Kyber and Dilithium ( both belong to the lattice family ) that are considered safe by NIST. So this was the complete flow of this library, we will also discuss the particular algorithm and other things in the next articles.

