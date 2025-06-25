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
mostrar_aristas = True
sample_size = 1000
start_node = 2572385  # <-- nodo inicial

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
    for v, _ in grafo.adj.get(u, []):  # corregido para extraer el nodo destino
        if v not in visited and v in grafo.locations:
            queue.append(v)

sample_ids = visited

# ============================
# Calcular conexiones entrantes
# ============================
in_degree = {}
for u, vecinos in grafo.adj.items():
    for v, _ in vecinos:
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
colores_base = px.colors.qualitative.Set3 + px.colors.qualitative.Pastel + px.colors.qualitative.Vivid
color_map = {c: colores_base[i % len(colores_base)] for i, c in enumerate(comunidades)}
df_nodes['color'] = df_nodes['community'].map(color_map)

# ============================
# Construir aristas
# ============================
edges = []
if mostrar_aristas:
    for u in sample_ids:
        for v, _ in grafo.adj.get(u, []):
            if v in sample_ids:
                lat1, lon1 = grafo.locations[u]
                lat2, lon2 = grafo.locations[v]
                edges.append(go.Scattergeo(
                    lon=[lon1, lon2, None],
                    lat=[lat1, lat2, None],
                    mode='lines',
                    line=dict(width=0.3, color='gray'),
                    hoverinfo='none',
                    showlegend=False
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
            size=group['grado_in'].apply(lambda d: 4 + d**0.4),
            color=group['color'].iloc[0],
            opacity=0.9,
            line=dict(width=0.5, color="black")
        ),
        hoverinfo='text',
        name=f'Comunidad {com_id}',
        text=[f"ID: {nid}<br>In-degree: {deg}" for nid, deg in zip(group['id'], group['grado_in'])]
    )
    node_traces.append(trace)

# ============================
# Combinar todo
# ============================
# ============================
# Resaltar el nodo inicial
# ============================
if start_node in df_nodes['id'].values:
    nodo_inicio = df_nodes[df_nodes['id'] == start_node].iloc[0]
    start_trace = go.Scattergeo(
        lon=[nodo_inicio['lon']],
        lat=[nodo_inicio['lat']],
        mode='markers+text',
        marker=dict(
            size=12,
            color='gold',
            line=dict(width=2, color='black')
        ),
        text=["Start"],
        textposition="bottom center",
        hoverinfo="text",
        hovertext=f"ID: {start_node}<br>Inicio del BFS",
        name="Nodo inicial"
    )
    node_traces.append(start_trace)

fig = go.Figure()
fig.add_traces(edges)
fig.add_traces(node_traces)

# ============================
# Estilo del mapa
# ============================
fig.update_geos(
    showcoastlines=True,
    showland=True,
    landcolor="rgb(240,240,240)",
    oceancolor="rgb(210,230,255)",
    showocean=True,
    showlakes=True,
    lakecolor="rgb(180, 210, 255)",
    showcountries=True,
    countrycolor="black"
)

fig.update_layout(
    title="Grafo (BFS) – Nodos coloreados por comunidad y tamaño según in-degree",
    margin=dict(l=0, r=0, t=40, b=0),
    legend_title="Comunidades",
    geo=dict(
        projection_type="natural earth"
    )
)

fig.write_html("graficos/BFS/grafo_bfs.html")
fig.show()
