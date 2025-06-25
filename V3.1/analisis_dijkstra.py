import heapq
import pickle
from graphObj import Graph
import time
import plotly.graph_objects as go
# Cargar grafo
with open("data/grafo_con_comunidades.pkl", "rb") as f:
    grafo = pickle.load(f)

def dijkstra(graph, start, goal):
    dist = {start: 0}
    prev = {}
    visited = set()
    heap = [(0, start)]

    while heap:
        current_dist, u = heapq.heappop(heap)
        if u in visited:
            continue
        visited.add(u)

        if u == goal:
            break

        for v, weight in graph.adj.get(u, []):
            if v in visited:
                continue
            new_dist = current_dist + weight
            if new_dist < dist.get(v, float('inf')):
                dist[v] = new_dist
                prev[v] = u
                heapq.heappush(heap, (new_dist, v))

    # Reconstruir camino
    if goal not in dist:
        return None, float('inf')  # No hay camino

    path = []
    current = goal
    while current != start:
        path.append(current)
        current = prev[current]
    path.append(start)
    path.reverse()
    return path, dist[goal]

# ====================
# 🧪 Prueba
# ====================
origen = 2572385
destino = 942391

inicio = time.time()
path, costo = dijkstra(grafo, origen, destino)
tiempo = time.time() - inicio

if path:
    print(f" Camino más corto ({len(path)} nodos, costo total: {costo:.2f}):")
    print(" → ".join(map(str, path[:10])), "...")  # Imprime solo los primeros 10 si es muy largo
    print(f"Tiempo transcurrido: {tiempo:.4f} segundos")
else:
    print("ERROR: No hay camino entre los nodos.")


# =============================
# 🗺️ Construcción del mapa
# =============================
lats, lons = [], []
for nodo in path:
    if nodo in grafo.locations:
        lat, lon = grafo.locations[nodo]
        lats.append(lat)
        lons.append(lon)

# ➤ Traza del camino
path_trace = go.Scattergeo(
    lat=lats,
    lon=lons,
    mode="lines+markers",
    line=dict(width=2, color="orange"),
    marker=dict(size=5, color="orange"),
    name="Camino más corto",
    hoverinfo="text",
    text=[f"ID: {nid}" for nid in path]
)

# ➤ Nodo origen
lat_o, lon_o = grafo.locations[origen]
origen_trace = go.Scattergeo(
    lat=[lat_o],
    lon=[lon_o],
    mode="markers+text",
    marker=dict(size=10, color="blue", symbol="circle"),
    text=["Origen"],
    textposition="bottom center",
    name="Origen"
)

# ➤ Nodo destino
lat_d, lon_d = grafo.locations[destino]
destino_trace = go.Scattergeo(
    lat=[lat_d],
    lon=[lon_d],
    mode="markers+text",
    marker=dict(size=10, color="red", symbol="circle"),
    text=["Destino"],
    textposition="bottom center",
    name="Destino"
)

# ➤ Mostrar figura
fig = go.Figure([path_trace, origen_trace, destino_trace])

fig.update_geos(
    showland=True,
    landcolor="rgb(240,240,240)",
    oceancolor="rgb(210, 230, 255)",
    showocean=True,
    showcountries=True,
    countrycolor="black"
)

fig.update_layout(
    title=f"Camino más corto entre {origen} y {destino} (costo: {costo:.2f})",
    margin=dict(l=0, r=0, t=40, b=0)
)

fig.write_html("graficos/dijkstra/camino_mas_corto.html")
fig.show()