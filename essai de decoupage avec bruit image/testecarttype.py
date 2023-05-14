from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

# Load the image and convert it to grayscale
im = Image.open("stripes.jpg").convert('L')
pix = np.array(im)

# Choose the column to analyze
col_index = 50
col = pix[:, col_index]

# Calculate the standard deviation of the pixels surrounding each pixel in the column
std = np.zeros(col.shape)
for i in range(col.shape[0]):
    if i == 0:
        std[i] = np.std(col[i:i+2])
    elif i == col.shape[0]-1:
        std[i] = np.std(col[i-1:i+1])
    else:
        std[i] = np.std(col[i-1:i+2])

# Plot the standard deviation for the column
plt.plot(std)
plt.show()
