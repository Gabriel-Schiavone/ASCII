from PIL import Image
import cv2
import os
import keyboard
from math import floor

# take size for output
new_size = int(input("Output size: "))

# create ascii character gradient
ascii_chars = " ,-~!%#$&@"

vc = cv2.VideoCapture(0)

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

# start creating video frames with ascii characters
while True:
	# capture frame from webcam and open it
	rval, frame = vc.read()
	cv2.imwrite("frame.png", frame)
	i = Image.open("frame.png")
	width, height = i.size

	row = 0
	column = 0
	layer = ""
	layers = []
	l = 0
	t = 0
	r = 0
	b = 0
	
	
	# generate ascii frame from webcam capture
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
			layer = layer + ascii_chars[floor(b * len(ascii_chars))]

			column += 1
		# build frame by adding one layer at a time
		layers.append(layer)
		layer = ""	
		row += 1
		column = 0
	# clean up
	os.remove("frame.png")
	os.system("cls")
	
	# print finished ascii frame
	for index in range(len(layers)):
		print(layers[index])

	# stop if 'q' is pressed
	if keyboard.is_pressed("q"):
		quit()
	