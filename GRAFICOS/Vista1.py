import pickle
from pyvis.network import Network
from graphObj import Graph
import os

# =======================
# Cargar grafo
# =======================
with open("data/grafo_guardado.pkl", "rb") as f:
    grafo = pickle.load(f)

# =======================
# Calcular grado de salida
# =======================
grados = {nodo: len(vecinos) for nodo, vecinos in grafo.adj.items()}

# Obtener los top N nodos con mayor out-degree
top_n = 1000
top_nodos = sorted(grados.items(), key=lambda x: x[1], reverse=True)[:top_n]
nodos_top = set(n for n, _ in top_nodos)

# =======================
# Construir subgrafo
# =======================
edges = []
for nodo in nodos_top:
    for vecino in grafo.adj.get(nodo, []):
        if vecino in nodos_top:
            edges.append((nodo, vecino))

# =======================
# Visualizar con Pyvis
# =======================
net = Network(height="900px", width="100%", directed=True, notebook=False)
net.barnes_hut()

# Agregar nodos (opcional: tamaño según grado)
for nodo, grado in top_nodos:
    net.add_node(nodo, label=str(nodo), size=5 + grado / 10)

# Agregar aristas
for u, v in edges:
    net.add_edge(u, v)

# Guardar HTML
os.makedirs("graficos", exist_ok=True)
net.write_html("graficos/top_nodos_representativos.html", open_browser=False)
print("✅ HTML generado con éxito.")
print("✅ Visualización guardada en 'graficos/top_nodos_representativos.html'")
