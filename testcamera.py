import requests
from PIL import Image, ImageChops
from io import BytesIO
import time

# Set the URL for the webcam
url = "http://86.241.3.36:81/videostream.cgi?loginuse=admin&loginpas=0000"

# Initialize the last frame
last_frame = None

# Loop indefinitely
while True:
    # Get the image from the URL
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))

    # If this is the first frame, set it as the last frame
    if last_frame is None:
        last_frame = img

    # Compare the current frame with the last frame
    diff = ImageChops.difference(img, last_frame)
    diff = diff.convert("L")
    threshold = 5
    if diff.getbbox() and diff.getextrema()[1] > threshold:
        print("Motion detected!")

    # Display the current frame
    img.show()

    # Set the current frame as the last frame
    last_frame = img

    # Wait for 1 second before getting the next frame
    time.sleep(1)
