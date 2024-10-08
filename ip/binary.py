import cv2
import numpy as np

def segment(images: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """Function to make a image stack segmentation with its mask

    Args:
        images (NDArray): image stack
        mask (NDArray): image stack mask

    Returns:
        NDArray: returns a segmented image stack
    """
    return np.array([cv2.bitwise_and(img, img, mask=binary) for img, binary in zip(images, mask)])

def otsu_binary(images: np.ndarray) -> np.ndarray:
    """Function to create a binary image stack with Otsu threshold technique

    Args:
        images (NDArray): image stack

    Returns:
        NDArray: returns a Otsu binary mask of the given image stack
    """
    return np.array([cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1] for img in images])

def simple_binary(images: np.ndarray, thresh: int) -> np.ndarray:
    """Function to create a binary image stack from a chosen bottom threshold 

    Args:
        images (NDArray): image stack
        thresh (int): threshold value

    Returns:
        NDArray: returns a binary mask of the given image stack
    """
    
    return np.array([cv2.threshold(img, thresh, 255, cv2.THRESH_BINARY)[1] for img in images])

def morphological(images: np.ndarray, op, shape_kernel, size_kernel: tuple[int]) -> np.ndarray:
    """Function to apply morphological operation from OpenCV lib over a given image stack

    Args:
        images (NDArray): image stack
        op (MorphTypes): type of a morphological operation such as: cv.MORPH_ERODE, cv.MORPH_DILATE, cv.MORPH_OPEN, cv.MORPH_CLOSE
        shape_kernel (MorphShapes): element shape that could be one of cv.MORPH_RECT, cv.MORPH_CROSS or cv.MORPH_ELLIPSE
        size_kernel (tuple(int, int)): size of the structuring element

    Returns:
        NDArray: returns a image stack from a chosen morphological operation
    """

    kernel = cv2.getStructuringElement(shape_kernel, size_kernel)
    
    return np.array([cv2.morphologyEx(img, op, kernel) for img in images])
    
    


def skel_zhang_suen(images: np.ndarray) -> np.ndarray:
    """Function to compute a skeleton of a given image stack using thinning technique of Zhang-Suen (from OpenCV lib).

    Args:
        images (NDArray): image stack

    Returns:
        NDArray: returns a skeleton 
    """
    return np.array([cv2.ximgproc.thinning(img) for img in images])

def mean_threshold(images: np.ndarray, factor:int = 1) -> int:
    """Function to calculate the mean value of a given image stack

    Args:
        images (NDArray): image stack
        factor (int, optional): optional factor to multiply the mean value. Defaults to 1.

    Returns:
        int: returns a ceiled value of the mean
    """
    return np.ceil((images.sum() / images.size) * factor)
