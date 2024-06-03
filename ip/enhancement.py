import cv2
import numpy as np

def non_local_means(images, n):
    nlm = []
    for img in images:
        i = cv2.fastNlMeansDenoising(img, h = n,templateWindowSize = 9, searchWindowSize = 21)
        nlm.append(img)
    return np.array(nlm)
    
def median_blur(images, n):
    median_blurreds = []
    for img in images:
        blur = cv2.medianBlur(img, n)
        median_blurreds.append(blur)
    return np.array(median_blurreds)

def gaussian_blur(images, n):
    gaussian_blurreds = []
    for img in images:
        blur = cv2.GaussianBlur(img,(n,n),0)
        gaussian_blurreds.append(blur)
    return np.array(gaussian_blurreds)