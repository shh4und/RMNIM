import numpy as np

def normalize_image_int(image):
    np_image = np.array(image).astype('float32')
    min_val = np.min(np_image)
    max_val = np.max(np_image)
    
    # Normalizar para a faixa de 0 a 255
    np_image_normalized = 255 * (np_image - min_val) / (max_val - min_val)
    
    return np_image_normalized.astype('uint8')

def normalize_image_float(image):
    np_image = np.array(image).astype('float32') / 255.0
    return np_image

def create_spherical_strel(size):
    # Certifique-se de que o tamanho é ímpar para que haja um centro definido
    assert size % 2 == 1, "O tamanho deve ser um número ímpar para ter um centro definido."

    # Criar um array 3D de zeros
    strel = np.zeros((size, size, size), dtype=int)

    # Definir o centro
    center = size // 2
    radius = center

    # Preencher a esfera
    for x in range(size):
        for y in range(size):
            for z in range(size):
                # Calcular a distância do ponto (x, y, z) ao centro
                distance = np.sqrt((x - center) ** 2 + (y - center) ** 2 + (z - center) ** 2)
                if distance <= radius:
                    strel[x, y, z] = 1

    return strel

# # Exemplo de uso:
# size = 3
# spherical_strel = create_spherical_strel(size)
# print(spherical_strel)