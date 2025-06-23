# paso_3_grafo_parquet.py

import polars as pl
import pickle
from graphObj import Graph

def construir_grafo_desde_parquet(parquet_usuarios, parquet_ubicaciones):
    grafo = Graph()

    print("📥 Leyendo conexiones desde .parquet...")
    df_usuarios = pl.read_parquet(parquet_usuarios)

    for idx, row in enumerate(df_usuarios.iter_rows(named=True)):
        vecinos = row["connections"]
        if vecinos is None:
            continue

        try:
            # Si es string, convertirlo en lista
            if isinstance(vecinos, str):
                vecinos = vecinos.split(",")
            for v in vecinos:
                if v.strip().isdigit():
                    grafo.add_edge(idx, int(v))
        except Exception as e:
            print(f"❌ Error en fila {idx}: {e}")

        if idx % 100_000 == 0 and idx > 0:
            print(f"  → {idx:,} usuarios procesados")

    print("📍 Leyendo ubicaciones desde .parquet...")
    df_ubicaciones = pl.read_parquet(parquet_ubicaciones)

    for idx, (lat, lon) in enumerate(zip(df_ubicaciones["latitude"], df_ubicaciones["longitude"])):
        grafo.set_location(idx, float(lat), float(lon))

    return grafo


# =============================
# 📌 EJECUCIÓN PRINCIPAL
# =============================
if __name__ == "__main__":
    path_usuarios = "data/usuarios_conexiones.parquet"
    path_ubicaciones = "data/ubicaciones_limpias.parquet"

    grafo = construir_grafo_desde_parquet(path_usuarios, path_ubicaciones)

    print("\n✅ GRAFO CONSTRUIDO")
    print(f"Total de nodos: {grafo.num_nodes():,}")
    print(f"Total de aristas: {grafo.num_edges():,}")
    print(f"Ubicaciones cargadas: {len(grafo.locations):,}")

    # =============================
    # 📊 Análisis simple del grafo
    # =============================
    print("\n📊 ANÁLISIS DEL GRAFO")

    grados = {nodo: len(vecinos) for nodo, vecinos in grafo.adj.items()}
    top_10 = sorted(grados.items(), key=lambda x: x[1], reverse=True)[:10]

    print("🔝 Top 10 nodos con más conexiones salientes:")
    for nodo, grado in top_10:
        print(f" - Nodo {nodo} → {grado} conexiones")

    nodos_sin_aristas = [n for n in range(len(grafo.locations)) if n not in grafo.adj]
    print(f"\n🧍 Nodos sin conexiones salientes: {len(nodos_sin_aristas):,}")

    if grados:
        grado_promedio = sum(grados.values()) / len(grados)
        print(f"📈 Grado promedio: {grado_promedio:.2f}")
        print(f"🔺 Máximo grado: {max(grados.values())}")
        print(f"🔻 Mínimo grado (>0): {min([g for g in grados.values() if g > 0])}")
    else:
        print("⚠️ No se encontraron aristas para analizar grados.")

    # Guardar el grafo en un archivo .pkl
    with open("data/grafo_guardado.pkl", "wb") as f:
        pickle.dump(grafo, f)
        print("💾 Grafo guardado en 'data/grafo_guardado.pkl'")