import numpy as np
from scipy.interpolate import UnivariateSpline
from PIL import Image, ImageDraw

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

# Compute the median y value of the spline for each column
median_y_values = []
for i in range(pix.shape[1]):
    column_points = spl.get_coeffs()[i:i+4]
    column_spline = np.poly1d(column_points[::-1])
    column_xs = np.linspace(i, i+1, 100)
    column_ys = column_spline(column_xs)
    median_y = np.median(column_ys)
    median_y_values.append(median_y)
median_y_values = np.array(median_y_values)

# Fit a new spline curve to the median y values
median_spl = UnivariateSpline(x, median_y_values, k=3, s=0.1)
best_fit_y = median_spl(x)

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
draw.line(line_coords, fill=(255, 0, 0), width=2)

# Save the trimmed image
trimmed_im = Image.fromarray(trimmed_pix)
trimmed_im.save("trimmed_image.jpg")

# Save the final image with the interpolated line
im.save("final_image.jpg")
