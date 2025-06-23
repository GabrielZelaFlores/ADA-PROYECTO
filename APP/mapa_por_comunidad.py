import pickle
import plotly.graph_objects as go
import pandas as pd

# ========================
# Parámetros configurables
# ========================
comunidad_objetivo = 29       # Comunidad a visualizar
max_nodos = 500             # Límite de nodos a mostrar (None para sin límite)
mostrar_aristas = True       # Mostrar o no las conexiones (aristas)
top_n = 10                   # Número de nodos más populares a resaltar

# ========================
# Cargar grafo
# ========================
with open("data/grafo_con_comunidades.pkl", "rb") as f:
    grafo = pickle.load(f)

if not hasattr(grafo, "comunidades"):
    raise ValueError("❌ El grafo no tiene atributo 'comunidades'. Debes calcularlas primero.")

# ========================
# Calcular in-degree
# ========================
in_degrees = {}
for u, vecinos in grafo.adj.items():
    for v in vecinos:
        in_degrees[v] = in_degrees.get(v, 0) + 1

# ========================
# Filtrar nodos válidos de la comunidad
# ========================
nodos = []
for nid, (lat, lon) in grafo.locations.items():
    if grafo.comunidades.get(nid) == comunidad_objetivo and -90 <= lat <= 90 and -180 <= lon <= 180:
        grado = in_degrees.get(nid, 0)
        nodos.append((nid, lat, lon, grado))

# Limitar nodos si es necesario
nodos = sorted(nodos, key=lambda x: -x[3])  # Ordenar por in-degree descendente
if max_nodos is not None:
    nodos = nodos[:max_nodos]

df = pd.DataFrame(nodos, columns=["id", "lat", "lon", "in_degree"])
df["size"] = df["in_degree"].apply(lambda x: 3 + (x ** 0.5))

# ========================
# Top N populares
# ========================
top_ids = df.nlargest(top_n, "in_degree")["id"].tolist()
df["label"] = df["id"].astype(str).where(df["id"].isin(top_ids), "")
df["color"] = df["id"].apply(lambda x: "crimson" if x in top_ids else "royalblue")

# ========================
# Crear nodos (Scattergeo)
# ========================
nodos_scatter = go.Scattergeo(
    lon=df["lon"],
    lat=df["lat"],
    mode="markers+text",
    marker=dict(
        size=df["size"],
        color=df["color"],
        opacity=0.8,
        line=dict(width=0.5, color="black")
    ),
    text=df["label"],
    textposition="top center",
    hovertext=[f"ID: {nid}<br>In-degree: {deg}" for nid, deg in zip(df["id"], df["in_degree"])],
    hoverinfo="text",
    name="Nodos"
)

# ========================
# Crear aristas si se habilitan
# ========================
edges = []
if mostrar_aristas:
    sample_ids = set(df["id"])
    for u in sample_ids:
        for v in grafo.adj.get(u, []):
            if v in sample_ids:
                try:
                    lat1, lon1 = grafo.locations[u]
                    lat2, lon2 = grafo.locations[v]
                    edges.append(go.Scattergeo(
                        lon=[lon1, lon2, None],
                        lat=[lat1, lat2, None],
                        mode="lines",
                        line=dict(width=0.3, color="gray"),
                        hoverinfo="none",
                        showlegend=False
                    ))
                except KeyError:
                    continue

# ========================
# Crear figura
# ========================
fig = go.Figure(data=[*edges, nodos_scatter] if mostrar_aristas else [nodos_scatter])

fig.update_layout(
    title=f"Comunidad #{comunidad_objetivo} – {len(df)} nodos, {top_n} más populares resaltados",
    showlegend=False,
    geo=dict(
        showland=True,
        landcolor="rgb(240,240,240)",
        oceancolor="rgb(210, 230, 255)",
        showocean=True,
        showcountries=True,
        countrycolor="black",
        projection_type="natural earth"
    ),
    margin=dict(l=0, r=0, t=50, b=0)
)

fig.write_html(f"graficos/comunidades/comunidad_{comunidad_objetivo}_con_aristas_{mostrar_aristas}.html")
fig.show()
