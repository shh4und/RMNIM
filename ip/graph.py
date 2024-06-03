import collections
import heapq
import numpy as np


class Graph:
    """ A hash-table implementation of an undirected graph."""

    def __init__(self,image):
        # Map each voxel to a set of voxels connected to it
        self._neighbors = collections.defaultdict(set)
        self._parents = {}
        self.image = image
        self.shape = image.shape
        self.root = None
    def connect(self, voxel1, voxel2):
        self._neighbors[voxel1].add(voxel2)
        self._neighbors[voxel2].add(voxel1)
        self._parents[voxel2] = voxel1 # Set voxel1 as the parent of voxel2


    def neighbors(self, voxel):
        return self._neighbors[voxel]

    def get_26_neighbors(self, voxel):
        z, y, x = voxel
        for i in range(-1, 2):
            for j in range(-1, 2):
                for k in range(-1, 2):
                    if i == 0 and j == 0 and k == 0:
                        continue  # Skip the current voxel itself
                    new_z, new_y, new_x = z + i, y + j, x + k
                    if 0 <= new_z < self.shape[0] and 0 <= new_y < self.shape[1] and 0 <= new_x < self.shape[2]:
                        if self.image[new_z, new_y, new_x] == 255:
                            yield (new_z, new_y, new_x)
        

    

    def euclidean_distance(self, point1, point2):
        """
        This function calculates the Euclidean distance between two points in 3D space.

        Args:
            point1: A tuple or list containing the (z, y, x) coordinates of the first point.
            point2: A tuple or list containing the (z, y, x) coordinates of the second point.

        Returns:
            The Euclidean distance between the two points.
        """

        # Ensure both points have 3 coordinates
        if len(point1) != 3 or len(point2) != 3:
            raise ValueError("Points must have 3 coordinates (z, y, x).")

        z1, y1, x1 = point1
        z2, y2, x2 = point2

        # Calculate the squared differences for each dimension
        squared_differences = (x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2

        # Calculate the distance using the square root of the sum of squared differences
        distance = np.sqrt(squared_differences)

        return distance


    def edge_weight(self, voxel1, voxel2):
        return self.euclidean_distance(voxel1, voxel2)
        
    def set_root(self, root_voxel):
        """
        Set the root node of the graph.
        """
        self.root = root_voxel

    def get_root(self):
        return self.root

    def create_graph(self):
        for z in range(self.shape[0]):
            if self.image[z,:,:].sum() == 0:
                continue
            for y in range(self.shape[1]):
                for x in range(self.shape[2]):
                    if self.image[z, y, x] == 0:
                        continue
                    voxel = (z, y, x)
                    for neighbor in self.get_26_neighbors(voxel):
                        self.connect(voxel, neighbor)
    
    def dijkstra(self):
        """
        Implement Dijkstra's algorithm to find the shortest path from the root to all other voxels.
        """
        distances = {voxel: float('infinity') for voxel in self._neighbors}
        distances[self.root] = 0

        parents = {voxel: -1 for voxel in self._neighbors} # Parent of root is -1
        labels = {voxel: 0 for voxel in self._neighbors} # Initialize labels
        labels[self.root] = 1 # Root starts at 1
        next_label = 2 # Start labeling from 2 for the next nodes

        queue = [(0, self.root)]

        while queue:
            current_distance, current_voxel = heapq.heappop(queue)

            if current_distance > distances[current_voxel]:
                continue

            for neighbor in self._neighbors[current_voxel]:
                distance = current_distance + self.edge_weight(current_voxel, neighbor)

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    parents[neighbor] = current_voxel
                    labels[neighbor] = next_label # Assign the next available label
                    next_label += 1 # Increment the label for the next node
                    heapq.heappush(queue, (distance, neighbor))

        return distances, parents, labels
