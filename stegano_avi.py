import utils

def sequential_image_stegano(frame, message, lsb_size, size_x, size_y):
	# takes a single frame and outputs a frame with a message hidden in it
	bits = str_to_bits(message)

	x = 0
	y = 0
	colour = 0

	for bit in bits:
		if(colour == 0):
			pixel = frame.get_pixel(x,y)
			pixel[0] = ((pixel[0] >> 1) << 1) + bit
		elif(colour == 1):
			pixel[1] = ((pixel[1] >> 1) << 1) + bit
		else:
			pixel[2] = ((pixel[2] >> 1) << 1) + bit
			frame.write_pixel(x, y, pixel)
			x += 1

		colour = (colour + 1) % 3
		if (x >= size_x):
			x = 0
			y += 1

	if colour != 0:
		frame.write_pixel(x, y, pixel)