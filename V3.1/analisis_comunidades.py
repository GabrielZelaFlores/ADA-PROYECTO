import pickle
from collections import defaultdict, Counter
import statistics
import time
from logger_config import setup_logger
# ========================
# Cargar grafo
# ========================
def cargar_grafo(path="data/grafo_con_comunidades.pkl"):
    with open(path, "rb") as f:
        grafo = pickle.load(f)
    if not hasattr(grafo, "comunidades"):
        raise ValueError("ERROR: El grafo no tiene atributo 'comunidades'.")
    return grafo    
# ========================
# Construir estructura por comunidad
# ========================
def construir_comunidades(grafo):
    comunidades = defaultdict(set)
    for nodo, comunidad in grafo.comunidades.items():
        comunidades[comunidad].add(nodo)
    return comunidades
# ========================
# Análisis por comunidad
# ========================
def analizar_comunidad(grafo, comunidades,comunidad_id):
    if comunidad_id not in comunidades:
        print(f" ERROR: Comunidad {comunidad_id} no encontrada.")
        return

    nodos = comunidades[comunidad_id]
    total_nodos = len(nodos)

    aristas = 0
    in_degrees = Counter()

    for u in nodos:
        for v, _ in grafo.adj.get(u, []):  # ahora v, peso
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
def analisis_general(grafo,comunidades):
    resumen = []
    print("\n===== Análisis General de Comunidades =====")
    for cid, nodos in comunidades.items():
        total_nodos = len(nodos)
        aristas = 0
        for u in nodos:
            for v, _ in grafo.adj.get(u, []):  # considerar pesos, pero aquí solo se cuenta
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

    print("\nTop 25 comunidades más grandes:")
    for cid, n, _, _ in sorted(resumen, key=lambda x: -x[1])[:25]:
        print(f"  Comunidad {cid:<4} con {n} nodos")

    min_nodos = 100

    print(f"\nTop 10 comunidades más pequeñas con más de {min_nodos} nodos:")
    for cid, n, _, _ in sorted([r for r in resumen if r[1] > min_nodos], key=lambda x: x[1])[:10]:
        print(f"  Comunidad {cid:<4} con {n} nodos")

def analisis_comunidades_main(script,logger):
    try:
        print(f"\n--- Ejecutando módulo: {script} ---")
        logger.info(f"Ejecutando módulo: {script}")
        start = time.time()
        logger.info(f"Construyendo grafo...")
        grafo = cargar_grafo()
        comunidades = construir_comunidades(grafo)

        opcion = input(
            "¿Qué deseas analizar?\n1. Comunidad específica\n2. Análisis general\nOpción: "
        ).strip()

        if opcion == "1":
            try:
                cid = int(input("Ingrese el ID de la comunidad: "))
                analizar_comunidad(grafo, comunidades, cid)
            except ValueError:
                print("ID inválido.")
        else:
            analisis_general(grafo, comunidades)

        end = time.time()
        dur = end - start

        print(f"--- Módulo {script} finalizado en {dur:.2f} segundos ---")
        logger.info(f"Módulo {script} ejecutado en {dur:.2f} segundos")

    except Exception as e:
        logger.exception(f"Error al ejecutar {script} como módulo: {e}")
        print(f"Error al ejecutar {script}. Ver app.log para detalles.")