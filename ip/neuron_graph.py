import networkx as nx
import numpy as np
from typing import List, Tuple
from ip.vfc import *

class NeuronGraph:
    def __init__(self, medial_points: np.ndarray, values: np.ndarray, k_neighbors: int = 5):
        self.graph = nx.Graph()
        self.root = None
        self.medial_points = medial_points
        self.values = values
        self.k = k_neighbors
        
    def build_graph(self, max_distance: float = 10.0):
        # Adicionar nós
        for i, point in enumerate(self.medial_points):
            self.graph.add_node(tuple(point), value=self.values[i])
            
        # Conectar k vizinhos mais próximos
        from sklearn.neighbors import NearestNeighbors
        nbrs = NearestNeighbors(n_neighbors=self.k).fit(self.medial_points)
        distances, indices = nbrs.kneighbors()
        
        # Adicionar arestas
        for i in range(len(self.medial_points)):
            point = tuple(self.medial_points[i])
            for j, dist in zip(indices[i], distances[i]):
                if dist <= max_distance:
                    neighbor = tuple(self.medial_points[j])
                    self.graph.add_edge(point, neighbor, weight=dist)
    
    def set_root(self):
        # Selecionar ponto com maior valor como raiz
        max_value_idx = np.argmax(self.values)
        self.root = tuple(self.medial_points[max_value_idx])
    
    def generate_swc(self, filename: str):
        if not self.root:
            self.set_root()
            
        # Gerar MST
        mst = nx.minimum_spanning_tree(self.graph)
        
        # DFS para ordenar nós
        visited = {}
        parent = {}
        node_id = 1
        
        stack = [(self.root, -1)]
        while stack:
            node, parent_id = stack.pop()
            if node not in visited:
                visited[node] = node_id
                parent[node] = parent_id
                node_id += 1
                stack.extend((n, visited[node]) for n in mst.neighbors(node) if n not in visited)
        
        # Escrever arquivo SWC
        with open(filename, 'w') as f:
            f.write("# id type x y z radius parent\n")
            for node in visited:
                z, y, x = node
                line = f"{visited[node]} 2 {x} {y} {z} 1.0 {parent[node]}\n"
                f.write(line)
        
        return True

# Uso:
def process_image_to_swc(image3d, scale_space, filename):
    # Obter pontos mediais
    medialness = scale_space_medialness(image3d, scale_space)
    coords, values = local_maxima_3D(medialness)
    
    # Criar e processar grafo
    neuron = NeuronGraph(coords, values)
    neuron.build_graph()
    neuron.generate_swc(filename)