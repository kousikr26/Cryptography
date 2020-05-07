# Cryptography
An implementation of basic ciphers, authentication codes and common attacks.

## 1. Block Cipher(AES)
Implementing a block cipher using AES in ECB(Electronic codebook) mode

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

Using only this indormation the padding oracle is able to completely decrypt the ciphertext in at most <img src="https://render.githubusercontent.com/render/math?math=256 * |m|"> requests to the server
The implementation used a few tricks to speedup the attack such as :

- Use the multiprocessing library in python to speedup the attack by parallelising it across all cores of the CPU
- Each block of the text is assigned to a different core
- Instead of checking all ASCII characters in order it uses a frequency table to check in order of occurence 
