import base64
from hashlib import md5

key = 'SNrTxg1fXAXOuXf3O+ZYyzsjhGprmgyaSNrTxg1fXAXOuXf3O+ZYyzsjhGprmgyaSNrTxg1fXAXOuXf3O+ZYyzsjhGprmgyaSNrTxg1fXAXOuXf3O+ZYyzsjhGprmgya'.encode()

def enc(plain):
    plain = plain.encode()
    encrypted = bytes([a ^ b for a, b in zip(plain, key)])
    enc_base = base64.b64encode(encrypted).decode()
    print(enc_base)

enc('Hello there.')
enc('General Kenobi, you are a bold one.')
enc('Your move.')
enc("You fool. I've been trained in your cryptography arts by Count Dooku!")
enc("Attack, Kenobi! flag{a23f721aeff7b65bc87e24015a54aa53}")
enc("So uncivilized...")

#enc_bytes = base64.b64decode(enc_base)
#dec_bytes = bytearray()
#for i in range(len(enc_bytes)):
#    dec_bytes.append(enc_bytes[i] ^ key[i])
#    print(dec_bytes.decode())
#    print(md5(dec_bytes).hexdigest())
