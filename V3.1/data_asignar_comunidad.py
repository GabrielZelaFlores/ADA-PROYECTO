from collections import defaultdict
import pickle
from graphObj import Graph  
import time
class LouvainCommunityDetector:
    def __init__(self, graph):
        self.graph = graph
        self.total_weight = self._compute_total_weight()
        self.node_community = {node: node for node in self.graph.adj}
        self.community_internal_weight = defaultdict(float)
        self.community_total_degree = defaultdict(float)

    def _compute_total_weight(self):
        total = 0
        for u in self.graph.adj:
            for v, w in self.graph.adj[u]:
                total += w
        return total / 2  # Cada arista se cuenta dos veces

    def _node_degree(self, node):
        return sum(w for _, w in self.graph.adj[node])

    def _init_communities(self):
        for node in self.graph.adj:
            deg = self._node_degree(node)
            self.community_total_degree[node] = deg
            for v, w in self.graph.adj[node]:
                if node == v:
                    self.community_internal_weight[node] += w

    def _modularity_gain(self, node, community, k_i, sum_tot, k_i_in):
        m = self.total_weight
        return (k_i_in - (sum_tot * k_i) / (2 * m))

    def _neighbor_communities(self, node):
        neighbor_coms = defaultdict(float)
        for neighbor, weight in self.graph.adj[node]:
            if neighbor == node:
                continue
            community = self.node_community[neighbor]
            neighbor_coms[community] += weight
        return neighbor_coms

    def _move_node(self, node, k_i):
        best_community = self.node_community[node]
        best_gain = 0.0
        current_community = best_community

        neighbor_coms = self._neighbor_communities(node)

        # Quitar nodo de su comunidad actual
        self.community_total_degree[current_community] -= k_i

        for community, k_i_in in neighbor_coms.items():
            gain = self._modularity_gain(node, community, k_i, self.community_total_degree[community], k_i_in)
            if gain > best_gain:
                best_gain = gain
                best_community = community

        # Mover nodo si hay mejora
        self.node_community[node] = best_community
        self.community_total_degree[best_community] += k_i

        return best_community != current_community

    def run(self, max_passes=10):
        self._init_communities()
        for _ in range(max_passes):
            moved = False
            for node in self.graph.adj:
                k_i = self._node_degree(node)
                moved |= self._move_node(node, k_i)
            if not moved:
                break
        return self._build_communities()

    def _build_communities(self):
        communities = defaultdict(list)
        for node, com in self.node_community.items():
            communities[com].append(node)
        return list(communities.values())

print("Cargando GRafo")
# Paso 1: Cargar grafo
with open("data/grafo_guardado.pkl", "rb") as f:
    grafo = pickle.load(f)
print("Comunidades:")
# Paso 2: Detectar comunidades
inicio = time.time()
detector = LouvainCommunityDetector(grafo)
comunidades = detector.run()
tiempo = time.time() - inicio
print(f"Tiempo transcurrido: {tiempo:.4f} segundos")
# Paso 3: Guardar comunidad por nodo
grafo.comunidades = {}
for cid, grupo in enumerate(comunidades):
    for nodo in grupo:
        grafo.comunidades[nodo] = cid
print("Guardando grafo")
# Paso 4: Guardar grafo
with open("data/grafo_con_comunidades.pkl", "wb") as f:
    pickle.dump(grafo, f)
    print(" Grafo con comunidades guardado como 'grafo_con_comunidades.pkl'")
