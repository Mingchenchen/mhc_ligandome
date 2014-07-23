letters = 'ARNDBCEQZGHILKMFPSTWYV'
assert len(letters) == 20

values = {}
for i, l in enumerate(letters):
	values[l] = i

def encode(pep):
	n = len(pep)
	total = 0
	for i, letter in enumerate(pep):
		x = values[letter]
		base = 20 ** (n - i - 1)
		total += base * values[letter]
	return total 
	