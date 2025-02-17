import numpy as np
from scipy import ndimage
from skimage.util import img_as_ubyte, img_as_float
from scipy.signal import convolve2d
from concurrent.futures import ProcessPoolExecutor
import cv2 as cv
from functools import partial
from scipy.ndimage import sobel

import numpy as np

def create_sphere(O, rad, L):
    """
    Cria uma região de suporte esférica em torno do ponto O com raio rad.
    :param O: Centro da esfera (x, y, z)
    :param rad: Raio da esfera
    :param L: Número de divisões angulares (determina a discretização)
    :return: Lista de pontos (x, y, z) na esfera de suporte
    """
    # Coordenadas esféricas discretizadas
    alpha = np.linspace(0, 2 * np.pi, 2 * L)  # Ângulo azimutal (0 a 2pi)
    beta = np.linspace(0, np.pi, L)           # Ângulo polar (0 a pi)

    points = []
    for a in alpha:
        for b in beta:
            # Convertendo de coordenadas esféricas para cartesianas
            x = int(O[0] + rad * np.sin(b) * np.cos(a))
            y = int(O[1] + rad * np.sin(b) * np.sin(a))
            z = int(O[2] + rad * np.cos(b))

            # Adiciona o ponto discreto
            points.append((x, y, z))
    
    # Remove duplicatas e mantém os pontos dentro de limites válidos
    points = list(set(points))
    return points

def voxelConvergenceIndex(O, Q, imageGradient):
    # O é o ponto central (x, y, z)
    # Q é o ponto atual (x, y, z)
    # imageGradient é um array 3D contendo os gradientes em cada voxel
    
    # Vetor QO
    QO = np.array(O) - np.array(Q)
    
    # Gradiente no ponto Q
    grad_Q = np.array(imageGradient[Q[0], Q[1], Q[2]])
    
    # Ângulo entre QO e grad_Q
    cos_phi = np.dot(QO, grad_Q) / (np.linalg.norm(QO) * np.linalg.norm(grad_Q) + 1e-6)  # Evita divisão por zero
    return cos_phi

def slidingVolumeFilter(O, imageGradient, rad, d, L, Rmin, Rmax):
    """
    Calcula o Sliding Volume Filter (SVF) em torno do voxel O.
    :param O: Centro do voxel (coordenadas x, y, z)
    :param imageGradient: Gradiente da imagem (array 3D com vetores gradientes)
    :param rad: Raio da região de suporte esférica
    :param d: Espessura do volume deslizante
    :param L: Número de divisões angulares
    :param Rmin: Raio mínimo para as linhas radiais
    :param Rmax: Raio máximo para as linhas radiais
    :return: Valor do SVF para o voxel O
    """
    SVF_O = 0
    M = 2 * L**2  # Número total de linhas radiais

    # Cria a região de suporte esférica
    support_region = create_sphere(O, rad, L)

    for point in support_region:
        # Calcule o VCI para os pontos da região de suporte
        vci_values = []

        for r in np.linspace(Rmin, Rmax, d//2):  # Pega valores ao longo do intervalo radial
            Qx = int(O[0] + r * (point[0] - O[0]) / rad)
            Qy = int(O[1] + r * (point[1] - O[1]) / rad)
            Qz = int(O[2] + r * (point[2] - O[2]) / rad)
            Q = (Qx, Qy, Qz)

            if 0 <= Q[0] < imageGradient.shape[0] and \
               0 <= Q[1] < imageGradient.shape[1] and \
               0 <= Q[2] < imageGradient.shape[2]:
                vci_values.append(voxelConvergenceIndex(O, Q, imageGradient))

        # Cálculo da média deslizante dos valores de VCI
        sliding_values = []
        for i in range(len(vci_values) - d + 1):
            sliding_values.append(np.mean(vci_values[i:i + d]))

        if sliding_values:
            SVF_O += max(sliding_values)  # Soma o máximo valor deslizante

    SVF_O /= M  # Normaliza pelo número total de linhas radiais
    return SVF_O

def sobel_gradient(img):
    # Suponha que img seja uma imagem 2D ou volume 3D
    dx = sobel(img, axis=0)  # Derivada em x
    dy = sobel(img, axis=1)  # Derivada em y
    dz = sobel(img, axis=2) if img.ndim == 3 else None  # Derivada em z (se 3D)

    # Gradiente e magnitude
    magnitude = np.sqrt(dx**2 + dy**2 + (dz**2 if dz is not None else 0))

    return img_as_float(magnitude)


from concurrent.futures import ProcessPoolExecutor
import numpy as np

def calculate_chunk_svf(chunk_data, params):
    chunk, start_idx = chunk_data
    rad, d, L, Rmin, Rmax = params['rad'], params['d'], params['L'], params['Rmin'], params['Rmax']
    svf_chunk = np.zeros_like(chunk, dtype=np.float32)
    
    for z in range(chunk.shape[0]):
        for y in range(chunk.shape[1]):
            for x in range(chunk.shape[2]):
                O = (x, y, z + start_idx)
                svf_value = slidingVolumeFilter(O, chunk, rad, d, L, Rmin, Rmax)
                svf_chunk[z, y, x] = svf_value
    
    return svf_chunk, start_idx

def calculate_svf_volume_parallel(image, rad, d, L, Rmin, Rmax, num_processes=4):
    svf_volume = np.zeros_like(image, dtype=np.float32)
    chunk_size = max(1, image.shape[0] // num_processes)
    chunks = [(image[i:i + chunk_size], i) for i in range(0, image.shape[0], chunk_size)]
    params = {'rad': rad, 'd': d, 'L': L, 'Rmin': Rmin, 'Rmax': Rmax}
    
    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        results = list(executor.map(partial(calculate_chunk_svf, params=params), chunks))
    
    for svf_chunk, start_idx in results:
        svf_volume[start_idx:start_idx + svf_chunk.shape[0]] = svf_chunk
    
    return svf_volume


# def calculate_svf_volume(image, rad, d, L, Rmin, Rmax):
#     """
#     Calcula o volume de valores SVF para toda a imagem.
#     :param image: Array 3D da imagem original.
#     :param rad: Raio da região de suporte esférica.
#     :param d: Espessura do volume deslizante.
#     :param L: Número de divisões angulares para a discretização.
#     :param Rmin: Raio mínimo para a região deslizante.
#     :param Rmax: Raio máximo para a região deslizante.
#     :return: Array 3D com os valores de SVF para cada voxel.
#     """
#     svf_volume = np.zeros_like(image, dtype=np.float32)  # Inicializa o volume SVF

#     # # Gradiente da imagem (usado no cálculo de VCI)
#     # image_gradient = np.gradient(image.astype(np.float32))

#     # Itera sobre todos os voxels da imagem
#     for z in range(image.shape[0]):
#         for y in range(image.shape[1]):
#             for x in range(image.shape[2]):
#                 # Define o voxel central (O)
#                 O = (x, y, z)

#                 # Calcula o SVF para este voxel
#                 svf_value = slidingVolumeFilter(O, image, rad, d, L, Rmin, Rmax)
#                 svf_volume[x, y, z] = svf_value

#     return svf_volume


def enhance_intensity_with_svf(original_image, svf_volume):
    """
    Realça a intensidade de cada voxel na imagem original usando os valores de SVF.
    :param original_image: Array 3D representando a intensidade original (I(p)).
    :param svf_volume: Array 3D representando os valores de SVF calculados para cada voxel.
    :return: Array 3D representando a nova intensidade após o realce com SVF.
    """
    # Garantir que os tamanhos das matrizes sejam consistentes
    assert original_image.shape == svf_volume.shape, "As dimensões da imagem original e do SVF devem ser iguais."

    # Aplica a fórmula para cada voxel
    enhanced_image = np.zeros_like(original_image, dtype=np.float32)  # Tipo float para evitar truncamento
    for x in range(original_image.shape[0]):
        for y in range(original_image.shape[1]):
            for z in range(original_image.shape[2]):
                # Intensidade original
                I_p = original_image[x, y, z]

                # Valor do SVF no ponto
                SVF_p = svf_volume[x, y, z]

                # Cálculo de ISVF(p)
                enhanced_intensity = 15 * np.sqrt(min(I_p * (1 + SVF_p), 255))
                enhanced_image[x, y, z] = enhanced_intensity

    return enhanced_image
