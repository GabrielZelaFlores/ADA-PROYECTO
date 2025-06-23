import pickle
import plotly.graph_objects as go
import pandas as pd
from collections import deque
from graphObj import Graph
import plotly.express as px

# ============================
# Cargar grafo
# ============================
with open("data/grafo_con_comunidades.pkl", "rb") as f:
    grafo = pickle.load(f)

# ============================
# Parámetros configurables
# ============================
sample_size = 1000
start_node = 811757  # <-- nodo inicial
#start_node = max(grafo.adj, key=lambda u: len(grafo.adj[u]))  # nodo más conectado

if start_node not in grafo.adj:
    raise ValueError(f"❌ Nodo inicial {start_node} no existe en el grafo.")

# ============================
# BFS para subgrafo conectado
# ============================
visited = set()
queue = deque([start_node])

while queue and len(visited) < sample_size:
    u = queue.popleft()
    if u in visited or u not in grafo.locations:
        continue
    visited.add(u)
    for v in grafo.adj.get(u, []):
        if v not in visited and v in grafo.locations:
            queue.append(v)

sample_ids = visited

# ============================
# Calcular conexiones entrantes
# ============================
in_degree = {}
for u, vecinos in grafo.adj.items():
    for v in vecinos:
        if v in sample_ids:
            in_degree[v] = in_degree.get(v, 0) + 1

# ============================
# Construir DataFrame de nodos con comunidad
# ============================
has_com = hasattr(grafo, "comunidades")

node_data = []
for nid in sample_ids:
    lat, lon = grafo.locations[nid]
    if -90 <= lat <= 90 and -180 <= lon <= 180:
        node_data.append({
            'id': nid,
            'lat': lat,
            'lon': lon,
            'community': grafo.comunidades.get(nid, -1) if has_com else -1,
            'grado_in': in_degree.get(nid, 0)
        })

df_nodes = pd.DataFrame(node_data)

# ============================
# Asignar color por comunidad
# ============================
comunidades = sorted(df_nodes['community'].unique())
color_map = {c: px.colors.qualitative.Set3[i % len(px.colors.qualitative.Set3)] for i, c in enumerate(comunidades)}
df_nodes['color'] = df_nodes['community'].map(color_map)

# ============================
# Construir aristas
# ============================
edges = []
for u in sample_ids:
    for v in grafo.adj.get(u, []):
        if v in sample_ids:
            lat1, lon1 = grafo.locations[u]
            lat2, lon2 = grafo.locations[v]
            edges.append(go.Scattergeo(
                lon=[lon1, lon2, None],
                lat=[lat1, lat2, None],
                mode='lines',
                line=dict(width=0.3, color='gray'),
                hoverinfo='none',
                showlegend=False  # ❌ Esto oculta de la leyenda la traza de líneas
            ))

# ============================
# Crear traza de nodos (por comunidad)
# ============================
node_traces = []
for com_id, group in df_nodes.groupby('community'):
    trace = go.Scattergeo(
        lon=group['lon'],
        lat=group['lat'],
        mode='markers',
        marker=dict(
            size=group['grado_in'].apply(lambda d: 4 + d**0.4),  # tamaño escalado
            color=group['color'].iloc[0]
        ),
        hoverinfo='text',
        name=f'Comunidad {com_id}',
        text=[f"ID: {nid}<br>In: {deg}" for nid, deg in zip(group['id'], group['grado_in'])]
    )
    node_traces.append(trace)

# ============================
# Combinar todo
# ============================
fig = go.Figure()

# Añadir aristas
fig.add_traces(edges)

# Añadir nodos
for trace in node_traces:
    fig.add_trace(trace)

# Estilo del mapa
fig.update_geos(
    showcoastlines=True,
    showland=True,
    landcolor="rgb(230, 250, 230)",
    oceancolor="rgb(200, 220, 255)",
    showocean=True,
    showlakes=True,
    lakecolor="rgb(180, 210, 255)",
    showcountries=True,
    countrycolor="black"
)

fig.update_layout(
    title="Grafo con nodos coloreados por comunidad y tamaño según popularidad (in-degree)",
    margin=dict(l=0, r=0, t=40, b=0),
    legend_title="Comunidades",
    geo=dict(
        projection_type="natural earth"
    )
)

fig.write_html("graficos/BFS/grafo_bfs.html")
fig.show()
