import networkx as nx
import numpy as np
from ip.binary import *

class Graph:
    def __init__(self, image):
        self.graph = nx.Graph()
        self.image = image
        self.shape = image.shape
        self.root = None
        self.node_id = 1  # Starting ID for nodes

    def add_edge_with_weight(self, voxel1, voxel2):
        weight = self.euclidean_distance(voxel1, voxel2)
        self.graph.add_edge(voxel1, voxel2, weight=weight)

    def euclidean_distance(self, point1, point2):
        z1, y1, x1 = point1
        z2, y2, x2 = point2
        squared_differences = (x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2
        distance = np.sqrt(squared_differences)
        return distance

    def create_graph(self):
        for z in range(self.shape[0]):
            if self.image[z,:,:].sum() == 0:
                print(f"skipped image{z}")
                continue
            for y in range(self.shape[1]):
                if self.image[z,y,:].sum() == 0:
                    continue
                    print(f"skipped {z}{y}")
                for x in range(self.shape[2]):
                    if self.image[z, y, x] == 0:
                        continue
                    voxel = (z, y, x)
                    for neighbor in self.get_26_neighbors(voxel):
                        self.add_edge_with_weight(voxel, neighbor)

    def get_26_neighbors(self, voxel):
        z, y, x = voxel
        for i in range(-1, 2):  # Iterate over the 3x3x3 neighborhood
            for j in range(-1, 2):
                for k in range(-1, 2):
                    if i == 0 and j == 0 and k == 0:
                        continue  # Skip the center voxel itself
                    new_z, new_y, new_x = z + i, y + j, x + k
                    # Check if the new coordinates are within the image bounds
                    if 0 <= new_z < self.shape[0] and 0 <= new_y < self.shape[1] and 0 <= new_x < self.shape[2]:
                        # Check if the voxel at the new coordinates is white
                        if self.image[new_z, new_y, new_x] == 255:
                            yield (new_z, new_y, new_x)

    def set_root(self, root_voxel):
        self.root = root_voxel

    def get_root(self):
        return self.root

    def get_mst(self):
        mst = nx.minimum_spanning_tree(self.graph)
        return mst

    def apply_dijkstra_and_label_nodes(self):
        mst = self.get_mst()
        distances, paths = nx.single_source_dijkstra(mst, source=self.root, cutoff=None, weight='weight')

        # Atualizando os nós com identidades e identidades dos pais
        for node, path in enumerate(paths.values()):
            for index, voxel in enumerate(path):
                if index == 0:
                    parent_id = -1  # Raiz tem parent_id como -1
                else:
                    parent_id = self.graph.nodes[path[index - 1]]['identity']
                
                if 'identity' not in self.graph.nodes[voxel]:
                    self.graph.nodes[voxel]['identity'] = self.node_id
                    self.node_id += 1
                
                self.graph.nodes[voxel]['parent'] = parent_id

        return distances, paths

    def save_to_swc(self, filename):
        ordered_nodes = sorted((node for node, attrs in self.graph.nodes(data=True) if 'identity' in attrs),
                           key=lambda node_data: self.graph.nodes[node_data]['identity'])
        with open(filename, 'w') as f:
            for node in ordered_nodes:
                attrs = self.graph.nodes(data=True)[node]
                if 'identity' not in attrs:
                    continue
                z,y,x = node
                f.write(f"{attrs['identity']} 2 {x} {y} {z} 1 {attrs['parent']}\n")