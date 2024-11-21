import numpy as np
from multiprocessing import Pool
from functools import partial
from scipy.ndimage import gaussian_filter
import concurrent.futures
from ip.ios import *
def calculate_chunk_svf(chunk_data, params):
    """Process a chunk of the volume with (z,y,x) format"""
    chunk, start_idx = chunk_data
    rad, L, d = params['rad'], params['L'], params['d']
    
    # Pre-compute angles
    alpha = np.linspace(0, 2*np.pi, 2*L)
    beta = np.linspace(0, np.pi, L)
    
    # Calculate gradients for chunk
    gradients = np.array(np.gradient(gaussian_filter(chunk, sigma=1.0)))
    
    result = np.zeros_like(chunk)
    shape = chunk.shape  # (z,y,x)
    
    # Prepare meshgrid for directions
    r_positions = np.arange(d/2, rad, d)
    
    # Pre-compute trigonometric values
    sin_beta = np.sin(beta)
    cos_beta = np.cos(beta)
    sin_alpha = np.sin(alpha)
    cos_alpha = np.cos(alpha)
    
    for z in range(shape[0]):
        for y in range(shape[1]):
            for x in range(shape[2]):
                if z < gradients.shape[1] and y < gradients.shape[2] and x < gradients.shape[3]:
                    current_gradients = gradients[:, z, y, x]
                    
                    # Reshape current_gradients for broadcasting
                    current_gradients = current_gradients.reshape(3, 1, 1, 1)
                    
                    # Calculate directions for all positions at once
                    directions = np.zeros((3, len(r_positions), len(beta), len(alpha)))
                    
                    for i, r in enumerate(r_positions):
                        for j, b in enumerate(beta):
                            for k, a in enumerate(alpha):
                                directions[0, i, j, k] = r * sin_beta[j] * cos_alpha[k]
                                directions[1, i, j, k] = r * sin_beta[j] * sin_alpha[k]
                                directions[2, i, j, k] = r * cos_beta[j]
                    
                    # Normalize directions
                    norm = np.linalg.norm(directions, axis=0) + 1e-10
                    directions /= norm[np.newaxis, :, :, :]
                    
                    # Calculate VCI with proper broadcasting
                    vci = np.sum(directions * current_gradients, axis=0)
                    result[z, y, x] = np.mean(np.max(vci, axis=0))
    
    return result, start_idx

def parallel_svf(volume, rad=5, L=8, d=2, n_processes=4):
    """Main function with improved chunk handling"""
    # Ensure volume is numpy array
    volume = np.array(volume)
    
    # Calculate optimal chunk size
    chunk_size = max(1, volume.shape[0] // n_processes)
    chunks = []
    
    # Create chunks with proper bounds checking
    for i in range(0, volume.shape[0], chunk_size):
        end = min(i + chunk_size, volume.shape[0])
        chunks.append((volume[i:end], i))
    
    params = {'rad': rad, 'L': L, 'd': d}
    
    with concurrent.futures.ProcessPoolExecutor(max_workers=n_processes) as executor:
        results = list(executor.map(partial(calculate_chunk_svf, params=params), chunks))
    
    final_result = np.zeros_like(volume)
    for chunk_result, start_idx in results:
        end_idx = start_idx + chunk_result.shape[0]
        final_result[start_idx:end_idx] = chunk_result
    
    return final_result
# Usage example
if __name__ == '__main__':
    # Create sample volume
    #test_volume = np.random.rand(100, 100, 100)
    folder_path = "./OlfactoryProjectionFibers/ImageStacks/OP_1"

    images = load_tif_stack(folder_path)
    # Process with parallel SVF
    result = parallel_svf(images, n_processes=4)