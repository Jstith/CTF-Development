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