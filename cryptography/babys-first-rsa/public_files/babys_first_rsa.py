from secrets import randbits
from sympy import nextprime

def encrypt(inp):
    p = nextprime(randbits(32))
    q = nextprime(randbits(32))
    e = 65537
    n = p * q
    enc = [pow(ord(c), e, n) for c in inp]
    return [n, e, enc]

plaintext = open('flag.txt').read()

with open('output.txt', 'w') as f:
    data = encrypt(plaintext)
    f.write(f'N: {data[0]}\ne: {data[1]}\nCipher Text:\n')
    f.write("".join(f'{e} ' for e in data[2]))
    f.write('\n\n')