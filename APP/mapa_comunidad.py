import pickle
import plotly.express as px
import pandas as pd
import random

# ========================
# Cargar grafo
# ========================
with open("data/grafo_con_comunidades.pkl", "rb") as f:
    grafo = pickle.load(f)

# ========================
# Verificar comunidades
# ========================
if not hasattr(grafo, "comunidades"):
    raise ValueError("❌ El grafo no tiene atributos de comunidad. Debes calcularlas antes.")

# ========================
# Muestreo de nodos
# ========================
sample_size = 10000
valid = [
    (nid, lat, lon, grafo.comunidades.get(nid, -1))
    for nid, (lat, lon) in grafo.locations.items()
    if -90 <= lat <= 90 and -180 <= lon <= 180
]

sample = random.sample(valid, min(sample_size, len(valid)))
df = pd.DataFrame(sample, columns=["id", "lat", "lon", "community"])

# ========================
# Crear gráfico con Plotly
# ========================
fig = px.scatter_geo(
    df,
    lat="lat",
    lon="lon",
    color="community",
    hover_name="id",
    projection="natural earth",
    title="Nodos sobre el mundo (coloreados por comunidad)",
    color_continuous_scale=px.colors.qualitative.Bold
)
fig.update_coloraxes(showscale=False)

# Mejoras visuales
fig.update_geos(
    showland=True,
    landcolor="rgb(240,240,240)",
    oceancolor="rgb(210, 230, 255)",
    showocean=True,
    showcountries=True,
    countrycolor="black"
)

fig.update_traces(marker=dict(size=4))
fig.write_html("graficos/grafo_coloreado_comunidad.html")
fig.show()
