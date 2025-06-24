import polars as pl
from pathlib import Path

folder = Path("data/aristas_parquet")
parquet_files = sorted(folder.glob("aristas_lote_*.parquet"))

print(f"📦 Encontrados {len(parquet_files)} archivos para concatenar...")

df = pl.concat([pl.read_parquet(f) for f in parquet_files], how="vertical")
df.write_parquet("data/aristas_completo.parquet")
print(f"✅ Archivo único guardado con {df.shape[0]:,} aristas.")
