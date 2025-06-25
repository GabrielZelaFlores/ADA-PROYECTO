# Importación de bibliotecas necesarias
import polars as pl
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
import os
import sys
import logging
from scipy.stats import zscore
from logger_config import setup_logger

# --------------------------
# Configurar logging
# --------------------------
# Configuración básica del sistema de logging para mostrar mensajes informativos
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S"
)

# Inicialización del logger personalizado
log = setup_logger()

# --------------------------
# Función principal
# --------------------------
def main():
    try:
        # Crear carpeta para los gráficos si no existe
        os.makedirs("graficos", exist_ok=True)

        # --------------------------
        # 1. Cargar datos procesados
        # --------------------------
        log.info(" Cargando archivos Parquet procesados...")

        # Cargar datos de ubicaciones limpias
        ubicaciones = pl.read_parquet("data/ubicaciones_limpias.parquet")

        # Cargar datos de conexiones entre usuarios
        conexiones = pl.read_parquet("data/usuarios_conexiones.parquet")

        # Registrar el tamaño de los datasets cargados
        log.info(f" Ubicaciones cargadas: {ubicaciones.shape}")
        log.info(f" Conexiones cargadas: {conexiones.shape}")

        # --------------------------
        # 2. Verificar valores nulos
        # --------------------------
        log.info(" Verificando valores nulos...")

        # Mostrar conteo de valores nulos en ambos datasets
        log.info("Nulos en ubicaciones:\n%s", ubicaciones.null_count().to_pandas().to_string(index=False))
        log.info(f"Nulos en conexiones:\n{conexiones.null_count()}")

        # --------------------------
        # 3. Estadísticas Descriptivas
        # --------------------------
        log.info(" Generando estadísticas descriptivas...")

        # Generar y mostrar resumen estadístico de ubicaciones
        stats = ubicaciones.describe()
        log.info("Resumen estadístico:\n%s", stats.to_pandas().to_string(index=False))


        # --------------------------
        # 4. Outliers Geográficos (Z-score)
        # --------------------------
        log.info(" Detectando outliers geográficos con Z-score...")

        # Convertir a pandas para usar zscore
        df_geo = ubicaciones.to_pandas()

        # Calcular z-score para latitud y longitud
        df_geo["z_lat"] = zscore(df_geo["latitude"])
        df_geo["z_lon"] = zscore(df_geo["longitude"])

        # Filtrar los outliers (valores con z-score > 3 o < -3)
        df_outliers = df_geo[(df_geo["z_lat"].abs() > 3) | (df_geo["z_lon"].abs() > 3)]

        # Registrar la cantidad de outliers detectados
        log.info(f" Outliers detectados: {df_outliers.shape[0]}")
        
        # --------------------------
        # 5. Gráfico de Outliers Geográficos
        # --------------------------
        log.info(" Generando gráfico de outliers geográficos...")

        # Crear figura del scatter plot
        plt.figure(figsize=(10, 6))

        # Graficar puntos normales
        sns.scatterplot(
            data=df_geo, x="longitude", y="latitude", s=1, alpha=0.3, label="Normal"
        )

        # Graficar puntos outliers
        sns.scatterplot(
            data=df_outliers, x="longitude", y="latitude", color="red", s=10, label="Outliers"
        )

        # Añadir título y etiquetas
        plt.title("Distribución Geográfica con Outliers Destacados")
        plt.xlabel("Longitud")
        plt.ylabel("Latitud")
        plt.legend()

        # Guardar gráfico en archivo
        plt.savefig("graficos/distribucion_outliers.png", dpi=300)
        plt.close()

        # Registrar guardado exitoso
        log.info(" Guardado: graficos/distribucion_outliers.png")

        # --------------------------
        # 6. Mapa geográfico general
        # --------------------------
        log.info(" Generando gráfico de distribución general...")

        # Crear figura para el mapa de distribución general
        plt.figure(figsize=(10, 6))

        # Graficar todos los puntos de ubicación
        sns.scatterplot(
            x=ubicaciones["longitude"],
            y=ubicaciones["latitude"],
            s=1, alpha=0.4
        )

        # Añadir título y etiquetas
        plt.title("Distribución Geográfica de Usuarios")
        plt.xlabel("Longitud")
        plt.ylabel("Latitud")

        # Guardar gráfico
        plt.savefig("graficos/distribucion_geografica.png", dpi=300)
        plt.close()

        # Registrar guardado exitoso
        log.info(" Guardado: graficos/distribucion_geografica.png")

        # --------------------------
        # 7. Tabla de distribución geográfica resumida
        # --------------------------
        log.info(" Generando resumen de distribución geográfica...")

        # Crear bins de latitud y longitud agrupando por rangos de 10
        geo_bins = (
            ubicaciones
            .with_columns([
                (pl.col("latitude") // 10).alias("lat_bin"),
                (pl.col("longitude") // 10).alias("lon_bin")
            ])
            .group_by(["lat_bin", "lon_bin"])  # Agrupar por estos bins
            .agg(pl.len().alias("conteo"))     # Contar registros por grupo
            .sort("conteo", descending=True)   # Ordenar de mayor a menor
        )

        # Mostrar las 10 regiones con mayor concentración
        log.info("Top 10 regiones más densas:\n%s", geo_bins.head(10).to_pandas().to_string(index=False))


        # Mensaje de finalización exitosa del análisis
        log.info(" Análisis completado con éxito.")

    except Exception as e:
        # Captura y registro de cualquier error que ocurra durante la ejecución
        log.exception(" Error crítico durante el análisis EDA.")
        sys.exit(1)

# --------------------------
# Entry point
# --------------------------
# Ejecutar la función principal si el archivo es el principal
if __name__ == "__main__":
    main()
