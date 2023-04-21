import cv2 
import numpy as np
def determine_weather_index(sky_image):
    # Convert image to grayscale
    gray_image = cv2.cvtColor(sky_image, cv2.COLOR_BGR2GRAY)
    
    # Compute mean and standard deviation of pixel intensities
    mean_intensity = np.mean(gray_image)
    std_intensity = np.std(gray_image)
    
    # Compute index based on mean and standard deviation
    index = 1 - (mean_intensity / 255) + (std_intensity / (2*255))
    
    # Normalize index to range of 0 to 1
    max_index = (255 / 255) + ((255 / (2*255)))
    normalized_index = index / max_index
    
    return normalized_index*100 # mulitplier par 100 pour qu'il prenne plus d'importance dans la mesure

