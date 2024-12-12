from typing import Tuple, Union
from math import sin, cos, atan2, sqrt, pi
import numpy as np


Number = Union[int, float]
Vector = Tuple[Number, Number, Number]


def distance(a: Vector, b: Vector) -> Number:
    """Returns the distance between two cartesian points."""
    x = (b[0] - a[0]) ** 2
    y = (b[1] - a[1]) ** 2
    z = (b[2] - a[2]) ** 2
    return (x + y + z) ** 0.5

  
def magnitude(x: Number, y: Number, z: Number) -> Number:
    """Returns the magnitude of the vector."""
    return sqrt(x * x + y * y + z * z)


def to_spherical(x: Number, y: Number, z: Number) -> Vector:
    """Converts a cartesian coordinate (x, y, z) into a spherical one (radius, theta, phi)."""
    radius = magnitude(x, y, z)
    
    if x > 0:
       phi = atan2(y, x)
    elif x < 0 and y >= 0:
        phi = atan2(y, x) + pi
    elif x < 0 and y < 0:
        phi = atan2(y, x) - pi
    elif x == 0 and y > 0:
        phi = pi/2
    elif x == 0 and y < 0:
        phi = -(pi/2)
    
    if z > 0:
        theta = atan2(sqrt(x * x + y * y), z)
    elif z < 0:
        theta = atan2(sqrt(x * x + y * y), z) + pi
    elif z == 0 and sqrt(x * x + y * y) != 0:
        theta = pi/2
    
    return (radius, theta, phi)


def to_cartesian(radius: Number, theta: Number, phi: Number) -> Vector:
    """Converts a spherical coordinate (radius, theta, phi) into a cartesian one (x, y, z)."""
    x = radius * cos(phi) * sin(theta)
    y = radius * sin(phi) * sin(theta)
    z = radius * cos(theta)
    return (x, y, z)


def iterate_spherical(volume: np.ndarray):
    """Iterate through 3D volume using spherical coordinates.
    
    Args:
        volume (np.ndarray): 3D image stack with shape (Z,Y,X)
    
    Yields:
        tuple: (r, theta, phi, value, (z,y,x))
        where:
        - r: radius from origin
        - theta: azimuthal angle in x-y plane from x-axis (0 to 2π)
        - phi: polar angle from z-axis (0 to π)
        - value: pixel value at that point
        - (z,y,x): original cartesian coordinates
    """
    # Get volume dimensions
    depth, height, width = volume.shape
    
    # Calculate center point
    center_z = depth // 2
    center_y = height // 2
    center_x = width // 2
    
    for z in range(depth):
        for y in range(height):
            for x in range(width):
                # Convert to centered coordinates
                z_rel = z - center_z
                y_rel = y - center_y
                x_rel = x - center_x
                
                # Calculate spherical coordinates
                r = np.sqrt(x_rel**2 + y_rel**2 + z_rel**2)
                theta = np.arccos(z_rel/r) if r > 0 else 0 # polar angle
                phi = np.arctan2(y_rel, x_rel) # azimuthal angle
                
                yield (r, theta, phi, volume[z,y,x], (z,y,x))

# Usage example:
"""
images = load_tif_stack(folder_path)

# Iterate through volume in spherical coordinates
for r, theta, phi, value, (z,y,x) in iterate_spherical(images):
    if value > threshold: # Example condition
        print(f"Found bright point at r={r:.2f}, θ={theta:.2f}, φ={phi:.2f}")
        print(f"Cartesian coordinates: z={z}, y={y}, x={x}")
"""