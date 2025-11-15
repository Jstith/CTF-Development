data = [139,143,137,163,155,144,145,142,156,145,150,143,135,137,155,139,145,145,165]

guess = input('Enter your guess for the flag: ')
check = list(guess)

for c in range(len(check)):

	# https://www.geeksforgeeks.org/ord-function-python/
	if not ord(check[c]) + 40 == data[c]:
		print("Incorrect")
		exit()
print("Correct!")