import pickle
import igraph as ig
from graphObj import Graph

# =============================
# Paso 1: Cargar tu grafo .pkl
# =============================
with open("data/grafo_guardado.pkl", "rb") as f:
    grafo = pickle.load(f)

# =============================
# Paso 2: Convertir a igraph
# =============================
edges = []
for u, vecinos in grafo.adj.items():
    for v in vecinos:
        edges.append((u, v))

# Total de nodos (usa los con ubicaciones)
n_total = max(grafo.locations.keys()) + 1  # Suponiendo IDs consecutivos

g = ig.Graph(n=n_total, edges=edges, directed=True)

# =============================
# Paso 3: Detectar comunidades
# =============================
# Convertimos el grafo a no-dirigido para Louvain
g_undirected = g.as_undirected()

print("🔍 Detectando comunidades (Louvain)...")
louvain = g_undirected.community_multilevel()
print(f"✅ Se detectaron {len(louvain)} comunidades.")

# =============================
# Paso 4: Asignar comunidad a cada nodo
# =============================
comunidades = {}
for comunidad_id, members in enumerate(louvain):
    for node_id in members:
        comunidades[node_id] = comunidad_id

# Guardamos dentro del grafo
grafo.comunidades = comunidades

# =============================
# Paso 5: Guardar el grafo actualizado
# =============================
with open("data/grafo_con_comunidades.pkl", "wb") as f:
    pickle.dump(grafo, f)
    print("💾 Grafo con comunidades guardado como 'grafo_con_comunidades.pkl'")