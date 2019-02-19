import re
import sys
import os

def remove_symbols(str):
	alphabet = re.compile('[^a-zA-Z]')
	new_str = alphabet.sub('', str)

	return new_str

def make_playfair_key(incomplete_key):
	alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
	complete_key = ""

	for letter in incomplete_key:
		if letter in alphabet:
			alphabet.remove(letter)
			complete_key = complete_key + letter

	for letter in alphabet:
		complete_key = complete_key + letter

	return complete_key

def prepare_playfair_text(text):
	prepared_pairs = []

	n = len(text)
	i = 0

	while (i < n-1):
		pair = ""
		char1 = text[i]
		char2 = text[i+1]

		if char1 == char2:
			char2 = 'X'
			i += 1
		else:
			i += 2

		if char1 == 'J':
			char1 == 'I'
		if char2 == 'J':
			char2 == 'I'

		pair = pair + char1 + char2
		prepared_pairs.append(pair)

	if (i == n-1):
		pair = ""
		pair = pair + text[i] + 'X'

		prepared_pairs.append(pair)

	return prepared_pairs

def playfair_cipher_pair(pair, key):

	pos1 = key.find(pair[0])
	pos2 = key.find(pair[1])

	row1 = int(pos1 / 5)
	row2 = int(pos2 / 5)

	col1 = pos1 % 5
	col2 = pos2 % 5

	if(row1 == row2):
		cipher_pos1 = row1*5 + (col1 + 1) % 5
		cipher_pos2 = row2*5 + (col2 + 1) % 5
	elif(col1 == col2):
		cipher_pos1 = ((row1 + 1) % 5)*5 + col1
		cipher_pos2 = ((row2 + 1) % 5)*5 + col2
	else:
		cipher_pos1 = row1*5 + col2
		cipher_pos2 = row2*5 + col1

	new_char1 = key[cipher_pos1]
	new_char2 = key[cipher_pos2]

	new_pair = ""
	new_pair = new_pair + new_char1 + new_char2

	return new_pair

def playfair_cipher(text, key, encrypt):
	if (not encrypt):
		key = "".join(reversed(key))

	new_text = ""

	for pair in text:
		new_pair = playfair_cipher_pair(pair, key)
		new_text = new_text + ' ' + new_pair

	return new_text.strip()

def group_by_five(str):
	#outputs string with letters in groups of five divided by spaces
	new_str = ""
	i = 0

	for letter in str:
		if(i >= 5):
			i = 1
			new_str = new_str + ' '
		else:
			i += 1

		new_str = new_str + letter

	return new_str

def alphabet_to_num (char):
	#mengubah huruf alphabet menjadi angka 0-25
	num = ascii_to_num(char)
	num = num - 65
	return num

def num_to_alphabet (num):
	#mengubah angka 0-25 menjadi alphabet
	num = num + 65
	char = num_to_ascii(num)
	return char

def ascii_to_num (char):
	#mengubah huruf ascii menjadi angka 0-255
	num = ord(char)
	return num

def num_to_ascii (num):
	#mengubah angka 0-255 menjadi ascii
	char = chr(num)
	return char

def caesar_cipher (char, key, encrypt):
	num = alphabet_to_num(char)
	key_num = alphabet_to_num(key)
	if encrypt:
		num = (num + key_num) % 26
	else:
		num = (num - key_num) % 26
	new_char = num_to_alphabet(num)
	return new_char

def modified_caesar_cipher (char, key, encrypt, sub):
	num = sub.find(char)
	key_num = alphabet_to_num(key)
	if encrypt:
		num = (num + key_num) % 26
	else:
		num = (num - key_num) % 26
	new_char = sub[num]
	return new_char

def extended_caesar_cipher (char, key, encrypt):
	num = char
	key_num = ascii_to_num(key)
	if encrypt:
		num = (num + key_num) % 256
	else:
		num = (num - key_num) % 256
	new_char = num_to_ascii(num)
	return new_char

def extended_vigenere_cipher(text, key, encrypt):
	new_text = ""
	n = len(key)
	for i, char in enumerate(text):
		i = i % n
		new_char = extended_caesar_cipher(char, key[i], encrypt)
		new_text = new_text + new_char

	new_text = bytearray(new_text, "latin-1")

	return new_text

def standard_vigenere_cipher(text, key, encrypt):
	alphabet = re.compile('[^a-zA-Z]')
	new_text = ""
	n = len(key)
	for i, char in enumerate(text):
		if (not re.search(alphabet, char)):
			i = i % n
			new_char = caesar_cipher(char, key[i], encrypt)
			new_text = new_text + new_char
		else:
			new_text = new_text + char
	return new_text

def autokey_vigenere_cipher(text, key, encrypt):
	alphabet = re.compile('[^a-zA-Z]')
	new_text = ""
	if(encrypt):
		key = key + text
		for i, char in enumerate(text):
			if (not re.search(alphabet, char)):
				new_char = caesar_cipher(char, key[i], encrypt)
				new_text = new_text + new_char
			else:
				new_text = new_text + char
	else:
		for i, char in enumerate(text):
			if (not re.search(alphabet, char)):
				new_char = caesar_cipher(char, key[i], encrypt)
				new_text = new_text + new_char
				key = key + new_char
			else:
				new_text = new_text + char
				key = ' ' + key;
			
	return new_text

def full_vigenere_cipher(text, key, encrypt, sub):
	alphabet = re.compile('[^a-zA-Z]')
	new_text = ""
	n = len(key)
	for i, char in enumerate(text):
		if (not re.search(alphabet, char)):
			i = i % n
			new_char = modified_caesar_cipher(char, key[i], encrypt, sub)
			new_text = new_text + new_char
		else:
			new_text = new_text + char
	return new_text

def vigenere_cipher(type, text, key, encrypt):
	if type == 1:
		new_text = standard_vigenere_cipher(text, key, encrypt)
	elif type == 2: #full vigenere
		input_file = "full_vigenere.txt"
		f = open(input_file, 'r')
		sub = f.read()
		f.close()
		new_text = full_vigenere_cipher(text, key, encrypt, sub)
	elif type == 4: #autokey vigenere
		new_text = autokey_vigenere_cipher(text, key, encrypt)
	else: #extended cipher
		new_text = extended_vigenere_cipher(text, key, encrypt)

	return new_text

def input_choices():
	action_type = 0
	while (action_type < 1 or action_type > 2):
		print("1. Enkripsi")
		print("2. Dekripsi")
		action_type = int(input("Pilihan : "))
		if (action_type < 1 or action_type > 2):
			print("Pilihlah pilihan yang sesuai\n")

	if (action_type == 1):
		encrypt = True
	else:
		encrypt = False

	#Pilih jenis cipher
	cipher_type = 0
	while (cipher_type < 1 or cipher_type > 6):
		print("\nPilih Jenis Cipher")
		print("==========================")
		print("1. Standard vigenere Cipher")
		print("2. Full vigenere Cipher")
		print("3. Auto-Key vigenere Cipher")
		print("4. Running-Key vigenere Cipher")
		print("5. Extended vigenere Cipher")
		print("6. Playfair Cipher")
		cipher_type = int(input("Pilihan : "))
		if (cipher_type < 1 or cipher_type > 6):
			print("Pilihlah pilihan yang sesuai\n")

	#Baca Input
	if(cipher_type != 5):
		text_choice = 0
		while (not (text_choice == 1 or text_choice == 2)):
			print("1. Input text dari file")
			print("2. Input text dari keyboard")
			text_choice = int(input("Pilihan : "))
			if (not (text_choice == 1 or text_choice == 2)):
				print("Pilihlah pilihan yang sesuai\n")
	else:
		text_choice = 1;

	#Baca Key
	key_choice = 0
	if (cipher_type != 4):
		while (not (key_choice == 1 or key_choice == 2)):
			print("1. Input key dari file")
			print("2. Input key dari keyboard")
			key_choice = int(input("Pilihan : "))
			if (not (key_choice == 1 or key_choice == 2)):
				print("Pilihlah pilihan yang sesuai\n")

	#Baca Pilihan output
	output_choice = 0
	if (not cipher_type in [5,6]):
		print("\nPilih Jenis Output")
		print("==========================")
		if(encrypt):
			while (output_choice < 1 or output_choice > 3):
				print("1. Dalam kelompok 5-huruf")
				print("2. Dengan spasi dan tanda baca")
				print("3. Tanpa spasi, dengan tanda baca")
				output_choice = int(input("Pilihan : "))
				if (not (output_choice >= 1 or output_choice <= 3)):
					print("Pilihlah pilihan yang sesuai\n")
		else:
			while (output_choice < 1 or output_choice > 3):
				print("1. Dalam kelompok 5-huruf")
				print("2. Tidak diubah")
				print("3. Tanpa spasi")
				output_choice = int(input("Pilihan : "))
				if (not (output_choice >= 1 or output_choice <= 3)):
					print("Pilihlah pilihan yang sesuai\n")
	else:
		output_choice = 2

	print("\n================================\n")

	if(text_choice == 1):
		if(cipher_type != 5):
			input_file = input("Input file text : ")
			f = open(input_file, 'r')
			text = f.read()
			f.close()
		else:
			input_file = input("Input file text : ")
			f = open(input_file, 'rb')
			text = f.read()
			f.close()
	else:
		text = input("Input text : ")

	print()

	if(not key_choice == 0):
		if(key_choice == 1):
			input_file = input("Input file key : ")
			f = open(input_file, 'r')
			key = f.read()
			f.close()
		else:
			key = input("Input key : ")
	else:
		input_file = "proklamasi.txt"
		f = open(input_file, 'r')
		key = f.read()
		f.close()

	return encrypt, cipher_type, text, key, output_choice

def main():
	os.system('cls' if os.name == 'nt' else 'clear')

	encrypt, cipher_type, text, key, output_choice = input_choices()

	if (cipher_type != 5):
		text = text.upper()
		key = key.upper()
		key = remove_symbols(key)
		key = key.replace(" ", "")

		if (output_choice == 1):
			text = remove_symbols(text)
		elif (output_choice == 3):
			text = text.replace(" ", "")

		if(cipher_type == 6):
			text = remove_symbols(text)
			text = text.replace(" ", "")

	if (cipher_type == 6):
		text = prepare_playfair_text(text)
		key = make_playfair_key(key)
		new_text = playfair_cipher(text, key, encrypt)
	else: #vigenere
		if (cipher_type in [1,4]):
			vigenere_type = 1
		elif (cipher_type == 2): #full vigenere
			vigenere_type = 2
		elif (cipher_type == 5): #extended vigenere
			vigenere_type = 3
		else: #cipher_type == 3, auto-key
			vigenere_type = 4

		new_text = vigenere_cipher(vigenere_type, text, key, encrypt)

	print("\n=================")

	if (output_choice == 1):
		new_text = group_by_five(new_text)

	print("Lihat hasil pada layar? (y/n)")
	print_result = '0'
	while (print_result.upper() != 'Y' and print_result.upper() != 'N'):
		print_result = input()
		if(print_result.upper() != 'Y' and print_result.upper() != 'N'):
			print("Pilih (y/n):")

	print("\nCetak hasil pada file? (y/n)")
	print_file = '0'
	while (print_file.upper() != 'Y' and print_file.upper() != 'N'):
		print_file = input()
		if(print_file.upper() != 'Y' and print_file.upper() != 'N'):
			print("Pilih (y/n):")

	if (print_file.upper() == 'Y'):
		output_file = input("\nFile output : ")
		if(cipher_type == 5):
			f = open(output_file, 'wb')
			f.write(new_text)
			f.close()
		else:
			f = open(output_file, 'w')
			f.write(new_text)
			f.close()

	if (print_result.upper() == 'Y'):
		print("\n\n==========HASIL==========\n")
		print(new_text)

	return 0

if __name__ == "__main__":
    main()