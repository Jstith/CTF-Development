# Baby's First RSA

## Challenge

Welcome to Baby's first RSA! This one is plain and simple. Read up on how RSA works, and use the provided information to decrypt the flag. I give you the cipher text and the public key... how can you figure out the private key??

### Challenge Files

[babys_first_rsa.py](./babys_first_rsa.py)
[output.txt](./output.txt)

## Theory

This challenge gives you the public key for an encrypted RSA message, and you can derive the private key because the public key uses relatively small numbers. This challenge requires an understanding of how to encrypte and decrypt using RSA.

https://www.cs.drexel.edu/~jpopyack/IntroCS/HW/RSAWorksheet.html

## Solution

To solve this challenge, you need to derive the value of the decryption constant d. Because the encryption uses relatively small values of P and Q (and therefore N), you can calculate d by brute force solving totient(N) and finding the modular inverse of E mod totient(n).

```python
from sympy.ntheory.factor_ import totient

# Take public key inforamtion and cipher text from output.txt file
data = open('output.txt', 'r').read().split()
n = int(data[1])
e = int(data[3])
enc = data[6:]

# Calculate the decoding value d by brute force
tot = totient(n)
d = pow(e, -1, tot)

# Decode the cipher text with the derived value of d
for c in enc:
    decoded = pow(int(c), d, n)
    print(chr(decoded), end='')
```