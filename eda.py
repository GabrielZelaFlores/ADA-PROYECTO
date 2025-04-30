import polars as pl
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
import os
import sys
import logging
from scipy.stats import zscore

# --------------------------
# Configurar logging
# --------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S"
)
log = logging.getLogger(__name__)

# --------------------------
# Función principal
# --------------------------
def main():
    try:
        # Crear carpeta para los gráficos
        os.makedirs("graficos", exist_ok=True)

        # --------------------------
        # 1. Cargar datos procesados
        # --------------------------
        log.info("📦 Cargando archivos Parquet procesados...")
        ubicaciones = pl.read_parquet("ubicaciones_limpias.parquet")
        conexiones = pl.read_parquet("usuarios_conexiones.parquet")

        log.info(f"✅ Ubicaciones cargadas: {ubicaciones.shape}")
        log.info(f"✅ Conexiones cargadas: {conexiones.shape}")

        # --------------------------
        # 2. Verificar valores nulos
        # --------------------------
        log.info("🔍 Verificando valores nulos...")
        log.info(f"Nulos en ubicaciones:\n{ubicaciones.null_count()}")
        log.info(f"Nulos en conexiones:\n{conexiones.null_count()}")

        # --------------------------
        # 3. Estadísticas Descriptivas
        # --------------------------
        log.info("📊 Generando estadísticas descriptivas...")
        stats = ubicaciones.describe()
        log.info(f"Resumen estadístico:\n{stats}")

        # --------------------------
        # 4. Outliers Geográficos (Z-score)
        # --------------------------
        log.info("📌 Detectando outliers geográficos con Z-score...")

        df_geo = ubicaciones.to_pandas()
        df_geo["z_lat"] = zscore(df_geo["latitude"])
        df_geo["z_lon"] = zscore(df_geo["longitude"])
        df_outliers = df_geo[(df_geo["z_lat"].abs() > 3) | (df_geo["z_lon"].abs() > 3)]

        log.info(f"🚨 Outliers detectados: {df_outliers.shape[0]}")
        
        # --------------------------
        # 5. Gráfico de Outliers Geográficos
        # --------------------------
        log.info("🖼️ Generando gráfico de outliers geográficos...")
        plt.figure(figsize=(10, 6))
        sns.scatterplot(
            data=df_geo, x="longitude", y="latitude", s=1, alpha=0.3, label="Normal"
        )
        sns.scatterplot(
            data=df_outliers, x="longitude", y="latitude", color="red", s=10, label="Outliers"
        )
        plt.title("Distribución Geográfica con Outliers Destacados")
        plt.xlabel("Longitud")
        plt.ylabel("Latitud")
        plt.legend()
        plt.savefig("graficos/distribucion_outliers.png", dpi=300)
        plt.close()
        log.info("📁 Guardado: graficos/distribucion_outliers.png")

        # --------------------------
        # 6. Mapa geográfico general
        # --------------------------
        log.info("🗺️ Generando gráfico de distribución general...")
        plt.figure(figsize=(10, 6))
        sns.scatterplot(
            x=ubicaciones["longitude"],
            y=ubicaciones["latitude"],
            s=1, alpha=0.4
        )
        plt.title("Distribución Geográfica de Usuarios")
        plt.xlabel("Longitud")
        plt.ylabel("Latitud")
        plt.savefig("graficos/distribucion_geografica.png", dpi=300)
        plt.close()
        log.info("📁 Guardado: graficos/distribucion_geografica.png")

        # --------------------------
        # 7. Tabla de distribución geográfica resumida
        # --------------------------
        log.info("📦 Generando resumen de distribución geográfica...")

        geo_bins = (
            ubicaciones
            .with_columns([
                (pl.col("latitude") // 10).alias("lat_bin"),
                (pl.col("longitude") // 10).alias("lon_bin")
            ])
            .group_by(["lat_bin", "lon_bin"])
            .agg(pl.len().alias("conteo"))
            .sort("conteo", descending=True)
        )

        log.info("📌 Top 10 regiones más densas:\n%s", geo_bins.head(10))

        log.info("✅ Análisis exploratorio completado con éxito.")

    except Exception as e:
        log.exception("❌ Error crítico durante el análisis EDA.")
        sys.exit(1)

# --------------------------
# Entry point
# --------------------------
if __name__ == "__main__":
    main()
