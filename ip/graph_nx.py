import networkx as nx
import numpy as np
from ip.swc import *


class Graph:
    def __init__(self, image):
        self.graph = nx.Graph()
        self.image = image
        self.shape = image.shape
        self.root = (0,0,0)
    def add_edge_with_weight(self, voxel1, voxel2):
        if not self.graph.has_edge(voxel1, voxel2):
            weight = self.euclidean_distance(voxel1, voxel2)
            self.graph.add_edge(voxel1, voxel2, weight=weight)

    def euclidean_distance(self, point1, point2):
        z1, y1, x1 = point1
        z2, y2, x2 = point2
        squared_diff_xy = (x2 - x1) ** 2 + (y2 - y1) ** 2
        #squared_diff_z = (z2 - z1) ** 2
        distance_xy = np.sqrt(squared_diff_xy)
        #distance_z = np.sqrt(squared_diff_z)
        return distance_xy
    def create_graph(self):
        y = self.root[1]
        self.image[:,y+1,:] = 0
        non_zero_voxels = np.nonzero(self.image)  # Get indices of all non-zero voxels
        for z, y, x in zip(*non_zero_voxels):
            voxel = (z, y, x)
            for neighbor in self.get_26_neighborhood(voxel):
                nz, ny, nx = neighbor
                # Check if the voxel at the new coordinates is foreground
                if (
                    0 <= nz < self.shape[0]
                    and 0 <= ny < self.shape[1]
                    and 0 <= nx < self.shape[2]
                    and self.image[nz, ny, nx] != 0
                ):
                    self.add_edge_with_weight(voxel, neighbor)
        
        print(">> Graph created")

    def get_26_neighborhood(self, voxel):
        # returns a list of all possible neighbors of voxel
        z, y, x = voxel
        z0, y0, x0 = self.root
        if z == z0 and y == y0 and x == x0:
            print("essa eh a raiz")
            return [
            (z + 1, y, x),
            (z - 1, y, x),
            (z, y - 1, x),
            (z, y, x + 1),
            (z, y, x - 1),
            (z + 1, y - 1, x),
            (z - 1, y - 1, x),
            (z + 1, y, x + 1),
            (z + 1, y, x - 1),
            (z - 1, y, x + 1),
            (z - 1, y, x - 1),
            (z, y - 1, x + 1),
            (z, y - 1, x - 1),
            (z + 1, y - 1, x + 1),
            (z + 1, y - 1, x - 1),
            (z - 1, y - 1, x + 1),
            (z - 1, y - 1, x - 1),
        ]
        else:
            return [
                (z + 1, y, x),
                (z - 1, y, x),
                (z, y + 1, x),
                (z, y - 1, x),
                (z, y, x + 1),
                (z, y, x - 1),
                (z + 1, y + 1, x),
                (z + 1, y - 1, x),
                (z - 1, y + 1, x),
                (z - 1, y - 1, x),
                (z + 1, y, x + 1),
                (z + 1, y, x - 1),
                (z - 1, y, x + 1),
                (z - 1, y, x - 1),
                (z, y + 1, x + 1),
                (z, y + 1, x - 1),
                (z, y - 1, x + 1),
                (z, y - 1, x - 1),
                (z + 1, y + 1, x + 1),
                (z + 1, y + 1, x - 1),
                (z + 1, y - 1, x + 1),
                (z + 1, y - 1, x - 1),
                (z - 1, y + 1, x + 1),
                (z - 1, y + 1, x - 1),
                (z - 1, y - 1, x + 1),
                (z - 1, y - 1, x - 1),
            ]

    def set_root(self, root_voxel):
        self.root = root_voxel

    def get_root(self):
        return self.root

    def get_mst(self):
        mst = nx.minimum_spanning_tree(self.graph, weight="weight", algorithm="prim")
        print(">> Minimum Spanning Tree Generated")
        print(">> Minimum Spanning Tree length:",len(mst))
        return mst

    def apply_dfs_and_label_nodes(self):
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
                stack.extend((neighbor, mst.nodes[voxel]["id"]) for neighbor in mst.neighbors(voxel))

        print(">> Depth-First search and labeling complete")
        return mst
    
    def save_to_swc(self,mst,filename, width=1.0):

        swc = SWCFile(filename)
        mst_nodes_data = mst.nodes(data=True)
        for node, attrs in mst_nodes_data:
            if "id" not in attrs:
                continue
            z, y, x = node
            swc.add_point(attrs["id"], 9, x, y, z, width, attrs["parent"])

        return swc.write_file()
