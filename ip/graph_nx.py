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
        self.mst = nx.Graph()

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

            z_sort = sorted(z)
            y_sort = sorted(y)
            x_sort = sorted(x)

            # Calcula a média móvel simples para cada array
            z_sma = np.convolve(
                z_sort, np.ones(window_size) / window_size, mode="valid"
            )
            y_sma = np.convolve(
                y_sort, np.ones(window_size) / window_size, mode="valid"
            )
            x_sma = np.convolve(
                x_sort, np.ones(window_size) / window_size, mode="valid"
            )

            return arr + list(zip(z_sma, y_sma, x_sma))

        return arr

    def euclidean_distance(
        self, point1: Tuple[float, float, float], point2: Tuple[float, float, float]
    ) -> float:
        z1, y1, x1 = point1
        z2, y2, x2 = point2
        squared_diff_xy = (x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2
        distance_xy = np.sqrt(squared_diff_xy)
        return distance_xy

    def create_graph(
        self, moving_avg: bool = False, window_moving_avg_sz: int = 2
    ) -> None:

        non_zero_voxels = np.nonzero(self.image)  # Get indices of all non-zero voxels
        for z, y, x in zip(*non_zero_voxels):
            voxel = (z, y, x)
            self.graph.add_node(voxel, pos=voxel)
            neighborhood = self.get_26_neighborhood(voxel)

            if moving_avg:
                mov_avg = self.simple_moving_average(neighborhood, window_moving_avg_sz)
                for neighbor in mov_avg:
                    self.add_edge_with_weight(voxel, neighbor)
            else:
                for neighbor in neighborhood:
                    self.add_edge_with_weight(voxel, neighbor)

        self.set_mst(self.graph)
        print(" >> undirected Graph and Minimum Spanning Tree created.")

    # Dentro da classe Graph em graph_nx.py

    def prune_by_branch_length(self, length_threshold: int):
        """
        Poda o grafo removendo ramos curtos.
        Um ramo é uma sequência de nós de um ponto final (grau 1) até um ponto de junção (grau > 2).

        Args:
            length_threshold (int): O comprimento máximo (em número de nós) para um ramo ser podado.
        """
        if length_threshold <= 0:
            return

        print(f" >> Iniciando a poda de ramos com comprimento <= {length_threshold}")

        # É mais seguro trabalhar em uma cópia para iterar enquanto se modifica o grafo
        graph_copy = self.get_mst()

        # Encontra todos os pontos finais no grafo original
        endpoints = [node for node, degree in graph_copy.degree() if degree == 1]

        nodes_to_remove = set()

        for start_node in endpoints:
            # Se o nó já foi removido como parte de outro ramo, pule
            if start_node not in graph_copy:
                continue

            path = [start_node]
            current_node = start_node
            visited_in_path = {current_node}

            # Percorre o ramo
            while graph_copy.degree(current_node) < 3:
                # Encontra o próximo vizinho que não foi visitado neste caminho
                # Para nós de grau 2, haverá um vizinho não visitado. Para grau 1, um. Para grau 0 ou >2, o laço para.
                next_neighbors = [
                    n
                    for n in graph_copy.neighbors(current_node)
                    if n not in visited_in_path
                ]

                if not next_neighbors:
                    break  # Chegou ao fim de um fragmento isolado ou de volta ao início

                current_node = next_neighbors[0]
                path.append(current_node)
                visited_in_path.add(current_node)

                # Para se o caminho ficar muito longo (segurança) ou se o nó já foi marcado para remoção
                if len(path) > length_threshold + 1 or current_node in nodes_to_remove:
                    break

            # Se o caminho (excluindo o ponto de junção) for curto o suficiente, marque para remoção
            # O último nó no 'path' é o ponto de junção ou o fim do fragmento
            branch_to_prune = path[:-1]
            if len(branch_to_prune) <= length_threshold:
                nodes_to_remove.update(branch_to_prune)

        if nodes_to_remove:
            graph_copy.remove_nodes_from(list(nodes_to_remove))
            print(
                f" >> Poda concluída. {len(nodes_to_remove)} nós removidos de ramos curtos."
            )

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

    def get_graph(self) -> nx.Graph:
        return self.graph

    def set_mst(self, graph: nx.Graph) -> nx.Graph:
        self.mst = nx.minimum_spanning_tree(
            graph.copy(), weight="weight", algorithm="kruskal"
        )

    def get_mst(self) -> nx.Graph:
        return self.mst

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

    def save_to_swc(
        self, mst: nx.Graph, filename: str, pressure_field: np.ndarray = None
    ) -> bool:

        swc = SWCFile(filename)
        mst_nodes_data = mst.nodes(data=True)

        for node, attrs in mst_nodes_data:

            if "id" not in attrs:
                continue
            z, y, x = node

            if (
                0 <= int(z) < pressure_field.shape[0]
                and 0 <= int(y) < pressure_field.shape[1]
                and 0 <= int(x) < pressure_field.shape[2]
                and pressure_field[int(z), int(y), int(x)] > 0
            ):
                width = pressure_field[int(z), int(y), int(x)]

            swc.add_point(attrs["id"], 9, x, y, z, width, attrs["parent"])

        return swc.write_file()
