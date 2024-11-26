import numpy as np
from skimage.util import img_as_ubyte, img_as_float
from scipy import ndimage
from scipy.signal import convolve2d


def create_edge_map(image3d):
    
    # Calcular gradientes usando Sobel
    sobely = ndimage.sobel(image3d, 1)
    sobelx = ndimage.sobel(image3d, 2)

    # Magnitude do gradiente
    edge_map = np.sqrt(sobelx**2 + sobely**2)
    
    # Normalizar para [0,1]
    edge_map = (edge_map - edge_map.min()) / (edge_map.max() - edge_map.min())
    
    return img_as_ubyte(edge_map)

def create_vfc_kernel(size, sigma=3.0):
    # Criar grid de coordenadas
    y, x = np.mgrid[-size//2:size//2+1, -size//2:size//2+1]
    
    # Calcular r
    r = np.sqrt(x**2 + y**2)
    r[r == 0] = 1e-8  # Evitar divisão por zero
    
    # Calcular termo exponencial
    exp_term = np.exp(-r**2 / (sigma**2))
    
    # Calcular componentes do vetor
    kx = exp_term * (-x/r)
    ky = exp_term * (-y/r)
    
    # Normalizar
    magnitude = np.sqrt(kx**2 + ky**2)
    max_mag = magnitude.max()
    
    if max_mag != 0:
        kx = kx / max_mag
        ky = ky / max_mag
        
    return kx, ky

def apply_vfc_3d(image, kx, ky):
    # Assume image shape is (z,y,x)
    z, y, x = image.shape
    
    # Inicializar arrays de saída
    fx = np.zeros_like(image, dtype=float)
    fy = np.zeros_like(image, dtype=float)
    
    # Aplicar convolução para cada fatia z
    for z_slice in range(z):
        # Convolução com kernel x
        fx[z_slice] = convolve2d(
            image[z_slice], 
            kx,
            mode='same',
            boundary='symm'
        )
        
        # Convolução com kernel y
        fy[z_slice] = convolve2d(
            image[z_slice],
            ky,
            mode='same',
            boundary='symm'
        )
    
    return fx, fy

def medialness(image3d, kernel_size=4, sigma=3.0):
    edge_map = create_edge_map(image3d)
    kx, ky = create_vfc_kernel(kernel_size, sigma)
    fx, fy = apply_vfc_3d(image3d, kx, ky)

    # Magnitude do campo vetorial
    magnitude = np.sqrt(fx**2 + fy**2)
    
    # normilize to [0,1]
    normalize_magnitude =( np.absolute(magnitude) - np.min(magnitude) ) / ( np.max(magnitude) - np.min(magnitude) )
    
    medial_axis = 1 - normalize_magnitude
    return medial_axis

def scale_space_medialness(image, scale_space):
    medialness_result = np.zeros_like(image, dtype=float)
    space_norm = np.sqrt(np.power(scale_space, 2).sum())
    for sigma in scale_space:
        medialness_result += img_as_float(medialness(image, 4, sigma))

    medialness_result = 1/space_norm * medialness_result

    return img_as_float(medialness_result)


# From: https://stackoverflow.com/questions/55453110/how-to-find-local-maxima-of-3d-array-in-python
def local_maxima_3D(data, order=1):
    """Detects local maxima in a 3D array

    Parameters
    ---------
    data : 3d ndarray
    order : int
        How many points on each side to use for the comparison

    Returns
    -------
    coords : ndarray
        coordinates of the local maxima
    values : ndarray
        values of the local maxima
    """
    size = 1 + 2 * order
    footprint = np.ones((size, size, size))
    footprint[order, order, order] = 0

    filtered = ndimage.maximum_filter(data, footprint=footprint)
    mask_local_maxima = data > filtered
    coords = np.asarray(np.where(mask_local_maxima)).T
    values = data[mask_local_maxima]

    return coords, values
