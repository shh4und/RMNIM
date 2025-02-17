from scipy.spatial import KDTree
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


def create_graph_from_kdtree(points, k=10, r=5, p=2):
    """
    Build a Minimum Spanning Tree (MST) using KD-Tree where nodes
    are points and edges are distances to nearest neighbors.

    Parameters:
        points (np.ndarray): Array of points (2D or 3D).

    Returns:
        nx.Graph: MST with points as nodes and distances as edges.
    """
    # Create KD-Tree
    tree = KDTree(points, leafsize=1)

    # Initialize graph
    G = nx.Graph()

    # Add nodes to the graph
    for i, point in enumerate(points):
        G.add_node(i, pos=point)

    # Find nearest neighbors and add edges
    distances, indices = tree.query(
        points, k=k + 1, eps=0.1, p=p, distance_upper_bound=r
    )  # Find all neighbors
    for i, (dist, idx) in enumerate(zip(distances, indices)):
        for j in range(1, k + 1):  # Start from 1 to skip the point itself
            G.add_edge(i, idx[j], weight=dist[j])

    # query-ball
    # # Find neighbors within radius r and add edges
    # neighbors = tree.query_ball_point(points, r, p=p)
    # for i, indices in enumerate(neighbors):
    #     for j in indices:
    #         if i != j:  # Avoid self-loops
    #             distance = np.linalg.norm(points[i] - points[j], ord=p)
    #             G.add_edge(i, j, weight=distance)
    return G

def get_node_index_by_position(graph, root_position):
    """
    Obtém o índice do nó do grafo a partir da posição da raiz.

    Parameters:
        graph (nx.Graph): O grafo.
        root_position (tuple): A posição da raiz (x, y, z).

    Returns:
        int: O índice do nó correspondente à posição da raiz.
    """
    for node, data in graph.nodes(data=True):
        if 'pos' in data and (data['pos'][0] == root_position[0] and data['pos'][1] == root_position[1] and data['pos'][2] == root_position[2]):
            return node
    raise ValueError("No node found with the specified root position")


def subgraph_length(G, vertex, visited):
    """
    Calcula a cardinalidade (número de vértices) de um subgrafo conectado ao vértice inicial.

    Args:
        G: Grafo do tipo nx.Graph.
        vertex: Vértice inicial para a BFS.
        visited: Conjunto de vértices já visitados.

    Returns:
        tamanho: Número de vértices no subgrafo.
        subgraph_nodes: Lista de nós no subgrafo.
    """
    # Verifica se o vértice já foi visitado
    if vertex in visited:
        return 0, []

    # Inicializa a busca em largura
    queue = [vertex]
    subgraph_nodes = []
    while queue:
        current = queue.pop(0)
        if current not in visited:
            visited.add(current)
            subgraph_nodes.append(current)
            # Adiciona os vizinhos na fila
            queue.extend(n for n in G.neighbors(current) if n not in visited)

    # Retorna o tamanho e os nós do subgrafo
    return len(subgraph_nodes), subgraph_nodes


def filter_graph_by_length(G, threshold_length):
    """
    Filtra subgrafos pequenos (com cardinalidade menor que o limiar) de um grafo.

    Args:
        G: Grafo do tipo nx.Graph.
        threshold_length: Tamanho mínimo do subgrafo para ser mantido.

    Returns:
        G_filtered: Grafo filtrado.
    """
    visited = set()
    nodes_to_keep = set()

    # Itera sobre todos os nós do grafo
    for node in G.nodes:
        if node not in visited:
            # Calcula a cardinalidade do subgrafo conectado ao nó atual
            size, subgraph_nodes = subgraph_length(G, node, visited)
            if size >= threshold_length:
                # Mantém os nós do subgrafo grande
                nodes_to_keep.update(subgraph_nodes)

    # Cria um subgrafo com os nós restantes
    G_filtered = G.subgraph(nodes_to_keep).copy()
    return G_filtered


def filter_graph_by_shortest_paths(G, root):
    """
    Filtra o grafo para conter apenas os caminhos mais curtos a partir do nó raiz.

    Parameters:
        G (nx.Graph): Grafo original.
        root (node): Nó raiz a partir do qual calcular os caminhos mais curtos.

    Returns:
        nx.Graph: Novo grafo contendo apenas os caminhos mais curtos a partir do nó raiz.
    """
    # Use single_source_dijkstra para obter distâncias e caminhos
    distances, paths = nx.single_source_dijkstra(G, root)

    # Crie um novo grafo para conter os caminhos mais curtos
    shortest_path_graph = nx.Graph()

    # Adicione nós e arestas ao novo grafo com base nos caminhos mais curtos
    for target, path in paths.items():
        # Adicione nós ao novo grafo
        for node in path:
            if node not in shortest_path_graph:
                if 'pos' not in G.nodes[node]:
                    continue
                else:
                    shortest_path_graph.add_node(node, pos=G.nodes[node]['pos'])

        # Adicione arestas ao novo grafo
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            weight = G[u][v]['weight']
            shortest_path_graph.add_edge(u, v, weight=weight)

    return shortest_path_graph


def visualize_medial_graph(image3d, graph):
    """
    Visualize the medial graph overlaid on the original image.
    Projects 3D coordinates to 2D for visualization.
    """
    plt.figure(figsize=(15, 15))

    # Show max projection of image
    proj = np.max(image3d, axis=0)
    plt.imshow(proj, cmap="gray")

    # Get 3D positions and convert to 2D by dropping z-coordinate
    pos_3d = nx.get_node_attributes(graph, "pos")
    pos_2d = {node: (pos[2], pos[1]) for node, pos in pos_3d.items()}  # Use y,x coords

    # Filter edges to include only those with defined positions
    edges_to_draw = [(u, v) for u, v in graph.edges if u in pos_2d and v in pos_2d]

    # Draw graph edges with 2D positions
    nx.draw_networkx_edges(
        graph, pos=pos_2d, edgelist=edges_to_draw, edge_color="r", width=0.5
    )

    # Draw nodes with 2D positions
    nodes_to_draw = [node for node in graph.nodes if node in pos_2d]
    nx.draw_networkx_nodes(
        graph, pos=pos_2d, nodelist=nodes_to_draw, node_size=0.3, node_color="b"
    )

    plt.axis("off")
    plt.show()


def find_nearest_foreground_point(image3d, root_point, search_radius=5):
    """
    Encontra o ponto foreground mais próximo de um ponto raiz em uma imagem 3D binária.

    Parameters:
        image3d (np.ndarray): Imagem 3D binária (z, y, x).
        root_point (tuple): Coordenadas do ponto raiz (x, y, z).
        search_radius (int): Raio de busca em torno do ponto raiz.

    Returns:
        tuple: Coordenadas do ponto foreground mais próximo (x, y, z).
    """
    x, y, z = map(int, root_point)

    # Definir os limites da região de busca
    z_min, z_max = max(0, z - search_radius), min(image3d.shape[0], z + search_radius + 1)
    y_min, y_max = max(0, y - search_radius), min(image3d.shape[1], y + search_radius + 1)
    x_min, x_max = max(0, x - search_radius), min(image3d.shape[2], x + search_radius + 1)

    # Extrair a região de busca
    search_region = image3d[z_min:z_max, y_min:y_max, x_min:x_max]

    # Encontrar coordenadas dos pontos foreground na região de busca
    foreground_coords = np.argwhere(search_region > 0)

    if len(foreground_coords) == 0:
        raise ValueError("Nenhum ponto foreground encontrado na região de busca.")

    # Ajustar as coordenadas para o sistema de coordenadas original
    foreground_coords += [z_min, y_min, x_min]

    # Criar KD-Tree para encontrar o ponto mais próximo
    tree = KDTree(foreground_coords)
    distance, index = tree.query([z, y, x])

    nearest_point = foreground_coords[index]
    return tuple(nearest_point)  # Retornar como (x, y, z)