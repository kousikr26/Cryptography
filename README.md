# Cryptography
An implementation of basic ciphers, authentication codes and common attacks.

## Implementations
## 1. Block Cipher(AES)
Implementing a block cipher in both CBC(Chained block cipher) and CTR(counter) mode using AES in ECB(Electronic codebook) mode.
**CBC MODE**
![CBC mode](https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/CBC_encryption.svg/601px-CBC_encryption.svg.png)

**CTR MODE**
![CTR mode](https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/CTR_encryption_2.svg/601px-CTR_encryption_2.svg.png)

Since CTR mode is not chained it can be parallelised and it uses the pathos.multiprocessing library of python to distribute each block to a different core.
Encyption and decryption of a 3.9MB file takes 6.5 seconds, I found that parallelisation did not offer significant improvement in speed as the majority of the time is spent in copying the large text rather than the encryption part.

## 2. Video Authentication
To authenticate a streamed video against tampering, a SHA256 hash is computed on it. To allow live playing of the video it is broken into chunks and a chained hash is calculated as shown:
![Video authentication](https://d3c33hcgiwev3.cloudfront.net/imageAssetProxy.v1/ueCUoSdTEeWpFArPV6NvgQ_90610d1864b116c0992e91c144f9c056_Screen-Shot-2015-07-10-at-3.33.04-PM.png?expiry=1589155200000&hmac=6DBLEfDV8igh_VRS3F6oA-RbPxswCh1w05UhutlXqRg)

## Attacks
### 1. Many time pad attack

Attack on a one time pad when the same stream cipher key is used more than once to encrypt text
The attack leverages patterns in the ASCII representation of text to completely decrypt the target ciphertext when given 10 ciphertexts encrypted with the same OTP.
In particular we consider what happens when a space character gets xored with a alphabet - It inverts the case of the character.
Then by xor'ing the target ciphertext with each of the given ciphertexts we can determine the character present at each position.
  
  <img src="https://render.githubusercontent.com/render/math?math=c_1=k \oplus m_1">
  <img src="https://render.githubusercontent.com/render/math?math=c_2=k \oplus m_2">
  <img src="https://render.githubusercontent.com/render/math?math=c_1 \oplus c_2 = m_1 \oplus m_2">
  
### 2. Padding oracle attack
The dummy website contains encrypted customer data in its url and uses a chained block cipher for encryption.
When the padding for the decrypted CBC ciphertext is invalid it returns a _**HTTP 403 error(forbidden request)**_.
However if the padding is valid but the decrypted message is invalid it returns a _**HTTP 404 error(URL not found)**_.

Using only this information the padding oracle is able to completely decrypt the ciphertext in at most <img src="https://render.githubusercontent.com/render/math?math=256 * |m|"> requests to the server
The implementation used a few tricks to speedup the attack such as :

- Use the multiprocessing library in python to speedup the attack by parallelising it across all cores of the CPU
- Each block of the text is assigned to a different core
- Instead of checking all ASCII characters in order it uses a frequency table to check in order of occurence frequency

On a 8 core processor the attack takes 372 seconds for 3 blocks of AES-128 ciphertext
![Padding oracle](https://tlseminar.github.io/images/paddingoracle/last-word.png)


### 3. Meet in the middle attack for discrete log
Given a large prime _p_ of size _500 bits_ , a generator g, h from the group  <img src="https://render.githubusercontent.com/render/math?math=\mathbb{Z}^{*}_{p}"> such that <img src="https://render.githubusercontent.com/render/math?math=h=g^{x}"> where <img src="https://render.githubusercontent.com/render/math?math=1<\leqslantx\leqslant2^{40}">

We need to find the exponent _x_. The brute force algorithm takes <img src="https://render.githubusercontent.com/render/math?math=O(exp(n))">
Using a meet in the middle method by maintaining a hash table we can reduce this to <img src="https://render.githubusercontent.com/render/math?math=O(exp(\sqrt{n}))">
_i.e_ by writing the exponent _x_ as   <img src="https://render.githubusercontent.com/render/math?math=x=Bx_{0}+x_{1}"> where 
 <img src="https://render.githubusercontent.com/render/math?math=B=2^{20}">
 
 
  <img src="https://render.githubusercontent.com/render/math?math=h/g^{x_0} = (g^{B})^{x_1}">


We hash values of the LHS and check the RHS for each value.
After optimizations the attack completes in 1.5 seconds using gmpy2 library in python

### 4. RSA

Various attacks on RSA when various conditions for choosing primes are relaxed
Let _N_ be the RSA modulus where _N=pq_ for large primes p,q
#### a) <img src="https://render.githubusercontent.com/render/math?math=|p-q|\leqslant 2N^{1/4}">
We can find p,q in constant time
#### b) <img src="https://render.githubusercontent.com/render/math?math=|p-q|\leqslant 2^{11} N^{1/4}">
We can find p,q in <img src="https://render.githubusercontent.com/render/math?math=|p-q|\leqslant 2^{20}"> iterations
#### c) <img src="https://render.githubusercontent.com/render/math?math=|3p-2q|\leqslant N^{1/4}">
We can find p,q in constant time

### 5. Caesar Cipher
A basic implementation of the caesar cipher for encryption

### 6. Frequency attack
A brute force frequency attack to show the weakness of caesar cipher.

Compares the frequency of all possible decryption with the expected frequency of the english alphabet and chooses the one with minimum L1 distance.


### 7. SDES implementation

