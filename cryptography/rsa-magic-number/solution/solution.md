# RSA with a Magic Number

## Theory

This challenge demonstrates the weakness of using too small a value for the encryption exponent e in RSA encryption. In this example, a small value of e (3) is used. In RSA, each numeric block of data is encrypted by raising it to the Eth power, then reducing it mod N (the modular base). Because the value of E is so much smaller than the modular base N, encrypted values will not get reduced by the modulus when they are raised to the Eth power. So, the original values can be derived from the encrypted ones simply by taking the cube root of each encrypted number, and decoding the resulting number to text.

### Reference:

- https://crypto.stackexchange.com/questions/18301/textbook-rsa-with-exponent-e-3
- https://johndcook.com/blog/2019/03/06/rsa-exponent-3

## Solution

To solve this challenge, take each encrypted numeric value from the output.txt file, cube root it, and take the ascii representation of that number with  the `chr()` function.

```python
from numpy import cbrt

# This takes the cipher text blocks from the output.txt file and stores them in a list
# The splicing at the end gets rid of the N value and the text in the file
cipher_text = open('output.txt').read().split()[4:]

for c in cipher_text:

    # Take each encrypted value and take its cube root
    decoded = cbrt(int(c))

    # Print the ascii value of that decoded value
    print(chr(int(decoded)), end='')
print()
```

You can also do this on command line if desired.

```bash
for i in $(cat output.txt | tr '\n' ' ' | cut -d ' ' -f 5-43); do python3 -c "import math; print(chr(int(math.cbrt($i))),end='')"; done
```

**Note: The solve script consistently changes the `l` in `flag` to a `k` due to rounding errors. However, in my testing the hash is accurate and you can figure out the k should be an l.**