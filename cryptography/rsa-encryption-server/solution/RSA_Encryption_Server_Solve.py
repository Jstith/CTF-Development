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
e = 740
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
