from PIL import Image
from math import floor

# take input image
image_name = input("Name of image file: ")

# open specified image
try:
	i = Image.open(image_name)
except:
	print("Error: No such file exists.")
	quit()
width, height = i.size

# take size for output
new_size = int(input("Output size: "))

# create variables including ascii gradient
row = 0
column = 0
layer = ""
ascii_chars = " ,-~!%#$&@"
l = 0
t = 0
r = 0
b = 0

# create function to calculate brightness
def calculate_brightness(image):
    greyscale_image = image.convert('L')
    histogram = greyscale_image.histogram()
    pixels = sum(histogram)
    brightness = scale = len(histogram)

    for index in range(0, scale):
        ratio = histogram[index] / pixels
        brightness += ratio * (-scale + index)

    return 1 if brightness == 255 else brightness / scale

# assign ascii characters to "pixels" based on brightness
while row < new_size:
	while column < new_size:
		# select a section of the original image to process
		l = column * (width / new_size)
		t = row * (height / new_size)
		r = (column + 1) * (width / new_size)
		b = (row + 1) * (width / new_size)

		# process the image section
		i2 = i.crop((l, t, r, b))
		b = calculate_brightness(i2)
		char_index = floor(b * len(ascii_chars))
		if char_index >= len(ascii_chars):	char_index = len(ascii_chars) - 1
		layer = layer + ascii_chars[char_index]

		column += 1
	# once a layer of "pixels" has been converted to ascii, print it and start the next
	print(layer)
	layer = ""	
	row += 1
	column = 0
	