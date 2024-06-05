import cv2
import numpy as np

def non_local_means(images, n):
    """
    Apply Non-Local Means denoising to a list of images.
    
    Parameters:
    - images: A list of images.
    - n: Denoising strength.
    
    Returns:
    - An array of denoised images.
    """
    return np.array([cv2.fastNlMeansDenoising(img, h=n, templateWindowSize=9, searchWindowSize=21) for img in images])

def median_blur(images, n):
    """
    Apply Median Blurring to a list of images.
    
    Parameters:
    - images: A list of images.
    - n: Kernel size for the median filter.
    
    Returns:
    - An array of blurred images.
    """
    return np.array([cv2.medianBlur(img, n) for img in images])

def gaussian_blur(images, n):
    """
    Apply Gaussian Blurring to a list of images.
    
    Parameters:
    - images: A list of images.
    - n: Kernel size for the Gaussian filter.
    
    Returns:
    - An array of blurred images.
    """
    return np.array([cv2.GaussianBlur(img, (n, n), 0) for img in images])

def mean_blur(images, n):
    """
    Apply Mean Blurring (Box Filtering) to a list of images.
    
    Parameters:
    - images: A list of images.
    - n: Kernel size for the mean filter.
    
    Returns:
    - An array of blurred images.
    """
    return np.array([cv2.boxFilter(img, -1, (n, n)) for img in images])