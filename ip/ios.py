import cv2
import numpy as np
import os
import re
from ip.utils import *

def load_tif_stack(folder:str) -> np.ndarray:
    """Function to load and order the images by its filename from an image stack folder
    (with .tif extension)

    Args:
        folder (str): stack directory path name

    Returns:
        np.ndarray: an ordered stack 
    """
    images = []
    tiff_files = sorted([f for f in os.listdir(folder) if re.match(r".*\.tif$", f)], key=lambda x: int(re.findall(r"\d+", x)[0]))
    for filename in tiff_files:
        filepath = os.path.join(folder, filename)
        if os.path.exists(filepath):
            img = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
            if img is not None:
                images.append(img)
        else:
            print(f"File {filename} does not exist.")
    return np.stack(images, axis=0)

def cv2_imshow(imgs):
    if len(np.array(imgs).shape) < 3:
        stack3d = np.array([imgs])
    else:
        stack3d = imgs
    x = 1
    for img in stack3d:
        cv2.imshow(f"img 0{x}", img)
        x+=1
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return True

def blended(imgs, proportion=False):
    if proportion:
        N = len(imgs)   
        weight = 1.0 / N 

        blend_img = normalize_image_float(imgs[0]) * weight
        for img in imgs[1:]:
            img = normalize_image_float(img)
            blend_img = cv2.addWeighted(blend_img, 1.0, img, weight, 0)
        blend_img = normalize_image_int(blend_img)
    else:
        blend_img = imgs[0]
        for img in imgs[1:]:
            blend_img = cv2.addWeighted(blend_img, 1, img, 1, 0)
    return blend_img

def single_download(image:np.ndarray, path:str) -> bool:
    """Function to download a single image

    Args:
        image (np.ndarray): a given image
        path (str): path where to downloaded the image

    Returns:
        bool: confirms if succesfully downloaded
    """
    return cv2.imwrite(path, image)

def download(images:np.ndarray, path:str) -> bool:
    """Function to download a whole image stack
    if it fails, it will show which index it fails at 
    Args:
        images (np.ndarray): a given image stack
        path (str): path where to downloaded the stack

    Returns:
        bool: returns True if successfully downloaded
    """
    if not os.path.exists(path):
        os.makedirs(path)
        print("Path created.")
    for idx, img in enumerate(images):
        if not cv2.imwrite(os.path.join(path, f"{idx+1}.tif"), img):
            print(f"Error at index: {idx}")
            return False
    return True
