# analisisdecomunidades.py

import pickle
from collections import defaultdict, Counter
import statistics

# ========================
# Cargar grafo
# ========================
with open("data/grafo_con_comunidades.pkl", "rb") as f:
    grafo = pickle.load(f)

if not hasattr(grafo, "comunidades"):
    raise ValueError("\u274c El grafo no tiene atributo 'comunidades'. Debes calcularlas primero.")

# ========================
# Construir estructura por comunidad
# ========================
comunidades = defaultdict(set)
for nodo, comunidad in grafo.comunidades.items():
    comunidades[comunidad].add(nodo)

# ========================
# Análisis por comunidad
# ========================
def analizar_comunidad(comunidad_id):
    if comunidad_id not in comunidades:
        print(f"\u274c Comunidad {comunidad_id} no encontrada.")
        return

    nodos = comunidades[comunidad_id]
    total_nodos = len(nodos)

    # Aristas dentro de la comunidad
    aristas = 0
    in_degrees = Counter()

    for u in nodos:
        for v in grafo.adj.get(u, []):
            if v in nodos:
                aristas += 1
                in_degrees[v] += 1

    grado_promedio = aristas / total_nodos if total_nodos else 0
    top_nodos = in_degrees.most_common(10)

    print(f"\n===== Comunidad {comunidad_id} =====")
    print(f"Nodos totales       : {total_nodos}")
    print(f"Aristas internas    : {aristas}")
    print(f"Grado promedio      : {grado_promedio:.2f}")
    print(f"Top 10 más populares (in-degree):")
    for nodo, grado in top_nodos:
        print(f"  Nodo {nodo:<6} → {grado} conexiones entrantes")

# ========================
# Análisis general
# ========================
def analisis_general():
    resumen = []
    print("\n===== Análisis General de Comunidades =====")
    for cid, nodos in comunidades.items():
        total_nodos = len(nodos)
        aristas = 0
        for u in nodos:
            for v in grafo.adj.get(u, []):
                if v in nodos:
                    aristas += 1
        grado_promedio = aristas / total_nodos if total_nodos else 0
        resumen.append((cid, total_nodos, aristas, grado_promedio))

    total_comunidades = len(resumen)
    prom_nodos = statistics.mean(r[1] for r in resumen)
    prom_aristas = statistics.mean(r[2] for r in resumen)
    prom_grado = statistics.mean(r[3] for r in resumen)

    print(f"Total de comunidades : {total_comunidades}")
    print(f"Promedio de nodos    : {prom_nodos:.2f}")
    print(f"Promedio de aristas  : {prom_aristas:.2f}")
    print(f"Grado promedio global: {prom_grado:.2f}")

    print("\nTop 5 comunidades más grandes:")
    for cid, n, _, _ in sorted(resumen, key=lambda x: -x[1])[:5]:
        print(f"  Comunidad {cid:<4} con {n} nodos")

    min_nodos = 100  # mínimo de nodos para considerar

    print(f"\nTop 20 comunidades más pequeñas con más de {min_nodos} nodos:")
    for cid, n, _, _ in sorted([r for r in resumen if r[1] > min_nodos], key=lambda x: x[1])[:10]:
        print(f"  Comunidad {cid:<4} con {n} nodos")


# ========================
# Ejecutar ejemplo
# ========================
if __name__ == "__main__":
    print("ANALISIS DE COMUNIDADES\nOpciones:\n1. Analisis de Comunidad por ID\n2. Analisis General")
    a =  int(input("Opción: "))
    if a == 1:
        comunidad_id = int(input("Ingrese el ID de la comunidad a analizar: "))
        analizar_comunidad(comunidad_id)
    else:
        analisis_general()
