from hashlib import md5
import string

# Generate hashes for each single character
hashes = {}
for s in string.printable:
    hashes[s] = md5(s.encode()).hexdigest()
#print(hashes)

# Load all groups of hashes from the log file (this is probably not the cleanest way but it works)
data = open('decryption_server.log', 'r').readlines()
filtered = [s.strip().split(' ')[-1] for s in data if 'digest' in s or 'factor' in s]

hash_groups = []
hash_group = []
for l in filtered:
    if(len(l) == 1):
        hash_groups.append(hash_group)
        hash_group = []
    else:
        hash_group.append(l)
hash_groups.append(hash_group)
hash_groups = hash_groups[1:]

# Iterate through all groups of hashes
for hash_group in hash_groups:
    crib = ''
    # Iterate through each hash in the group
    for this_hash in hash_group:
        # Start iterating through each possible character added by the hash, breaking on success
        for test_char in hashes.keys():
            crib_guess = crib + test_char
            # Compare hash of guess to hash in log file
            test_hash = md5(crib_guess.encode()).hexdigest()
            if(test_hash == this_hash):
                crib += test_char
                break
    # Print decrypted message
    print(crib)