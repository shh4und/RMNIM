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

def gaussian_blur(images, n=0, sig=2.0):
    """
    Apply Gaussian Blurring to a list of images.
    
    Parameters:
    - images: A list of images.
    - n: Kernel size for the Gaussian filter.
    
    Returns:
    - An array of blurred images.
    """
    return np.array([cv2.GaussianBlur(img, (n, n), sigmaX=sig) for img in images])

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

def bilateral_blur(images, n=9, sigcolor=75, sigspace=75):
    """
    Apply Bilateral Filtering to a list of images.
    
    Parameters:
    - images: A list of images.
    - n: Kernel size for the Bilateral Filter.
    - sigcolor: Filter sigma in the color space.
    - sigspace: Filter sigma in the coordinate space.
    
    Returns:
    - An array of blurred images.
    """
    return np.array([cv2.bilateralFilter(img, n, sigmaColor=sigcolor, sigmaSpace=sigspace) for img in images])
