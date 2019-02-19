import utils

def sequential_image_stegano(frame, message, lsb_size, size_x, size_y):
	# takes a single frame and outputs a frame with a message hidden in it
	bits = utils.str_to_bits(message)

	x = 0
	y = 0
	colour = 0

	i = 0

	while (i < len(bits)):
		if(colour == 0):
			pixel = frame.get_pixel(x,y)

		if(lsb_size == 1):
			pixel[colour] = ((pixel[colour] >> 1) << 1) + bits[i]
			i = i + 1
		else:
			pixel[colour] = ((((pixel[colour] >> 2) << 1) + bits[i]) << 1) + bits[i+1]
			i = i + 2

		if(colour == 2):
			frame.write_pixel(x, y, pixel)
			x += 1

		colour = (colour + 1) % 3
		if (x >= size_x):
			x = 0
			y += 1

	if colour != 0:
		frame.write_pixel(x, y, pixel)

def seeded_image_stegano(frame, message, lsb_size, size_x, size_y, pixels):
	# takes a single frame and outputs a frame with a message hidden in it
	bits = utils.str_to_bits(message)

	colour = 0
	i = 0

	while (i < len(bits)):
		if(lsb_size == 1):
			pixel_pos = pixels[i]
		else:
			pixel_pos = pixels[i/2]

		x = pixel_pos % size_x
		y = pixel_pos / size_x
		pixel = frame.get_pixel(x,y)

		if(lsb_size == 1):
			pixel[colour] = ((pixel[colour] >> 1) << 1) + bits[i]
			i = i + 1
		else:
			pixel[colour] = ((((pixel[colour] >> 2) << 1) + bits[i]) << 1) + bits[i+1]
			i = i + 2

		frame.write_pixel(x, y, pixel)

		colour = (colour + 1) % 3

	if colour != 0:
		frame.write_pixel(x, y, pixel)

def extract_sequential(frame, message_length, lsb_size, size_x, size_y):
	# takes a single frame and extracts a hidden message

	x = 0
	y = 0
	colour = 0
	bits = []
	i = 0

	while (i < message_length):
		if(colour == 0):
			pixel = frame.get_pixel(x,y)

		if(lsb_size == 1):
			bit = (pixel[colour] << 7) >> 7
			bits.append(bit)
			i = i + 1
		else:
			bit = (pixel[colour] << 6) >> 7
			bits.append(bit)
			bit = (pixel[colour] << 7) >> 7
			bits.append(bit)
			i = i + 2
		

		if(colour == 2):
			x += 1

		colour = (colour + 1) % 3
		if (x >= size_x):
			x = 0
			y += 1

	message = utils.bits_to_str(bits)

	return message

def extract_seeded(frame, lsb_size, size_x, size_y, pixels):
	# takes a single frame and extracts a hidden message

	colour = 0
	bits = []
	i = 0

	while (i < len(pixels)):
		x = pixels[i] % size_x
		y = pixels[i] / size_x
		pixel = frame.get_pixel(x,y)

		if(lsb_size == 1):
			bit = (pixel[colour] << 7) >> 7
			bits.append(bit)
		else:
			bit = (pixel[colour] << 6) >> 7
			bits.append(bit)
			bit = (pixel[colour] << 7) >> 7
			bits.append(bit)

		i = i + 1

		colour = (colour + 1) % 3

	message = utils.bits_to_str(bits)

	return message