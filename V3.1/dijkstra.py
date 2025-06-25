import pickle
import heapq
import numpy as np
import sys

# Aumentar el límite de recursión a 10000
sys.setrecursionlimit(10000)

# Cargar grafo
with open("data/grafo_con_comunidades.pkl", "rb") as f:
    grafo = pickle.load(f)

# Comunidad objetivo
comunidad_objetivo = 122

# Extraer nodos de la comunidad
nodos_comunidad = [
    nid for nid, com in grafo.comunidades.items()
    if com == comunidad_objetivo and nid in grafo.adj
]

# Dijkstra parcial: solo calcula distancias
def dijkstra_distancias(graph, start, nodos_objetivo):
    dist = {start: 0}
    visited = set()
    heap = [(0, start)]

    while heap:
        current_dist, u = heapq.heappop(heap)
        if u in visited:
            continue
        visited.add(u)

        for v, weight in graph.adj.get(u, []):
            if v in visited:
                continue
            new_dist = current_dist + weight
            if new_dist < dist.get(v, float('inf')):
                dist[v] = new_dist
                heapq.heappush(heap, (new_dist, v))

    return {v: d for v, d in dist.items() if v in nodos_objetivo and v != start}

# Calcular distancias entre todos los pares
distancias = []
for i, nodo in enumerate(nodos_comunidad):
    resultado = dijkstra_distancias(grafo, nodo, nodos_comunidad)
    distancias.extend(resultado.values())
    if i % 100 == 0:
        print(f"Procesado {i}/{len(nodos_comunidad)} nodos")

# Resultado
if distancias:
    promedio = np.mean(distancias)
    print(f"Promedio de distancia entre pares en la comunidad {comunidad_objetivo}: {promedio:.2f}")
    print(f"Cantidad de pares analizados: {len(distancias)}")
    print(f"Total de nodos en la comunidad: {len(nodos_comunidad)}")
else:
    print("No se encontraron caminos dentro de la comunidad.")
