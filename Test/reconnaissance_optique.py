import cv2
import pytesseract
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' #https://stackoverflow.com/questions/34966541/how-can-one-display-an-image-using-cv2-in-python

#https://towardsdatascience.com/optical-character-recognition-ocr-with-less-than-12-lines-of-code-using-python-48404218cccb


def ocr(img):
    cv2.imshow('image',img)
    cv2.waitKey(0)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    gray, img_bin = cv2.threshold(gray,128,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    gray = cv2.bitwise_not(img_bin)

    kernel = np.ones((2, 1), np.uint8)
    img = cv2.erode(gray, kernel, iterations=1)
    img = cv2.dilate(img, kernel, iterations=1)
    out_below = pytesseract.image_to_string(img)
    return out_below


for i in range(1):
    try:
        img = cv2.imread('test.png')
        print(ocr(img))
    except cv2.error:
        #fragmenter l'image en 2 et faire la meme chose pour chaque image (comme ca les dimensions sont moins grandes et ca rique moins de planter)
        img = cv2.imread('test.png')
        h, w, channels = img.shape
        half2 = h//2
        top = img[:half2, :]
        bottom = img[half2:, :]
        test1 = ocr(top)
        test2 = ocr(bottom)
        print('resultat du haut,',test1,'resultat du bas',test2)
            
