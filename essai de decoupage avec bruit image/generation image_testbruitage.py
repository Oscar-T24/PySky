from PIL import Image, ImageDraw
import random

# Set the image dimensions
width = 400
height = 400

# Create a new image object with the specified dimensions and color
img = Image.new('RGB', (width, height), color='white')

# Create a draw object for the image
draw = ImageDraw.Draw(img)

# Draw the first stripe
draw.rectangle((0, 0, width, height/2), fill='white')

# Draw the second stripe
for y in range(int(height/2), height):
    for x in range(width):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        draw.point((x, y), fill=(r, g, b))

# Save the image
img.save('stripes.jpg')
