import cv2
import numpy as np
from skimage.morphology import thin
from skimage import img_as_ubyte
from concurrent.futures import ThreadPoolExecutor

def segment(images, binaries):
    return np.array([cv2.bitwise_and(img, img, mask=bin) for img, bin in zip(images, binaries)])

def otsu_binary(images):
    return np.array([cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1] for img in images])

def simple_binary(images, n):
    return np.array([cv2.threshold(img, n, 255, cv2.THRESH_BINARY)[1] for img in images])

def morphological(img, op, shape_kernel, size_kernel, iter_num=None, kernel=None):
    if kernel is None:
        kernel = cv2.getStructuringElement(shape_kernel, size_kernel)
        if iter_num is None:
            return cv2.morphologyEx(img, op, kernel)
        else:
            return cv2.morphologyEx(img, op, kernel, iterations=iter_num)
    else:
        return cv2.morphologyEx(img, op, kernel)

def thinned(images, iter=1):
    return np.array([img_as_ubyte(thin(img, iter)) for img in images])

def skel_zhang_suen(images):
    return np.array([cv2.ximgproc.thinning(img) for img in images])

def mean_threshold(img, factor=1):
    return (img.sum() / img.size) * factor

# Exemplo de uso com paralelização para a função otsu_binary
def otsu_binary_parallel(images, num_threads=4):
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        return np.array(list(executor.map(otsu_binary, images)))

# Exemplo de uso com paralelização para a função simple_binary
def simple_binary_parallel(images, n, num_threads=4):
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        return np.array(list(executor.map(lambda img: simple_binary([img], n)[0], images)))
