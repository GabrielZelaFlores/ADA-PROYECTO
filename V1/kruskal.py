import pickle
# Import graphObj to be able to load the pickled graph.
# This is not used by Kruskal's algorithm itself but by the example loader.
from graphObj import Graph

class DSU:
    """
    Disjoint Set Union (DSU) data structure, also known as Union-Find.
    Used to efficiently track connected components and detect cycles.
    """
    def __init__(self, n):
        """
        Initializes DSU for n elements. Each element is initially in its own set.
        Args:
            n (int): The number of elements (nodes). Can also be initialized lazily.
        """
        self.parent = {} # Using a dictionary for sparse node IDs
        self.num_nodes_processed = 0

    def _add_node_if_not_exists(self, i):
        """Adds a node to the DSU if it's not already present."""
        if i not in self.parent:
            self.parent[i] = i
            self.num_nodes_processed +=1

    def find(self, i):
        """
        Finds the representative (root) of the set containing element i,
        with path compression.
        Args:
            i: The element to find.
        Returns:
            The representative of the set containing i.
        """
        self._add_node_if_not_exists(i)
        if self.parent[i] == i:
            return i
        self.parent[i] = self.find(self.parent[i])  # Path compression
        return self.parent[i]

    def union(self, i, j):
        """
        Merges the sets containing elements i and j.
        Uses union by rank (implicitly, by always making root_i parent of root_j,
        though a more explicit rank/size tracking could be added if needed).
        Args:
            i: An element from the first set.
            j: An element from the second set.
        Returns:
            bool: True if a union occurred (i and j were in different sets),
                  False otherwise (i and j were already in the same set).
        """
        self._add_node_if_not_exists(i)
        self._add_node_if_not_exists(j)

        root_i = self.find(i)
        root_j = self.find(j)

        if root_i != root_j:
            self.parent[root_j] = root_i  # Merge smaller tree under larger (simplified here)
            return True
        return False

def kruskal_mst(edges, num_nodes=None):
    """
    Computes the Minimum Spanning Tree (MST) of a graph using Kruskal's algorithm.
    Args:
        edges (list of tuples): A list where each tuple represents an edge
                                (weight, u, v), where u and v are node identifiers.
        num_nodes (int, optional): The total number of nodes in the graph.
                                   If not provided, DSU will initialize nodes lazily.
    Returns:
        tuple: (mst_edges, mst_weight)
               mst_edges (list of tuples): The edges forming the MST.
               mst_weight (float): The total weight of the MST.
    """
    if not edges:
        return [], 0

    # Sort edges by weight in non-decreasing order
    # The items in the edge tuple are (weight, u, v)
    sorted_edges = sorted(edges, key=lambda edge: edge[0])

    mst_edges = []
    mst_weight = 0.0

    # Initialize DSU. If num_nodes is not given, it handles nodes as they appear.
    # However, for Kruskal's, it's typical to know the set of vertices.
    # If num_nodes is not given, DSU will create entries for nodes as they are seen.
    # Max node ID could be inferred if num_nodes is None, but DSU handles sparse IDs.
    if num_nodes is None:
        all_nodes = set()
        for _, u, v in edges:
            all_nodes.add(u)
            all_nodes.add(v)
        # DSU can be initialized with count, but our dictionary-based DSU is fine.
        dsu = DSU(len(all_nodes))
    else:
        dsu = DSU(num_nodes)


    for weight, u, v in sorted_edges:
        # If adding edge (u,v) doesn't form a cycle
        if dsu.union(u, v):
            mst_edges.append((u, v, weight)) # Storing as (u,v,weight) for consistency
            mst_weight += weight
            # Optimization: if MST has V-1 edges, it's complete (for a connected graph)
            # This requires knowing V (number of nodes involved in edges).
            # dsu.num_nodes_processed gives nodes seen by DSU.
            # If num_nodes is supplied and represents the total expected nodes in the component:
            if num_nodes and len(mst_edges) == num_nodes -1:
                 break
            # If num_nodes is not supplied, we might not reach V-1 if graph is disconnected.
            # The DSU will correctly find MST for each connected component if run till end.
            # For a single component MST, it would be num_nodes_in_component - 1.

    return mst_edges, mst_weight

if __name__ == "__main__":
    print(" Kuskal's Algorithm for Minimum Spanning Tree (MST) ")
    print("----------------------------------------------------")

    # --- Example 1: Simple hardcoded graph ---
    print("\n--- Ejemplo 1: Grafo simple ---")
    # Edges: (weight, node1, node2)
    example_edges_1 = [
        (1, 'A', 'B'), (3, 'A', 'C'), (2, 'B', 'C'),
        (4, 'B', 'D'), (5, 'C', 'D'), (6, 'C', 'E'),
        (7, 'D', 'E')
    ]
    # Nodes: A, B, C, D, E (5 nodes)
    # For this small example, we can pass num_nodes or let DSU infer.

    mst_edges_1, mst_weight_1 = kruskal_mst(example_edges_1, num_nodes=5)

    print(f"MST Edges: {mst_edges_1}")
    print(f"Total MST Weight: {mst_weight_1}")
    # Expected for Example 1 (if connected and 5 nodes):
    # Edges like (A,B,1), (B,C,2), (B,D,4), (C,E,6) -> Weight 1+2+4+6 = 13

    # --- Example 2: Graph with numerical node IDs ---
    print("\n--- Ejemplo 2: Grafo con IDs numéricos ---")
    example_edges_2 = [
        (10, 0, 1), (12, 0, 2), (14, 0, 3),
        (8, 1, 2), (7, 2, 3)
    ]
    # Nodes: 0, 1, 2, 3 (4 nodes)
    mst_edges_2, mst_weight_2 = kruskal_mst(example_edges_2) # Not passing num_nodes

    print(f"MST Edges: {mst_edges_2}")
    print(f"Total MST Weight: {mst_weight_2}")
    # Expected for Example 2: (2,3,7), (1,2,8), (0,1,10) -> Weight 7+8+10 = 25

    # --- Example 3: Loading graph from project data ---
    print("\n--- Ejemplo 3: Cargando grafo desde 'data/grafo_guardado.pkl' ---")
    GRAPH_PATH = "data/grafo_guardado.pkl"
    try:
        with open(GRAPH_PATH, "rb") as f:
            project_graph = pickle.load(f)

        print(f"Grafo cargado: {project_graph.num_nodes()} nodos, {project_graph.num_edges()} aristas.")

        # Convert project_graph to list of edges (weight, u, v)
        # project_graph.adj is like: {u: [(v1, w1), (v2, w2), ...]}
        graph_edges = []
        if hasattr(project_graph, 'adj'):
            for u, neighbors in project_graph.adj.items():
                for v, weight in neighbors:
                    # Kruskal typically works on undirected graphs.
                    # If the stored graph is directed, we add each edge.
                    # To make it undirected for Kruskal, ensure (u,v,w) and (v,u,w) are considered once.
                    # A common way is to add only if u < v, or handle duplicates if graph is already undirected.
                    # For now, assuming weights are symmetric or we want MST of this directed structure.
                    # To treat as undirected, one might sort (u,v) to (min(u,v), max(u,v)) before adding to a set.
                    # Here, we just add all edges as they are.
                    graph_edges.append((weight, u, v))

            print(f"Número de aristas extraídas para Kruskal: {len(graph_edges)}")
            if not graph_edges:
                print("No se extrajeron aristas del grafo. No se puede ejecutar Kruskal.")
            else:
                # Get unique nodes to determine num_nodes for DSU if graph might be disconnected
                # or if node IDs are not sequential from 0.
                all_nodes_in_project_graph = set()
                for u, neighbors in project_graph.adj.items():
                    all_nodes_in_project_graph.add(u)
                    for v, _ in neighbors:
                        all_nodes_in_project_graph.add(v)

                num_distinct_nodes = len(all_nodes_in_project_graph)
                print(f"Número de nodos distintos en el grafo cargado: {num_distinct_nodes}")

                print("Ejecutando Kruskal en el grafo del proyecto (esto puede tardar)...")
                # Pass num_distinct_nodes for potentially better DSU initialization if graph is connected.
                # If the graph could have multiple components, not passing num_nodes or passing a count
                # of all possible nodes (e.g. max_id + 1 if dense) is also an option.
                # DSU with dict handles sparse node IDs well.
                mst_edges_project, mst_weight_project = kruskal_mst(graph_edges, num_nodes=num_distinct_nodes)

                print(f"\nResultados de Kruskal para el grafo del proyecto:")
                print(f" - Número de aristas en el MST: {len(mst_edges_project)}")
                print(f" - Peso total del MST: {mst_weight_project:.2f}")

                # Display a few edges from the MST if it's large
                if mst_edges_project:
                    print(" - Primeras 5 aristas del MST:")
                    for i, edge in enumerate(mst_edges_project[:5]):
                        print(f"   {i+1}. Nodo {edge[0]} - Nodo {edge[1]} (Peso: {edge[2]:.2f})")
        else:
            print("El objeto grafo cargado no tiene el atributo 'adj'. No se puede procesar.")

    except FileNotFoundError:
        print(f"❌ Error: Archivo del grafo '{GRAPH_PATH}' no encontrado.")
    except Exception as e:
        print(f"❌ Error al cargar o procesar el grafo del proyecto: {e}")

```
This implementation includes:
- A `DSU` (Disjoint Set Union) class with `find` (with path compression) and `union` operations. It uses a dictionary for `parent` to handle potentially sparse or non-integer node IDs (though the example uses integers from the project graph).
- The `kruskal_mst` function that takes a list of edges `(weight, u, v)` and an optional `num_nodes`. It sorts edges and uses DSU to build the MST.
- An `if __name__ == "__main__":` block with three examples:
    1. A simple graph with character node IDs.
    2. A simple graph with numerical node IDs.
    3. Loading the graph from `data/grafo_guardado.pkl`, converting its adjacency list to the required edge list format, and then running Kruskal's algorithm on it. It prints the total weight and number of edges in the resulting MST.

A note on graph representation for Kruskal:
The `project_graph` is loaded from a pickle file. Its `adj` attribute is a dictionary like `{u: [(v1, w1), (v2, w2), ...]}`. Kruskal's algorithm generally assumes an undirected graph. If the stored graph is directed, simply adding all its edges might not be standard for a classical MST unless that's the specific intent. For a true undirected MST, one would typically ensure each edge `(u, v)` with weight `w` is considered only once (e.g., by processing edges `(w, u, v)` where `u < v`, or by adding both `(u,v,w)` and `(v,u,w)` to the list if the original graph is stored as directed but represents an undirected one, and then letting Kruskal sort them). The current example code directly converts all edges from `adj` list.
The DSU is initialized with `num_distinct_nodes` found in the graph, which is appropriate if we expect a single MST for the main connected component. If the graph has multiple disconnected components, Kruskal's will find an MST for each (a minimum spanning forest).
```
