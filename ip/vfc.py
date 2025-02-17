import numpy as np
from scipy import ndimage
from skimage.util import img_as_ubyte, img_as_float
from scipy.signal import convolve2d
from concurrent.futures import ProcessPoolExecutor
import cv2 as cv


def convolve3d(image3d: np.ndarray, kernel):
    # check if the image is 3d
    if image3d.ndim != 3:
        print("The image needs to be 3D and (z,y,x) shape")
        return
    convolved_image = np.zeros_like(image3d, image3d.dtype)
    z, _, _ = image3d.shape
    for zi in range(z):
        convolved_image[zi] = convolve2d(
            image3d[zi], kernel, mode="same", boundary="symm"
        )

    return convolved_image


def create_edge_map(image3d, mode="sobel"):
    edge_map = np.zeros_like(image3d)
    if mode == "sobel":
        image3d = img_as_float(image3d)
        # Calcular gradientes usando Sobel
        # sobelz = ndimage.sobel(image3d, 0)
        sobely = ndimage.sobel(image3d, 1)
        sobelx = ndimage.sobel(image3d, 2)

        # Magnitude do gradiente
        edge_map = np.sqrt(sobelx**2 + sobely**2)  # + sobelz**2

        # Normalizar para [0,1]
        edge_map = (edge_map - edge_map.min()) / (edge_map.max() - edge_map.min())
    # elif mode == "canny":
    #     for z in range(image3d.shape[0]):
    #         edge_map[z] = feature.canny(
    #             image3d[z], low_threshold=0.1, high_threshold=0.2
    #         )
    elif mode == "canny":
        image3d = img_as_ubyte(image3d)
        for z in range(image3d.shape[0]):
            edge_map[z] = cv.Canny(
                image3d[z], int(255 * 0.1), int(255 * 0.3), L2gradient=True
            )
    elif mode == "prewitt":
        prewitt_x = ndimage.prewitt(image3d, axis=1)
        prewitt_y = ndimage.prewitt(image3d, axis=2)
        edge_map = np.sqrt(prewitt_x**2 + prewitt_y**2)
        edge_map = (edge_map - edge_map.min()) / (edge_map.max() - edge_map.min())

    elif mode == "laplace":
        laplacian = ndimage.laplace(image3d)
        edge_map = np.abs(laplacian)
        edge_map = (edge_map - edge_map.min()) / (edge_map.max() - edge_map.min())

    elif mode == "roberts":
        pass

    else:
        print("choose one of the provided modes")

    return img_as_float(edge_map)


def create_vfc_kernel(size, sigma=3.0):
    # Criar grid de coordenadas
    y, x = np.mgrid[-size // 2 : size // 2 + 1, -size // 2 : size // 2 + 1]

    # Calcular r
    r = np.sqrt(x**2 + y**2)
    r[r == 0] = 1e-8  # Evitar divisão por zero

    # Calcular termo exponencial
    exp_term = np.exp(-(r**2) / (sigma**2))

    # Calcular componentes do vetor
    kx = exp_term * (-x / r)
    ky = exp_term * (-y / r)

    # Normalizar
    magnitude = np.sqrt(kx**2 + ky**2)
    max_mag = magnitude.max()

    if max_mag != 0:
        kx = kx / max_mag
        ky = ky / max_mag

    return kx, ky


def process_chunk(chunk_data):
    chunk, kx, ky = chunk_data
    fx_chunk = np.zeros_like(chunk)
    fy_chunk = np.zeros_like(chunk)

    # Process multiple slices at once using vectorization
    for i in range(len(chunk)):
        fx_chunk[i] = convolve2d(chunk[i], kx, mode="same", boundary="wrap")
        fy_chunk[i] = convolve2d(chunk[i], ky, mode="same", boundary="wrap")

    return fx_chunk, fy_chunk


def apply_vfc_3d_parallel_improved(image, kx, ky, num_processes=None, chunk_size=4):
    """
    Improved parallel VFC computation with chunking

    Args:
        image: 3D input array (z,y,x)
        kx, ky: VFC kernels
        num_processes: Number of processes to use
        chunk_size: Number of slices per chunk
    """
    z, y, x = image.shape

    # Create chunks
    chunks = [image[i : i + chunk_size] for i in range(0, z, chunk_size)]
    chunk_args = [(chunk, kx, ky) for chunk in chunks]

    # Initialize output arrays
    fx = np.zeros_like(image, dtype=float)
    fy = np.zeros_like(image, dtype=float)

    # Process chunks in parallel
    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        results = list(executor.map(process_chunk, chunk_args))

    # Reconstruct output
    current_z = 0
    for fx_chunk, fy_chunk in results:
        chunk_depth = fx_chunk.shape[0]
        fx[current_z : current_z + chunk_depth] = fx_chunk
        fy[current_z : current_z + chunk_depth] = fy_chunk
        current_z += chunk_depth

    return fx, fy


def medialness(
    image3d, edge_map_mode, kernel_size=4, sigma=3.0, num_processes=None, chunk_size=4
):
    edge_map = create_edge_map(image3d, edge_map_mode)
    kx, ky = create_vfc_kernel(kernel_size, sigma)
    fx, fy = apply_vfc_3d_parallel_improved(edge_map, kx, ky, num_processes, chunk_size)

    # Calculate vector field magnitude
    magnitude = np.linalg.norm(np.stack([fx, fy]), axis=0)

    # Normalize to [0,1]
    normalize_magnitude = (magnitude - magnitude.min()) / (
        magnitude.max() - magnitude.min()
    )

    medial_axis = 1 - normalize_magnitude
    return img_as_float(medial_axis)


def scale_space_medialness(
    image, edge_map_mode, kernel_size, scale_space, num_processes, chunk_size
):
    medialness_result = np.zeros_like(image, dtype=float)
    for sigma in scale_space:
        current_medialness = medialness(
            image, edge_map_mode, kernel_size, sigma, num_processes, chunk_size
        )
        medialness_result = np.maximum(medialness_result, current_medialness)

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
    # footprint=ndimage.generate_binary_structure(size, 1)
    footprint[order, order, order] = 0

    filtered = ndimage.maximum_filter(data, footprint=footprint)
    mask_local_maxima = data > filtered

    coords = np.asarray(np.where(mask_local_maxima)).T
    values = data[mask_local_maxima]

    return coords, values


# More efficient way
def create_maxima_image(coords, shape):
    """
    Creates binary image from coordinates

    Args:
        coords: Nx3 array of coordinates
        shape: Shape of output image (z,y,x)
    """
    img = np.zeros(shape, dtype=np.uint8)
    # Convert coordinates to tuple of index arrays
    indices = tuple(coords.T)  # Transpose to get separate x,y,z arrays
    img[indices] = 255
    return img_as_ubyte(img)
