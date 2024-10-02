import numpy as np

def normalize_image_int(image: np.ndarray) -> np.ndarray:
    """Function to normalize a given image from float type range (0,1) to uint type range (0,255)

    Args:
        image (np.ndarray): given image

    Returns:
        np.ndarray: returns a normalized uint image
    """
    np_image = np.array(image).astype('float32')
    min_val = np.min(np_image)
    max_val = np.max(np_image)
    
    np_image_normalized = 255 * (np_image - min_val) / (max_val - min_val)
    
    return np_image_normalized.astype('uint8')

def normalize_image_float(image: np.ndarray) -> np.ndarray:
    """Function to normalize a given image from uint type range (0,255) to float type range (0,1)

    Args:
        image (np.ndarray): given image

    Returns:
        np.ndarray: returns a normalized float image
    """
    np_image = np.array(image).astype('float32') / 255.0
    return np_image

def create_spherical_strel(size: int) -> np.ndarray:
    """Function to create a spherical structuring element
    the size must be an odd number so that there is a defined center

    Args:
        size (odd int): size of the strel

    Returns:
        np.ndarray: returns a spherical structuring element of the given size
    """
    # Ensure the size is odd so that there is a defined center
    assert size % 2 == 1, "Size must be an odd number to have a defined center."

    # Create a 3D array of zeros
    strel = np.zeros((size, size, size), dtype=int)

    # Define the center
    center = size // 2
    radius = center

    # Fill the sphere
    for x in range(size):
        for y in range(size):
            for z in range(size):
                # Calculate the distance from point (x, y, z) to the center
                distance = np.sqrt((x - center) ** 2 + (y - center) ** 2 + (z - center) ** 2)
                if distance <= radius:
                    strel[x, y, z] = 1

    return strel

def remove_zero_slices(image :np.ndarray) -> np.ndarray:
    
    """Function to remove zero value slices from the image stack
    
    Args:
        image (np.ndarray): given 3D stack image

    Returns:
        np.ndarray: returns a 3D stack image with only non-zero slices
    """
    
    # Supondo que sua imagem seja um array chamado 'image'
    non_zero_slices = np.sum(image, axis=(1, 2)) != 0
    # invert boolean array to select only non-zero slices
    keep_slices = ~non_zero_slices

    # use np.delete to keep non-zero slices
    result = np.delete(image, np.where(keep_slices), axis=0)
    
    return result