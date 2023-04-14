import cv2
import numpy as np

# Load image
image = cv2.imread('letriadou.png')

# Convert image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Threshold image to create binary mask
ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

# Calculate percentage of white pixels in mask
white_pixels = np.sum(thresh == 255)
total_pixels = image.shape[0] * image.shape[1]
percentage_white = white_pixels / total_pixels

# Determine weather based on percentage of white pixels
if percentage_white > 0.8:
    print('Sunny')
elif percentage_white > 0.5:
    print('Cloudy')
elif percentage_white > 0.2:
    print('Rainy')
else:
    print('Foggy')
