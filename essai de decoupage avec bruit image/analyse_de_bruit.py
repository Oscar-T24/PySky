from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

# Load the image and convert it to grayscale
im = Image.open("sky.jpg").convert('L')
pix = np.array(im)

# Choose the median column
col_index = int(np.median(np.arange(pix.shape[1])))
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

# Calculate the slope of the standard deviation values
slope = np.abs(np.diff(std))

# Find the index with the highest slope
max_slope_index = np.argmax(slope)

# Calculate the trust coefficient
trust = 1 - (max_slope_index - len(slope)/2) / (len(slope)/2)

# Plot the standard deviation for the column and mark the point with the highest slope
plt.plot(std)
plt.plot(max_slope_index, std[max_slope_index], 'ro')
plt.show()

# Print the trust coefficient and the y index with the highest slope

print("Trust coefficient:", trust)
print("Y index with highest slope:", max_slope_index)
