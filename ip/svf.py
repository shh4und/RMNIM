import numpy as np

def cartesian_to_spherical(x, y, z):
    rho = np.sqrt(x**2 + y**2 + z**2)
    phi = np.arctan2(y, x)
    theta = np.arccos(z / rho)
    return rho, phi, theta

def calculate_vci(gradient_vector, direction_vector):
    norm_gradient = np.linalg.norm(gradient_vector)
    norm_direction = np.linalg.norm(direction_vector)
    
    if norm_gradient == 0 or norm_direction == 0:
        return 0  # ou algum valor apropriado para o seu caso
    
    cos_phi = np.dot(gradient_vector, direction_vector) / (norm_gradient * norm_direction)
    return cos_phi

def sliding_volume_filter(image, Rmin, Rmax, d, L):
    M = 2 * L**2
    output_image = np.zeros_like(image)
    gradient = np.gradient(image)
    
    for x in range(image.shape[0]):
        for y in range(image.shape[1]):
            for z in range(image.shape[2]):
                sum_vci = 0
                for a in np.linspace(0, 2*np.pi, 2*L):
                    for b in np.linspace(0, np.pi, L):
                        max_vci = 0
                        for r in np.linspace(Rmin, Rmax, int((Rmax-Rmin)/d)):
                            vci_sum = 0
                            for q in np.linspace(r-d/2, r+d/2, int(d)):
                                qx = q * np.sin(b) * np.cos(a)
                                qy = q * np.sin(b) * np.sin(a)
                                qz = q * np.cos(b)
                                gradient_vector = [gradient[0][x, y, z], gradient[1][x, y, z], gradient[2][x, y, z]]
                                direction_vector = [qx, qy, qz]
                                vci_sum += calculate_vci(gradient_vector, direction_vector)
                            max_vci = max(max_vci, vci_sum / (d + 1))
                        sum_vci += max_vci
                output_image[x, y, z] = sum_vci / M
    return output_image