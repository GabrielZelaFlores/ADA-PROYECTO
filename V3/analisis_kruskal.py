import pickle
import plotly.graph_objects as go
from collections import deque, defaultdict

# =======================
# 📦 Cargar grafo con comunidades
# =======================
with open("data/grafo_con_comunidades.pkl", "rb") as f:
    grafo = pickle.load(f)

# =======================
# 🎯 Comunidad objetivo
# =======================
comunidad_objetivo = 7
max_nodos_mostrar = 5000  # Limitar cantidad de nodos mostrados

# =======================
# 🔎 Filtrar nodos de la comunidad
# =======================
nodos = {nid for nid, com in grafo.comunidades.items() if com == comunidad_objetivo}
aristas = []

for u in nodos:
    for v, w in grafo.adj.get(u, []):
        if v in nodos and u < v:
            aristas.append((u, v, w))

# =======================
# 🔗 Kruskal con Union-Find
# =======================
class UnionFind:
    def __init__(self):
        self.parent = {}

    def find(self, u):
        if self.parent.get(u, u) != u:
            self.parent[u] = self.find(self.parent[u])
        return self.parent.get(u, u)

    def union(self, u, v):
        pu, pv = self.find(u), self.find(v)
        if pu == pv:
            return False
        self.parent[pu] = pv
        return True

uf = UnionFind()
mst = []
peso_total = 0
aristas_ordenadas = sorted(aristas, key=lambda x: x[2])

for u, v, w in aristas_ordenadas:
    if uf.union(u, v):
        mst.append((u, v, w))
        peso_total += w

# =======================
# 🌳 Construir grafo MST para BFS
# =======================
mst_adj = defaultdict(list)
for u, v, w in mst:
    mst_adj[u].append((v, w))
    mst_adj[v].append((u, w))

# Elegir raíz como nodo con mayor grado
root = max(mst_adj, key=lambda x: len(mst_adj[x]))

# BFS para recorrer primeros niveles
visited = set()
queue = deque([root])
ordenado = []

while queue and len(visited) < max_nodos_mostrar:
    u = queue.popleft()
    if u in visited:
        continue
    visited.add(u)
    ordenado.append(u)
    for v, _ in mst_adj[u]:
        if v not in visited:
            queue.append(v)

nodos_visibles = set(ordenado)

# =======================
# 📈 Visualización del MST limitado por BFS
# =======================
edges = []
for u, v, _ in mst:
    if u in nodos_visibles and v in nodos_visibles:
        lat1, lon1 = grafo.locations[u]
        lat2, lon2 = grafo.locations[v]
        edges.append(go.Scattergeo(
            lon=[lon1, lon2, None],
            lat=[lat1, lat2, None],
            mode='lines',
            line=dict(width=0.7, color='orange'),
            hoverinfo='none',
            showlegend=False
        ))

nodes = go.Scattergeo(
    lon=[grafo.locations[n][1] for n in nodos_visibles],
    lat=[grafo.locations[n][0] for n in nodos_visibles],
    mode="markers",
    marker=dict(size=3, color="blue", opacity=0.7),
    name=f"Nodos Comunidad {comunidad_objetivo}",
    hovertext=[f"ID: {nid}" for nid in nodos_visibles],
    hoverinfo="text"
)

fig = go.Figure(data=[*edges, nodes])
fig.update_layout(
    title=f"MST – Comunidad {comunidad_objetivo} (primeros niveles, máx. {max_nodos_mostrar} nodos)",
    geo=dict(
        showland=True,
        landcolor="rgb(240,240,240)",
        oceancolor="rgb(210, 230, 255)",
        showocean=True,
        showcountries=True,
        countrycolor="black",
        projection_type="natural earth"
    ),
    margin=dict(l=0, r=0, t=50, b=0)
)

fig.write_html(f"graficos/MST/mst_comunidad_{comunidad_objetivo}_niveles.html")
fig.show()

# =======================
# 📊 Resultados finales
# =======================
print(f"✅ Comunidad analizada: {comunidad_objetivo}")
print(f"🌲 Aristas en el MST: {len(mst)}")
print(f"⚖️ Peso total del árbol: {peso_total:.2f}")
print(f"🔗 Componentes conectados: {len(set(uf.find(n) for n in nodos))}")
print(f"📌 Nodos visualizados (niveles más cercanos): {len(nodos_visibles)}")
