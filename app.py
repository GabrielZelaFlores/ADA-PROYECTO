import polars as pl
import logging
import sys
from pathlib import Path

# --------------------------
# Configurar logging
# --------------------------
from logger_config import setup_logger

log = setup_logger()

# --------------------------
# Función principal
# --------------------------
def main():
    try:
        log.info(" Cargando ubicaciones en modo streaming (lazy)...")

        locations_lazy = pl.scan_csv(
            "social_network_data/10_million_location.txt",
            separator=",",
            has_header=False,
            new_columns=["latitude", "longitude"]
        )

        log.info(" Cargando usuarios (adyacencias) en modo streaming (lazy)...")

        users_lazy = pl.scan_csv(
            "social_network_data/10_million_user.txt",
            separator="\n",
            has_header=False,
            new_columns=["connections"],
            truncate_ragged_lines=True  # Previene errores por líneas irregulares
        )

        # --------------------------
        # Limpieza y validaciones
        # --------------------------
        log.info(" Validando datos de ubicación...")
        locations_valid = locations_lazy.filter(
            (pl.col("latitude").cast(pl.Float64) >= -90) & 
            (pl.col("latitude").cast(pl.Float64) <= 90) &
            (pl.col("longitude").cast(pl.Float64) >= -180) & 
            (pl.col("longitude").cast(pl.Float64) <= 180)
        )

        log.info(" Procesando listas de conexiones...")
        users_processed = users_lazy.with_columns([
            pl.col("connections")
            .str.strip_chars()
            .str.split(",")
        ])

        # --------------------------
        # Ejecutar el plan (collect)
        # --------------------------
        log.info(" Ejecutando procesamiento de ubicaciones (esto puede tardar un poco)...")
        locations_final = locations_valid.collect(engine="streaming")
        log.info(f" Ubicaciones válidas: {locations_final.shape}")

        log.info(" Ejecutando procesamiento de usuarios...")
        users_final = users_processed.collect(engine="streaming")
        log.info(f" Usuarios procesados: {users_final.shape}")

        # --------------------------
        # Guardar los resultados
        # --------------------------
        log.info(" Guardando archivos .parquet...")
        locations_final.write_parquet("ubicaciones_limpias.parquet")
        users_final.write_parquet("usuarios_conexiones.parquet")

        log.info(" Preprocesamiento terminado (eficiente y escalable).")

    except Exception as e:
        log.exception(" Ocurrió un error crítico durante el preprocesamiento.")
        sys.exit(1)

# --------------------------
# Entry point
# --------------------------
if __name__ == "__main__":
    main()
