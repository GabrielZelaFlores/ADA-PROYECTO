import pickle
import plotly.graph_objects as go
import pandas as pd

# ========================
# Parámetros configurables
comunidad_objetivo = 27     # Comunidad a visualizar
# ========================
max_nodos = 1000           # Límite de nodos a mostrar (None para sin límite)
mostrar_aristas = True      # Mostrar o no las conexiones (aristas)
top_n = 10                   # Número de nodos más populares a resaltar

# ========================
# Cargar grafo
# ========================
with open("data/grafo_con_comunidades.pkl", "rb") as f:
    grafo = pickle.load(f)

if not hasattr(grafo, "comunidades"):
    raise ValueError("ERROR: El grafo no tiene atributo 'comunidades'.")

# ========================
# Calcular in-degree considerando pesos
# ========================
in_degrees = {}
for u, vecinos in grafo.adj.items():
    for v, _ in vecinos:  # v es una tupla (destino, peso)
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
df["size"] = df["in_degree"].apply(lambda x: 3 + (x ** 0.4))

# ========================
# Top N populares
# ========================
top_ids = df.nlargest(top_n, "in_degree")["id"].tolist()

df_top = df[df["id"].isin(top_ids)].copy()
df_main = df[~df["id"].isin(top_ids)].copy()

# ========================
# Crear nodos normales
# ========================
nodos_main = go.Scattergeo(
    lon=df_main["lon"],
    lat=df_main["lat"],
    mode="markers",
    marker=dict(
        size=df_main["size"],
        color="royalblue",
        opacity=0.6,
        line=dict(width=0.3, color="black")
    ),
    hovertext=[
        f"ID: {nid}<br>In-degree: {deg}" for nid, deg in zip(df_main["id"], df_main["in_degree"])
    ],
    hoverinfo="text",
    name="Nodos"
)

# ========================
# Crear nodos destacados
# ========================
nodos_top = go.Scattergeo(
    lon=df_top["lon"],
    lat=df_top["lat"],
    mode="markers+text",
    marker=dict(
        size=df_top["size"] + 2,
        color="crimson",
        opacity=1.0,
        line=dict(width=1, color="black")
    ),
    text=df_top["id"].astype(str),
    textposition="top center",
    hovertext=[
        f"ID: {nid}<br>In-degree: {deg}" for nid, deg in zip(df_top["id"], df_top["in_degree"])
    ],
    hoverinfo="text",
    name=f"Top {top_n}"
)

# ========================
# Crear aristas si están habilitadas
# ========================
edges = []
if mostrar_aristas:
    sample_ids = set(df["id"])
    for u in sample_ids:
        for v, _ in grafo.adj.get(u, []):
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
fig = go.Figure(
    data=[*edges, nodos_main, nodos_top] if mostrar_aristas else [nodos_main, nodos_top]
)

fig.update_layout(
    title=f"Comunidad #{comunidad_objetivo} – {len(df)} nodos, top {top_n} más populares resaltados",
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
