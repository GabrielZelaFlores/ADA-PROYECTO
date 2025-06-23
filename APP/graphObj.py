
class Graph:
    def __init__(self):
        self.adj = {}  # usuario -> lista de vecinos
        self.locations = {}  # usuario -> (lat, lon)

    def add_edge(self, u, v):
        if u not in self.adj:
            self.adj[u] = []
        self.adj[u].append(v)

    def set_location(self, user_id, lat, lon):
        self.locations[user_id] = (lat, lon)

    def num_nodes(self):
        return len(self.adj)

    def num_edges(self):
        return sum(len(v) for v in self.adj.values())