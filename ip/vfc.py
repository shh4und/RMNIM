import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from skimage import feature
from scipy import ndimage
from skimage.util import img_as_ubyte, img_as_float
from scipy.signal import convolve2d
from scipy.spatial.distance import pdist, squareform
from concurrent.futures import ProcessPoolExecutor

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
    elif mode == "canny":
        for z in range(image3d.shape[0]):
            edge_map[z] = feature.canny(
                image3d[z], sigma=1.0, low_threshold=0.1, high_threshold=0.3
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


# def apply_vfc_3d(image, kx, ky):
#     # Assume image shape is (z,y,x)
#     z, y, x = image.shape

#     # Inicializar arrays de saída
#     fx = np.zeros_like(image, dtype=float)
#     fy = np.zeros_like(image, dtype=float)

#     # Aplicar convolução para cada fatia z
#     for z_slice in range(z):
#         # Convolução com kernel x
#         fx[z_slice] = convolve2d(image[z_slice], kx, mode="same", boundary="symm")

#         # Convolução com kernel y
#         fy[z_slice] = convolve2d(image[z_slice], ky, mode="same", boundary="symm")

#     return fx, fy


# def process_slice(args):
#     z_slice, image_slice, kx, ky = args
#     # Process single slice
#     fx_slice = convolve2d(image_slice, kx, mode="same", boundary="wrap")
#     fy_slice = convolve2d(image_slice, ky, mode="same", boundary="wrap")
#     return z_slice, fx_slice, fy_slice


# def apply_vfc_3d_parallel(image, kx, ky, num_processes=None):
#     z, y, x = image.shape

#     # Initialize output arrays
#     fx = np.zeros_like(image, dtype=float)
#     fy = np.zeros_like(image, dtype=float)

#     # Prepare arguments for parallel processing
#     args = [(i, image[i], kx, ky) for i in range(z)]

#     # Process slices in parallel
#     with Pool(processes=num_processes) as pool:
#         results = pool.map(process_slice, args)

#     # Reorganize results
#     for z_slice, fx_slice, fy_slice in results:
#         fx[z_slice] = fx_slice
#         fy[z_slice] = fy_slice

#     return fx, fy


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


def medialness(image3d, edge_map_mode, kernel_size=4, sigma=3.0, num_processes=None, chunk_size=4):
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


def scale_space_medialness(image, edge_map_mode, kernel_size, scale_space, num_processes, chunk_size):
    medialness_result = np.zeros_like(image, dtype=float)
    for sigma in scale_space:
        current_medialness = medialness(image, edge_map_mode, kernel_size, sigma, num_processes, chunk_size)
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
    footprint[order, order, order] = 0

    filtered = ndimage.maximum_filter(data, footprint=footprint)
    mask_local_maxima = data > filtered
    coords = np.asarray(np.where(mask_local_maxima)).T
    values = data[mask_local_maxima]

    return coords, values


def connect_medial_points(coords, values, max_distance=10, angle_threshold=90):
    """
    Connect medial points into a graph based on distance and orientation.

    Parameters
    ----------
    coords : ndarray
        Coordinates of medial points (N x 3)
    values : ndarray
        Medialness values at those coordinates
    max_distance : float
        Maximum distance to connect points
    angle_threshold : float
        Maximum angle difference in degrees to connect points

    Returns
    -------
    nx.Graph
        Graph representing connected medial points
    """
    # Create graph
    G = nx.Graph()

    # Add nodes with their properties
    for i, (coord, val) in enumerate(zip(coords, values)):
        G.add_node(i, pos=coord, value=val)

    # Calculate pairwise distances
    distances = pdist(coords)
    dist_matrix = squareform(distances)

    # Connect points based on distance and orientation
    for i in range(len(coords)):
        for j in range(i + 1, len(coords)):
            dist = dist_matrix[i, j]
            v1 = coords[i]
            v2 = coords[j]
            if dist <= max_distance:
                # Calculate orientation vector between points
                dot_product = np.dot(v1, v2)
                magnitude_v1 = np.linalg.norm(v1)
                magnitude_v2 = np.linalg.norm(v2)
                # vec = coords[j] - coords[i]
                # Cálculo do cosseno do ângulo
                cos_theta = dot_product / (magnitude_v1 * magnitude_v2)
                # Cálculo do ângulo em radianos
                theta_rad = np.arccos(cos_theta) * 180 / np.pi

                # Converter para graus
                theta_deg = np.degrees(theta_rad)
                # angle = np.arctan2(vec[1], vec[2]) * 180 / np.pi

                # Add edge if angle difference is within threshold
                if abs(theta_deg) <= angle_threshold:
                    G.add_edge(i, j, weight=dist)

    return G


def visualize_medial_graph(image3d, graph):
    """
    Visualize the medial graph overlaid on the original image.
    Projects 3D coordinates to 2D for visualization.
    """
    plt.figure(figsize=(10, 10))

    # Show max projection of image
    proj = np.max(image3d, axis=0)
    plt.imshow(proj, cmap="gray")

    # Get 3D positions and convert to 2D by dropping z-coordinate
    pos_3d = nx.get_node_attributes(graph, "pos")
    pos_2d = {node: (pos[2], pos[1]) for node, pos in pos_3d.items()}  # Use y,x coords

    # Draw graph edges with 2D positions
    nx.draw_networkx_edges(graph, pos=pos_2d, edge_color="r", width=0.5)

    plt.axis("off")
    plt.show()


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
