def str_to_bits(string):
	result = []
	for char in string:
		bits = bin(ord(char))[2:]
		bits = '00000000'[len(bits):] + bits
		result.extend([int(b) for b in bits])
	return result

def bits_to_str(bits):
	string = []
	for b in range(len(bits) / 8):
		byte = bits[b*8:(b+1)*8]
		string.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
	return ''.join(chars)