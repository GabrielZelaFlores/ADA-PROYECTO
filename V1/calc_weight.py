import polars as pl
import math
import sys
from pathlib import Path
from logger_config import setup_logger

# ======================
# Configuración
# ======================
log = setup_logger()
PARQUET_LOC = "data/ubicaciones_limpias.parquet"
PARQUET_USER = "data/usuarios_conexiones.parquet"
OUTPUT_DIR = Path("data/aristas_parquet")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
BATCH_SIZE = 100_000

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
        log.info("📦 Cargando ubicaciones desde Parquet...")
        locs = pl.read_parquet(PARQUET_LOC)
        coords = locs.to_dicts()
        coord_map = {idx: (row["latitude"], row["longitude"]) for idx, row in enumerate(coords)}

        log.info("📦 Cargando conexiones desde Parquet...")
        users = pl.read_parquet(PARQUET_USER)

        log.info("🔁 Generando aristas con pesos por lotes...")
        batch, batch_num, total = [], 0, 0

        for idx, row in enumerate(users.iter_rows()):
            src = idx
            vecinos = row[0]  # lista de strings
            if not isinstance(vecinos, list):
                continue

            if src not in coord_map:
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
                df = pl.DataFrame(batch, schema=["source", "target", "weight"])
                output = OUTPUT_DIR / f"aristas_lote_{batch_num:03}.parquet"
                df.write_parquet(str(output))
                log.info(f"✅ Lote {batch_num} guardado con {len(batch):,} aristas")
                batch = []
                batch_num += 1

            if idx % 50_000 == 0:
                log.info(f"  → Procesados {idx:,} nodos")

        if batch:
            df = pl.DataFrame(batch, schema=["source", "target", "weight"])
            output = OUTPUT_DIR / f"aristas_lote_{batch_num:03}.parquet"
            df.write_parquet(str(output))
            log.info(f"✅ Último lote {batch_num} guardado con {len(batch):,} aristas")

        log.info(f"🎉 Proceso finalizado. Total aristas: {total:,}")

    except Exception as e:
        log.exception("❌ Error al generar el archivo de aristas.")
        sys.exit(1)

if __name__ == "__main__":
    main()
