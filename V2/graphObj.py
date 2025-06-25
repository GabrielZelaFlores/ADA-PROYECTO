class Graph:
    def __init__(self):
        self.adj = {}        # nodo -> lista de (vecino, peso)
        self.locations = {}  # nodo -> (lat, lon)

    def add_edge(self, u, v, weight=1.0):
        if u not in self.adj:
            self.adj[u] = []
        self.adj[u].append((v, weight))

    def set_location(self, user_id, lat, lon):
        self.locations[user_id] = (lat, lon)

    def num_nodes(self):
        return len(self.adj)

    def num_edges(self):
        return sum(len(vecinos) for vecinos in self.adj.values())
    
    def print_node_info(self, node_id):
        print(f"📍 Nodo {node_id}")

        # Ubicación
        if node_id in self.locations:
            lat, lon = self.locations[node_id]
            print(f"  🌎 Ubicación: ({lat:.6f}, {lon:.6f})")
        else:
            print("  ⚠️ Ubicación no registrada.")

        # Vecinos
        if node_id in self.adj and self.adj[node_id]:
            print(f"  🔗 Conexiones ({len(self.adj[node_id])}):")
            for v, peso in self.adj[node_id]:
                print(f"    → {v} (peso: {peso})")
        else:
            print("  ❌ Sin conexiones salientes.")