import pickle
import plotly.express as px
import pandas as pd
import random
from collections import Counter
import colorsys

# ========================
# FUNCIONES DE APOYO
# ========================
def generar_colores_distintos(n):
    colores = []
    for i in range(n):
        h = i / n
        r, g, b = colorsys.hsv_to_rgb(h, 0.65, 0.9)
        colores.append(f"rgb({int(r*255)}, {int(g*255)}, {int(b*255)})")
    return colores

def formatear_nombre_comunidad(com, size):
    return f"Comunidad {com} ({size:,} nodos)"

# ========================
# Cargar grafo
# ========================
with open("data/grafo_con_comunidades.pkl", "rb") as f:
    grafo = pickle.load(f)

if not hasattr(grafo, "comunidades"):
    raise ValueError("ERROR: El grafo no tiene atributo 'comunidades'.")

# ========================
# Muestreo y DataFrame
# ========================
sample_size = 100_000
valid = [
    (nid, lat, lon, grafo.comunidades.get(nid, -1))
    for nid, (lat, lon) in grafo.locations.items()
    if -90 <= lat <= 90 and -180 <= lon <= 180
]

sample = random.sample(valid, min(sample_size, len(valid)))
df = pd.DataFrame(sample, columns=["id", "lat", "lon", "community"])
df["community"] = df["community"].astype(str)

# ========================
# Filtrar top N comunidades más grandes
# ========================
top_n = 50
conteo = Counter(df["community"])
top_comunidades = conteo.most_common(top_n)

# Mapa de comunidad original → nombre formateado
comunidad_nombre = {
    com: formatear_nombre_comunidad(com, size)
    for com, size in top_comunidades
}

df_top = df[df["community"].isin(comunidad_nombre.keys())].copy()
df_top["Community"] = df_top["community"].map(comunidad_nombre)

# ========================
# Asignar colores a comunidades top
# ========================
colores = generar_colores_distintos(top_n)
color_discrete_map = {
    comunidad_nombre[com]: colores[i]
    for i, (com, _) in enumerate(top_comunidades)
}

# ========================
# Graficar
# ========================
fig = px.scatter_geo(
    df_top,
    lat="lat",
    lon="lon",
    color="Community",
    hover_name="id",
    projection="natural earth",
    title=f"Nodos de las {top_n} comunidades más grandes",
    color_discrete_map=color_discrete_map
)

fig.update_traces(marker=dict(size=4))
fig.update_geos(
    showland=True,
    landcolor="rgb(240,240,240)",
    oceancolor="rgb(210,230,255)",
    showocean=True,
    showcountries=True,
    countrycolor="black"
)

fig.write_html(f"graficos/grafo_top_{top_n}_comunidades.html")
fig.show()
