import cv2
import numpy as np


def truncate_sky(img):
    """
    premiere fonction tronquer
    :param : image PIL / opencv2
    :out : image tronquée ne gardant que le ciel
    """
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_sky = np.array([0, 0, 150])
    upper_sky = np.array([180, 50, 255])

    mask = cv2.inRange(hsv, lower_sky, upper_sky)

    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    max_area = 0
    max_contour = None
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > max_area:
            max_area = area
            max_contour = contour
    x, y, w, h = cv2.boundingRect(max_contour)

    sky = img[y:y + h, x:x + w]
    cv2.imwrite('sky.jpg', sky)
    return w, h, sky


def truncate_sky2(img):

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_sky = np.array([0, 70, 70])
    upper_sky = np.array([180, 255, 255])

    mask = cv2.inRange(hsv, lower_sky, upper_sky)

    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    edges = cv2.Canny(mask, 100, 200)

    contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    max_area = 0
    max_contour = None
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > max_area:
            max_area = area
            max_contour = contour
    x, y, w, h = cv2.boundingRect(max_contour)

    sky = img[y:y + h, x:x + w]
    return w, h, sky


def tronquer(image):
    """
    fonction tronquer principale
    utilise deux fonctions avec des seuils differents : truncate_sky() et truncate_sky2()
    truncate_sky2() n'est utilisée que si truncate_sky() renvoit une image trop petite
    si l'image est toujours trop petite, renvoyer l'image originale
    :param : image PIL / opencv2
    :out : image tronquée ne gardant que le ciel
    """
    height = image.shape[0]
    width = image.shape[1]

    w, h, sky = truncate_sky(image)
    if w < width // 2 and h < height // 2:
        w, h, sky = truncate_sky2(image)
        if w < width // 2 and h < height // 2:
            return image
        else:
            return sky
    else:
        return sky
