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
    #print(c)
    decoded = pow(int(c), d, n)
    print(chr(decoded), end='')