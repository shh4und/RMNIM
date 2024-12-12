import numpy as np
from scipy import ndimage

def estimate_noise_level(image):
    """
    Estimates noise level in a grayscale image using multiple metrics.
    Returns a dict with different noise measurements.
    """
    metrics = {}
    
    # # 1. Basic statistical measures
    # metrics['std'] = np.std(image)  # Standard deviation
    # metrics['var'] = np.var(image)  # Variance
    
    # # 2. Local variance analysis
    # local_var = ndimage.uniform_filter(image**2, size=3) - ndimage.uniform_filter(image, size=3)**2
    # metrics['local_var_mean'] = np.mean(local_var)
    
    # # 3. Gradient-based measures
    # gz = ndimage.sobel(image, axis=0)
    # gy = ndimage.sobel(image, axis=1)
    # gx = ndimage.sobel(image, axis=2)
    # gradient_magnitude = np.sqrt(gx**2 + gy**2 + gz**2)
    # metrics['gradient_mean'] = np.mean(gradient_magnitude)
    
    # 4. Laplacian variance (good noise estimator)
    laplacian = ndimage.laplace(image)
    metrics['laplacian_var'] = np.var(laplacian)
    
    return metrics

def compare_noise_levels(image1, image2):
    """
    Compares noise levels between two images.
    Returns True if image1 is more noisy than image2.
    """
    metrics1 = estimate_noise_level(image1)
    metrics2 = estimate_noise_level(image2)
    
    # Weight and combine metrics
    noise_score1 = (metrics1['std'] * 0.2 + 
                   metrics1['local_var_mean'] * 0.3 +
                   metrics1['gradient_mean'] * 0.2 +
                   metrics1['laplacian_var'] * 0.3)
    
    noise_score2 = (metrics2['std'] * 0.2 + 
                   metrics2['local_var_mean'] * 0.3 +
                   metrics2['gradient_mean'] * 0.2 +
                   metrics2['laplacian_var'] * 0.3)
    
    return noise_score1 > noise_score2

# Example usage:

# # Get detailed metrics
# print("vol1")
# metrics = estimate_noise_level(volumeOP1)
# for key, value in metrics.items():
#     print(f"{key}: {value:.4f}")
# print("vol2")
# metrics = estimate_noise_level(volumeOP2)
# for key, value in metrics.items():
#     print(f"{key}: {value:.4f}")
# print("vol3")
# metrics = estimate_noise_level(volumeOP3)
# for key, value in metrics.items():
#     print(f"{key}: {value:.4f}")

# print("vol5")
# metrics = estimate_noise_level(volumeOP5)
# for key, value in metrics.items():
#     print(f"{key}: {value:.4f}")