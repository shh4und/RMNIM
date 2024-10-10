import networkx as nx
import numpy as np
from ip.swc import *
from typing import Tuple, Optional, List


class Graph:
    def __init__(self, image: np.ndarray):
        self.graph = nx.Graph()
        self.image = image
        self.shape = image.shape
        self.root: Tuple[float, float, float] = (0, 0, 0)

    def add_edge_with_weight(
        self, voxel1: Tuple[float, float, float], voxel2: Tuple[float, float, float]
    ):
        if not self.graph.has_edge(voxel1, voxel2):
            weight = self.euclidean_distance(voxel1, voxel2)
            self.graph.add_edge(voxel1, voxel2, weight=weight)

    def simple_moving_average(self, arr, window_size):
        # Separa os arrays individuais das triplas
        if len(arr) >= window_size:
            z, y, x = zip(*arr)

            # Calcula a média móvel simples para cada array
            z_sma = np.convolve(z, np.ones(window_size) / window_size, mode="valid")
            y_sma = np.convolve(y, np.ones(window_size) / window_size, mode="valid")
            x_sma = np.convolve(x, np.ones(window_size) / window_size, mode="valid")

            return arr + list(zip(z_sma, y_sma, x_sma))

        return arr

    def euclidean_distance(
        self, point1: Tuple[float, float, float], point2: Tuple[float, float, float]
    ) -> float:
        z1, y1, x1 = point1
        z2, y2, x2 = point2
        squared_diff_xy = (x2 - x1) ** 2 + (y2 - y1) ** 2  + (z2 - z1) ** 2
        distance_xy = np.sqrt(squared_diff_xy)
        return distance_xy

    def create_graph(
        self, moving_avg: bool = False, window_moving_avg_sz: int = 2
    ) -> None:

        non_zero_voxels = np.nonzero(self.image)  # Get indices of all non-zero voxels
        for z, y, x in zip(*non_zero_voxels):
            voxel = (z, y, x)
            neighborhood = self.get_26_neighborhood(voxel)

            if moving_avg:
                mov_avg = self.simple_moving_average(neighborhood, window_moving_avg_sz)
                for neighbor in mov_avg:
                    self.add_edge_with_weight(voxel, neighbor)
            else:
                for neighbor in neighborhood:
                    self.add_edge_with_weight(voxel, neighbor)

        print(">> Graph created")

    def get_26_neighborhood(
        self, voxel: Tuple[float, float, float]
    ) -> List[Tuple[int, int, int]]:
        z, y, x = map(int, voxel)
        neighbors = []

        for dz in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if dz == 0 and dy == 0 and dx == 0:
                        continue
                    nz, ny, nx = z + dz, y + dy, x + dx

                    if (
                        0 <= nz < self.shape[0]
                        and 0 <= ny < self.shape[1]
                        and 0 <= nx < self.shape[2]
                        and self.image[nz, ny, nx] != 0
                    ):
                        neighbors.append((nz, ny, nx))

        return neighbors

    def set_root(self, root_voxel: Tuple[float, float, float]) -> None:
        self.root = root_voxel

    def get_root(self) -> Tuple[float, float, float]:
        return self.root

    def get_mst(self) -> nx.Graph:
        mst = nx.minimum_spanning_tree(self.graph, weight="weight", algorithm="prim")
        print(">> Minimum Spanning Tree Generated")
        print(">> Minimum Spanning Tree length:", len(mst))
        return mst

    def apply_dfs_and_label_nodes(self) -> nx.Graph:
        # apply the dfs for labeling the nodes over the mst generated
        mst = self.get_mst()
        visited = set()  # Keep track of visited nodes
        stack = [(self.root, -1)]  # Initialize stack with root and parent_id -1
        node_id = 1  # Start ID assignment from 1, following the SWC pattern

        while stack:
            voxel, parent_id = stack.pop()
            if voxel not in visited:
                visited.add(voxel)
                if "id" not in mst.nodes[voxel]:
                    mst.nodes[voxel]["id"] = node_id
                    node_id += 1
                mst.nodes[voxel]["parent"] = parent_id
                # Add children to stack
                stack.extend(
                    (neighbor, mst.nodes[voxel]["id"])
                    for neighbor in mst.neighbors(voxel)
                )

        print(">> Depth-First search and labeling complete")
        return mst

    def save_to_swc(self, mst: nx.Graph, filename: str, width: float = 1.0) -> bool:
        swc = SWCFile(filename)
        mst_nodes_data = mst.nodes(data=True)
        for node, attrs in mst_nodes_data:
            if "id" not in attrs:
                continue
            z, y, x = node
            swc.add_point(attrs["id"], 9, x, y, z, width, attrs["parent"])

        return swc.write_file()
