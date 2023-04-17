import cv2

def truncate_sky(image_path):
    # Load the image and convert it to the HSV color space
    img = cv2.imread(image_path)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Define the range of blue colors in HSV color space
    lower_blue = (90, 50, 50)
    upper_blue = (130, 255, 255)

    # Threshold the image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Find the contours of the blue regions in the image
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Get the bounding box of the largest contour (i.e., the sky region)
    max_area = 0
    max_contour = None
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > max_area:
            max_area = area
            max_contour = contour
    x, y, w, h = cv2.boundingRect(max_contour)

    # Extract the sky region from the original image and save it
    sky = img[y:y+h, x:x+w]
    cv2.imwrite('sky.jpg', sky)

# Example usage
truncate_sky('static.infoclimat.net-imageserver.jpg')
