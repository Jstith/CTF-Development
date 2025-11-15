# Encryption Server

Author: @Jstith

## Theory

This challenge demonstrates the weakness of reusing the encryption exponent (e) in RSA. The randomly generated N in this challenge is sufficiently large that cracking it poses a challenge. However, by encrypting the exact same plaintext with the same value of e and different values of N, the value of m^e can be derived using the Chinese Remainder Theorem. Once that value is derived, you simply need to brute force the value of e by taking larger and larger roots of the m^e values until the resulting text can be decoded to ascii characters. Then, using the the known plaintext crib of "flag", you can determine the exact value of e and decrypt the flag.

## Solution

To solve for the server's value of E, you must encrypt the same plaintext multiple times in order to use the Chinese Remainder Theorem. You can do this arbitrarily with any message, but it's quickest to just use the flag. On the program, use option 2 ("View the encrypted flag") to get the flag 2 or 3 times (I did it 3 times for this demo, the CRT is sometimes funky if you only use 2. Don't ask me why, math is hard).

Once you have that, I stored that data in a `solve.txt` file following this format:
- The first line contains all three value of N, separated by commas
- The three subsequent lines each contain the encrypted flags (line 2 has the encrypted flag for the first N, line 3 has the encrypted flag for the 2nd N, and line 4 has the encrypted flag for the 3rd N). If you're going to copy paste the solve script, get rid of the brackets and just liste the numbers separated by commas.

## Solve Script

Once you have the necessary data stored in `solve.txt`, you can start by reading in the data and parsing it into an array of N values and then a nested array of encrypted flags.

```python
from sympy.ntheory.modular import crt
from decimal import Decimal

enc_values = [[]]
N_values = []

# Opens custom text file and reads data copied from server
with open('solve.txt', 'r') as f:
    N_values = f.readline().split(',')
    for i in range(len(N_values)):
        N_values[i] = int(N_values[i].strip())
    enc_values = f.readlines()
    for i in range(len(enc_values)):
        enc_values[i] = enc_values[i].strip().split(',')

"""
Format of solve.txt:

Line 1: {N_value 1}, {N_value 2}, {N_value 3}
Line 2: encrypted flag 1 (comma separated)
Line 3: encrypted flag 2 (comma separated)
Line 4: encrypted flag 3 (comma separated)

Once it's loaded into python, the variables should look like this:

N_values [< N value 1>, < N value 2>, ...]

enc_values = [
    [enc_1_char_1, enc_1_char_2, ...],
    [enc_2_char_1, enc_2_char_2, ...],
    ...
]
"""
```

Next, use the Chinese Remainder Theorem to find the unique c^e value of each ciphered character.

```python
# List holding the values of m^e for each encrypted character
crt_vals = []

# Iterates through each character in the encrypted message
for i in range(len(enc_values[0])):
    
    # Creates a list of all different encryptions of the given character
    char_enc_vals = []
    for j in enc_values:
        char_enc_vals.append(int(j[i]))

    # Finds unique value of c^e using CRT
    crt_val = crt(N_values, char_enc_vals)
    crt_vals.append(crt_val[0])
```

Finally, once you have the unique values of c^e for each character, you can brute force the value of e by iterating through possible values of e, taking the Eth root of the CRT values generated for each encrypted character, and seeing if that root decrypts to the known crib text of "flag" for the first 4 characters (you could also just print the entire plaintext message for each E candidate if you didn't know the crib, but it takes a lot longer).

```python
# Brute force the reused value of e
e = 0
while True:
    plaintext_try = ''
    e += 1
    crib_count = 0
    for c in crt_vals:
        crib_count += 1
        try:
            # Take the Eth root of the CRT output, and see if it's in range to decode to a character
            # Uses decimal library to operate on large numbers
            test = Decimal(int(c)) ** (Decimal(1.0) / Decimal(e))
            decoded = chr(int(test))
            plaintext_try += decoded
        except:
            plaintext_try = 'not a valid decoded value'
            break
        
        # Checking against the crib after 4 characters to greatly reduce runtime
        if(crib_count == 4):
            if(not 'flag' in plaintext_try):
                plaintext_try = f'failed crib check after 4 characters {plaintext_try}'
                break
   
    if('flag' in plaintext_try):
        break
    else:
        try:
            print(f'Testing e={e}:\t{plaintext_try}')
        except Exception as ex:
            print(f'Testing e={e}:\t{ex}')

print(f'Plaintext found with e={e}:\t{plaintext_try}')
``` 

## Final Solve Script

```python
from sympy.ntheory.modular import crt
from decimal import Decimal

enc_values = [[]]
N_values = []

# Opens custom text file and reads data copied from server
with open('solve.txt', 'r') as f:
    N_values = f.readline().split(',')
    for i in range(len(N_values)):
        N_values[i] = int(N_values[i].strip())
    enc_values = f.readlines()
    for i in range(len(enc_values)):
        enc_values[i] = enc_values[i].strip().split(',')

"""
Format of solve.txt:

Line 1: {N_value 1}, {N_value 2}, {N_value 3}
Line 2: encrypted flag 1 (comma separated)
Line 3: encrypted flag 2 (comma separated)
Line 4: encrypted flag 3 (comma separated)

Once it's loaded into python, the variables should look like this:

N_values [< N value 1>, < N value 2>, ...]

enc_values = [
    [enc_1_char_1, enc_1_char_2, ...],
    [enc_2_char_1, enc_2_char_2, ...],
    ...
]
"""

# List holding the values of m^e for each encrypted character
crt_vals = []

# Iterates through each character in the encrypted message
for i in range(len(enc_values[0])):
    
    # Creates a list of all different encryptions of the given character
    char_enc_vals = []
    for j in enc_values:
        char_enc_vals.append(int(j[i]))

    # Finds unique value of c^e using CRT
    crt_val = crt(N_values, char_enc_vals)
    crt_vals.append(crt_val[0])

# Brute force the reused value of e
e = 0
while True:
    plaintext_try = ''
    e += 1
    crib_count = 0
    for c in crt_vals:
        crib_count += 1
        try:
            # Take the Eth root of the CRT output, and see if it's in range to decode to a character
            # Uses decimal library to operate on large numbers
            test = Decimal(int(c)) ** (Decimal(1.0) / Decimal(e))
            decoded = chr(int(test))
            plaintext_try += decoded
        except:
            plaintext_try = 'not a valid decoded value'
            break
        
        # Checking against the crib after 4 characters to greatly reduce runtime
        if(crib_count == 4):
            if(not 'flag' in plaintext_try):
                plaintext_try = f'failed crib check after 4 characters {plaintext_try}'
                break
   
    if('flag' in plaintext_try):
        break
    else:
        try:
            print(f'Testing e={e}:\t{plaintext_try}')
        except Exception as ex:
            print(f'Testing e={e}:\t{ex}')

print(f'Plaintext found with e={e}:\t{plaintext_try}')
```