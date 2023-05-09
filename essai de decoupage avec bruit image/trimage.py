import numpy as np
from scipy.interpolate import UnivariateSpline
from PIL import Image, ImageDraw
from statsmodels.nonparametric.smoothers_lowess import lowess

# Load the image
im = Image.open("imagetest.jpg")
im = im.crop((0, 50, im.width, im.height-50))
pix = np.array(im)

# Find the maximum slope in each column
diffs = np.diff(pix, axis=0)
slopes = np.sqrt(np.sum(diffs**2, axis=2))
max_slope_y = np.argmax(slopes, axis=0)

# Fit a spline curve to the maximum slope points
x = np.arange(pix.shape[1])
spl = UnivariateSpline(x, max_slope_y, k=3, s=0.1)
best_fit_y = spl(x)

# Calculate the lower half of the image cut by the curve fit
lower_half_mask = np.zeros_like(pix)
for i in range(pix.shape[1]):
    lower_half_mask[:int(best_fit_y[i]), i] = 1
trimmed_pix = np.multiply(pix, lower_half_mask)

# Filter the trimmed image to remove lower part
lower_half_mask = np.ones_like(pix)
for i in range(pix.shape[1]):
    start_row = int(best_fit_y[i])
    col = trimmed_pix[:, i]
    for j in range(start_row, pix.shape[0]):
        if np.any(col == 0):
            lower_half_mask[j:, i] = 0
            break
trimmed_pix = np.multiply(trimmed_pix, lower_half_mask)

# Draw the interpolated line on the final image
draw = ImageDraw.Draw(im)
line_coords = list(zip(x, best_fit_y))
#draw.line(line_coords, fill=(255, 0, 0), width=2)

# Draw a line passing through the median y-value of the interpolated line in every column
median_y_values = []
for i in range(pix.shape[1]):
    col_y_values = spl(x[i])
    median_y_values.append(np.median(col_y_values))

median_line_coords = list(zip(x, median_y_values))
#draw.line(median_line_coords, fill=(0, 0, 255), width=5)

# Add a lowess regression line to the plot
lowess_coords = lowess(median_y_values, x, frac=0.1, return_sorted=False)
lowess_line_coords = list(zip(x, lowess_coords))
draw.line(lowess_line_coords, fill=(0, 255, 0), width=3)

# Trim the image
upper_half_mask = 1 - lower_half_mask
trimmed_pix = np.multiply(trimmed_pix, upper_half_mask)
trimmed_im = Image.fromarray(trimmed_pix)

# Save the final image with the interpolated line and lowess regression line
im.save("final_image.png")
