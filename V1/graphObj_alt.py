class Graph:
    def __init__(self):
        self.adj = {}        # nodo -> lista de (vecino, peso)
        self.locations = {}  # nodo -> (lat, lon)
        self.comunidades = {}  # nodo -> id de comunidad

    def add_edge(self, u, v, weight=1.0):
        if u not in self.adj:
            self.adj[u] = []
        self.adj[u].append((v, weight))

    def set_location(self, node_id, lat, lon):
        self.locations[node_id] = (lat, lon)

    def num_nodes(self):
        return len(self.adj)

    def num_edges(self):
        return sum(len(vecinos) for vecinos in self.adj.values())

    def get_neighbors(self, node_id):
        """Devuelve solo los vecinos (sin pesos)"""
        return [v for v, _ in self.adj.get(node_id, [])]

    def to_undirected(self):
        """Devuelve una versión no dirigida del grafo"""
        undirected = Graph()
        undirected.locations = self.locations.copy()

        for u, vecinos in self.adj.items():
            for v, w in vecinos:
                undirected.add_edge(u, v, w)
                undirected.add_edge(v, u, w)  # Añadir arista en sentido inverso

        return undirected

    def set_communities(self, labels: dict):
        """Asigna el diccionario nodo -> comunidad"""
        self.comunidades = labels
