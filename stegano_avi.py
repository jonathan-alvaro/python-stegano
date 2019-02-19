import utils
from VideoIO import VideoFrame

def insert_stegano_info(frame, lsb_size, is_frame_random, is_pixel_random):
	#inserts stegano info on first frame
	if is_frame_random:
		frame_value = 1
	else:
		frame_value = 0

	if is_pixel_random:
		pixel_value = 1
	else:
		pixel_value = 0

	lsb_value = lsb_size - 1

	pixel = frame.get_pixel(0, 0)
	pixel[0] = ((pixel[0] >> 1) << 1) + frame_value
	pixel[1] = ((pixel[1] >> 1) << 1) + pixel_value
	pixel[2] = ((pixel[2] >> 1) << 1) + lsb_value

	frame.write_pixel(0, 0, pixel)

def extract_stegano_info(frame):
	pixel = frame.get_pixel(0, 0)
	frame_value = ((pixel[0] >> 1) << 1) + frame_value
	pixel_value = ((pixel[1] >> 1) << 1) + pixel_value
	lsb_value = ((pixel[2] >> 1) << 1) + lsb_value

	if frame_value == 1:
		is_frame_random = True
	else:
		is_frame_random = False

	if pixel_value == 1:
		is_pixel_random = True
	else:
		is_pixel_random = False

	lsb_size = lsb_value + 1

	return is_frame_random, is_pixel_random, lsb_value

def sequential_image_stegano(frame, message, lsb_size, size_x, size_y):
	# takes a single frame and outputs a frame with a message hidden in it
	bits = utils.str_to_bits(message)

	## SIMPAN PANJANG MESSAGE DI PIXEL PERTAMA
	pixel = frame.get_pixel(0,0)
	pixel[0] = len(bits)
	frame.write_pixel(0, 0, pixel)

	colour = 0
	x = 1
	y = 0
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

def extract_sequential(frame, lsb_size, size_x, size_y):
	# takes a single frame and extracts a hidden message

	# AMBIL PANJANG MESSAGE
	pixel = frame.get_pixel(0,0)
	message_length = pixel[0]

	x = 1
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