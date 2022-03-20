from PIL import Image
import threading
from math import floor

# take input image
image_name = input("Name of image file: ")

# open specified image
try:
	i = Image.open(image_name)
except:
	print("No such file exists.")
	quit()
width, height = i.size

# take size for output
new_size = int(input("Output size: "))

# create variables including ascii gradient
ascii_chars = " ,-~!%#$&@"
row = 0
l = 0
t = 0
r = 0
b = 0

lock = threading.Lock()

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

# create function to draw output image with ascii gradient
def draw_func(row, new_size):
	# lock to prevent threads from printing rows out of order
	with lock:
		layer = ""
		column = 0
		# create row of ascii characters
		while column < new_size:
			# select a section of the original image to process
			l = column * (width / new_size)
			t = row * (height / new_size)
			r = (column + 1) * (width / new_size)
			b = (row + 1) * (width / new_size)		
			
			# process the image section
			i2 = i.crop((l, t, r, b))
			b = calculate_brightness(i2)
			char_ind = floor(b * len(ascii_chars))
			if char_ind > (len(ascii_chars) - 1):	char_ind = len(ascii_chars) - 1
			char = ascii_chars[char_ind]
			layer = layer + char
		
			column += 1
		# print layer when done
		print(layer)	

# create threads
for index in range(new_size):
	thread = threading.Thread(target=draw_func, args=(index, new_size))
	thread.start()
	
	