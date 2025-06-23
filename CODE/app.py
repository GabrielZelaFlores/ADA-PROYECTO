# Importación de bibliotecas necesarias
import polars as pl
import logging
import sys
from pathlib import Path

# --------------------------
# Configurar logging
# --------------------------
from logger_config import setup_logger

# Inicialización del logger personalizado
log = setup_logger()

LOCATION = "data/10_million_location.txt"
USER = "data/10_million_user.txt"

# --------------------------
# Función principal
# --------------------------
def main():
    try:
        # Log de inicio de carga de ubicaciones usando lectura perezosa (lazy)
        log.info(" Cargando ubicaciones en modo streaming (lazy)...")

        # Cargar archivo de ubicaciones usando polars en modo scan_csv (streaming/lazy)
        locations_lazy = pl.scan_csv(
            LOCATION,  # Ruta al archivo
            separator=",",  # Separador de columnas
            has_header=False,  # El archivo no tiene encabezados
            new_columns=["latitude", "longitude"]  # Nombres de columnas asignados
        )

        # Log de inicio de carga de usuarios/conexiones
        log.info(" Cargando usuarios (adyacencias) en modo streaming (lazy)...")

        # Cargar archivo de conexiones de usuarios
        users_lazy = pl.scan_csv(
            USER,  # Ruta al archivo
            separator="\n",  # Cada línea es una fila con una sola columna
            has_header=False,  # Sin encabezado
            new_columns=["connections"],  # Nombre asignado a la columna
            truncate_ragged_lines=True  # Ignora líneas que no cumplen el formato esperado
        )

        # --------------------------
        # Limpieza y validaciones
        # --------------------------
        log.info(" Validando datos de ubicación...")

        # Filtrar ubicaciones con latitudes y longitudes válidas
        locations_valid = locations_lazy.filter(
            (pl.col("latitude").cast(pl.Float64) >= -90) & 
            (pl.col("latitude").cast(pl.Float64) <= 90) &
            (pl.col("longitude").cast(pl.Float64) >= -180) & 
            (pl.col("longitude").cast(pl.Float64) <= 180)
        )

        # Log de procesamiento de conexiones
        log.info(" Procesando listas de conexiones...")

        # Limpiar y convertir strings de conexiones a listas
        users_processed = users_lazy.with_columns([
            pl.col("connections")
            .str.strip_chars()  # Eliminar espacios u otros caracteres
            .str.split(",")     # Separar por comas y convertir en listas
        ])

        # --------------------------
        # Ejecutar el plan (collect)
        # --------------------------
        log.info(" Ejecutando procesamiento de ubicaciones (esto puede tardar un poco)...")

        # Ejecutar la carga perezosa y recolectar el resultado en memoria
        locations_final = locations_valid.collect(engine="streaming")

        # Mostrar tamaño final de ubicaciones procesadas
        log.info(f" Ubicaciones válidas: {locations_final.shape}")

        # Ejecutar procesamiento de usuarios y recolectar
        log.info(" Ejecutando procesamiento de usuarios...")
        users_final = users_processed.collect(engine="streaming")

        # Mostrar tamaño final de conexiones procesadas
        log.info(f" Usuarios procesados: {users_final.shape}")

        # --------------------------
        # Guardar los resultados
        # --------------------------
        log.info(" Guardando archivos .parquet...")

        # Guardar ubicaciones validadas en formato Parquet
        locations_final.write_parquet("data/ubicaciones_limpias.parquet")

        # Guardar conexiones procesadas en formato Parquet
        users_final.write_parquet("data/usuarios_conexiones.parquet")

        # Mensaje final de éxito
        log.info(" Preprocesamiento terminado (eficiente y escalable).")

    except Exception as e:
        # Captura de errores y log del fallo
        log.exception(" Ocurrió un error crítico durante el preprocesamiento.")
        sys.exit(1)

# --------------------------
# Entry point
# --------------------------
# Ejecutar función principal si el script es ejecutado directamente
if __name__ == "__main__":
    main()
