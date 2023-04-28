from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

# Load the image and convert it to grayscale
im = Image.open("test.jpg")
pix = np.array(im.convert('L'))

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
    for j in range(20,col.shape[0]-10): # on commence à 20 et on s'arrete avant les 10 derniers pour eviter d'avoir les banderoles météo sur la plupart des webcams
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

# Slice the image into upper and lower halves
upper_half_gray = pix[:int(max_slope_y[col_index]), :]
upper_half_rgb = np.zeros((upper_half_gray.shape[0], upper_half_gray.shape[1], 3), dtype=np.uint8)

# Retrieve the colors from the original image
for i in range(3):
    upper_half_rgb[:,:,i] = np.array(im)[:,:,i][:int(max_slope_y[col_index]), :]

# Save the upper half of the image
im_upper = Image.fromarray(upper_half_rgb)
im_upper.save("upper_half.jpg")
