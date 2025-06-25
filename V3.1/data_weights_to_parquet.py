import polars as pl
import math
import sys
from pathlib import Path
import os
from logger_config import setup_logger

# ======================
# Configuración
# ======================
log = setup_logger()
PARQUET_LOC = "data/ubicaciones_limpias.parquet"
PARQUET_USER = "data/usuarios_conexiones.parquet"
OUTPUT_DIR = Path("data/aristas_parquet")
OUTPUT_FINAL = Path("data/aristas_completo.parquet")
FLAG_FINAL = OUTPUT_DIR / "finished.flag"
BATCH_SIZE = 200_000
BORRAR_LOTES = True  # True para eliminar archivos intermedios tras unir

# ======================
# Distancia geográfica
# ======================
def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))

# ======================
# Función principal
# ======================
def main():
    try:
        log.info("Cargando ubicaciones desde Parquet...")
        locs = pl.read_parquet(PARQUET_LOC)
        coord_map = {i: (row["latitude"], row["longitude"]) for i, row in enumerate(locs.iter_rows(named=True))}

        log.info("Cargando conexiones desde Parquet...")
        users = pl.read_parquet(PARQUET_USER)

        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        log.info("Generando aristas con pesos por lotes...")
        batch, batch_num, total = [], 0, 0

        for idx, row in enumerate(users.iter_rows()):
            src = idx
            vecinos = row[0]
            if not isinstance(vecinos, list) or src not in coord_map:
                continue
            lat1, lon1 = coord_map[src]

            for v_str in vecinos:
                try:
                    tgt = int(v_str)
                    if tgt not in coord_map:
                        continue
                    lat2, lon2 = coord_map[tgt]
                    peso = haversine(lat1, lon1, lat2, lon2)
                    batch.append((src, tgt, peso))
                    total += 1
                except ValueError:
                    continue

            if len(batch) >= BATCH_SIZE:
                df = pl.DataFrame(batch, schema=["source", "target", "weight"], orient="row")
                output = OUTPUT_DIR / f"aristas_lote_{batch_num:03}.parquet"
                df.write_parquet(output)
                log.info(f"Lote {batch_num} guardado con {len(batch):,} aristas")
                batch = []
                batch_num += 1

            if idx % 100_000 == 0:
                log.info(f"Procesados {idx:,} nodos")

        # Último lote
        if batch:
            df = pl.DataFrame(batch, schema=["source", "target", "weight"], orient="row")
            output = OUTPUT_DIR / f"aristas_lote_{batch_num:03}.parquet"
            df.write_parquet(output)
            log.info(f"Último lote {batch_num} guardado con {len(batch):,} aristas")

        log.info("Concatenando lotes parquet...")
        parquet_files = sorted(OUTPUT_DIR.glob("aristas_lote_*.parquet"))
        df_all = pl.concat([pl.read_parquet(f) for f in parquet_files], how="vertical")
        df_all.write_parquet(OUTPUT_FINAL)
        log.info(f"Archivo final guardado: {OUTPUT_FINAL} con {df_all.shape[0]:,} aristas")

        if BORRAR_LOTES:
            for f in parquet_files:
                os.remove(f)
            log.info("Lotes temporales eliminados")

        # Escribir flag de finalización (opcional)
        # with open(FLAG_FINAL, "w") as f:
        #     f.write("done")

        log.info("Proceso completado correctamente")

    except Exception as e:
        log.exception("Error durante la generación de aristas.")
        sys.exit(1)

if __name__ == "__main__":
    main()
