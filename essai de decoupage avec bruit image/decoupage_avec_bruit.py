from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
from scipy.interpolate import make_interp_spline

# Load the image and convert it to grayscale
im = Image.open("imagetest.jpg").convert('L')
pix = np.array(im)

# Choose the column to analyze
col_index = int(np.median(np.arange(pix.shape[1])))

# Initialize arrays to store the results
max_slope_indices = np.zeros(pix.shape[1])
trusts = np.zeros(pix.shape[1])

# Loop over every column
for i in range(pix.shape[1]):
    col = pix[:, i]

    # Calculate the standard deviation of the pixels surrounding each pixel in the column
    std = np.zeros(col.shape)
    for j in range(col.shape[0]):
        if j == 0:
            std[j] = np.std(col[j:j+2])
        elif j == col.shape[0]-1:
            std[j] = np.std(col[j-1:j+1])
        else:
            std[j] = np.std(col[j-1:j+2])

    # Calculate the slope of the standard deviation values
    slope = np.abs(np.diff(std))

    # Find the index with the highest slope
    max_slope_index = np.argmax(slope)

    # Calculate the trust coefficient
    trust = 1 - (max_slope_index - len(slope)/2) / (len(slope)/2)

    # Store the results for this column
    max_slope_indices[i] = max_slope_index
    trusts[i] = trust

# Find the y values with the highest slopes for each column
max_slope_y = np.zeros(pix.shape[1])
for i in range(pix.shape[1]):
    if max_slope_indices[i] == 0:
        max_slope_y[i] = 0
    elif max_slope_indices[i] == pix.shape[0]-1:
        max_slope_y[i] = pix.shape[0]-1
    else:
        max_slope_y[i] = np.argmax(np.abs(np.diff(std[int(max_slope_indices[i])-1:int(max_slope_indices[i])+2]))) + int(max_slope_indices[i]) - 1


# Add small random values to duplicate values
unique_max_slope_y, unique_indices = np.unique(max_slope_y, return_index=True)
duplicates = np.setdiff1d(np.arange(len(max_slope_y)), unique_indices)
for idx in duplicates:
    max_slope_y[idx] += np.random.uniform(-0.1, 0.1)

# Sort the indices by the x values
sorted_indices = np.argsort(max_slope_y)

# Create a spline interpolation of the sorted indices
spline = make_interp_spline(max_slope_y[sorted_indices], np.arange(pix.shape[1])[sorted_indices], k=3)

# Evaluate the spline on a finer grid
x = np.linspace(0, pix.shape[1], num=pix.shape[1]*10)
y = spline(x)

# Plot the best fit line
plt.plot(x, y, color='r')

# Calculate the horizontal line based on the dots and their trust coefficient
mean_slope_y = np.mean(max_slope_y)
mean_trust = np.mean(trusts)
y_horiz = mean_slope_y + (pix.shape[0] - mean_slope_y) * mean_trust

# Plot the horizontal line
plt.axhline(y_horiz, color='g', linestyle='--')

# Plot the results on top of the image
fig, ax = plt.subplots()
ax.imshow(pix, cmap='gray', alpha=0.5)

plt.show()

