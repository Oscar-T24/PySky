from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline

# Load the image and convert it to grayscale
im = Image.open("lol.jpg").convert('L')
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


# Plot the results on top of the image
fig, ax = plt.subplots()
ax.imshow(pix, cmap='gray', alpha=0.5)
scatter = ax.scatter(np.arange(pix.shape[1]), max_slope_y, c=trusts)
ax.set_xlim([0, pix.shape[1]])
ax.set_ylim([pix.shape[0], 0])
ax.set_xlabel("Column index")
ax.set_ylabel("Row index")
fig.colorbar(scatter, ax=ax)

# Save the image
fig.savefig("lol_with_sc")

plt.show()
