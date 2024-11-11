import cv2
import numpy as np

def non_local_means(images:np.ndarray, n:int) -> np.ndarray:
    """Apply Non-Local Means denoising to a list of images

    Args:
        images (np.ndarray): image stack
        n (int): Denoising strength

    Returns:
        np.ndarray: An array of denoised images 
    """
    return np.array([cv2.fastNlMeansDenoising(img, h=n, templateWindowSize=9, searchWindowSize=21) for img in images])

def median_blur(images:np.ndarray, n:int) -> np.ndarray:
    """Apply Median Blurring to a list of images
    
    Args:
        images (np.ndarray): image stack
        n (int): Kernel size for the median filter
    Returns:
        np.ndarray: An array of blurred images
    """
    return np.array([cv2.medianBlur(img, n) for img in images])

def gaussian_blur(images, n=0, sig=2.0) -> np.ndarray:
    """Apply Gaussian Blurring to a list of images
    
    Args:
        images (np.ndarray): image stack
        n (int): Kernel size for the Gaussian filter
    
    Returns:
        np.ndarray: An array of blurred images
    """
    return np.array([cv2.GaussianBlur(img, (n, n), sigmaX=sig) for img in images])

def mean_blur(images:np.ndarray, n:int):
    """Apply Mean Blurring (Box Filtering) to a list of images
    
    Args:
        images (np.ndarray): image stack
        n (int): Kernel size for the mean filter
    
    Returns:
        np.ndarray: An array of blurred images.
    """
    return np.array([cv2.boxFilter(img, -1, (n, n)) for img in images])

def bilateral_blur(images:np.ndarray, n:int = 9, sigcolor:int = 75, sigspace:int = 75) -> np.ndarray:
    """Apply Bilateral Filtering to a list of images
    
    Args:
        images (np.ndarray): image stack
        n (int): Kernel size for the mean filter
        sigcolor (int): Filter sigma in the color space
        sigspace (int): Filter sigma in the coordinate space
    
    Returns:
        np.ndarray: An array of blurred images.
    """
    return np.array([cv2.bilateralFilter(img, n, sigmaColor=sigcolor, sigmaSpace=sigspace) for img in images])
