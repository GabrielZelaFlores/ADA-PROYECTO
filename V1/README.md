# Proyecto de Análisis de Redes Sociales V1

Este directorio (`V1/`) contiene la primera versión de un proyecto enfocado en el análisis de datos de una red social simulada. El objetivo principal es construir un grafo a partir de datos de ubicación y conexión de usuarios, detectar comunidades dentro de este grafo y realizar diversos análisis y visualizaciones.

## Descripción del Flujo

El flujo de trabajo general del proyecto se puede describir en los siguientes pasos principales:

1.  **Preprocesamiento de Datos (`data_to_parquet.py`)**:
    *   Carga datos crudos de ubicación (`10_million_location.txt`) y conexiones de usuarios (`10_million_user.txt`).
    *   Limpia los datos de ubicación, filtrando coordenadas inválidas.
    *   Procesa las conexiones de usuarios, convirtiendo strings de conexiones en listas.
    *   Guarda los datos procesados en formato Parquet (`ubicaciones_limpias.parquet` y `usuarios_conexiones.parquet`) para un acceso más eficiente.
    *   Utiliza `logger_config.py` para registrar el proceso.

2.  **Cálculo de Pesos de Aristas (`calc_weight.py`)**:
    *   Carga los datos procesados de ubicaciones y conexiones.
    *   Calcula el peso de las aristas entre usuarios conectados. El peso se define como la distancia geográfica (Haversine) entre ellos.
    *   Guarda las aristas con sus pesos en archivos Parquet por lotes en el directorio `data/aristas_parquet/`.
    *   Utiliza `logger_config.py`.

3.  **Unión de Archivos de Aristas (`join_weights.py`)**:
    *   Concatena todos los archivos Parquet de aristas generados por `calc_weight.py` en un único archivo `data/aristas_completo.parquet`.

4.  **Construcción del Grafo (`graph_construction.py`)**:
    *   Lee el archivo completo de aristas (`data/aristas_completo.parquet`) y el archivo de ubicaciones (`data/ubicaciones_limpias.parquet`).
    *   Construye un objeto grafo (usando `graphObj.py`) donde los nodos son usuarios y las aristas representan conexiones ponderadas por la distancia.
    *   Almacena la información de ubicación de cada nodo.
    *   Realiza un análisis básico del grafo (top nodos por grado, grado promedio, etc.).
    *   Guarda el objeto grafo construido en `data/grafo_guardado.pkl` usando `pickle`.

5.  **Detección de Comunidades**:
    *   Se proporcionan dos implementaciones para la detección de comunidades:
        *   **`asignar_comunidad.py`**: Implementa el algoritmo de Louvain directamente usando el objeto `Graph` definido en `graphObj.py`. Carga `data/grafo_guardado.pkl`, detecta comunidades y guarda el grafo actualizado (con información de comunidades) en `data/grafo_con_comunidades.pkl`.
        *   **`comunidad_igraph.py`**: Convierte el grafo guardado (`data/grafo_guardado.pkl`) a un formato compatible con la librería `igraph`. Utiliza el algoritmo Louvain (multilevel) de `igraph` para detectar comunidades. Asigna las comunidades detectadas de nuevo al objeto grafo original y lo guarda en `data/grafo_con_comunidades.pkl`.
    *   Ambos scripts cargan el grafo, procesan comunidades y guardan el resultado. `graphObj_alt.py` parece ser una versión alternativa de `graphObj.py` posiblemente usada o probada con `asignar_comunidad.py`.

6.  **Análisis y Visualización**:
    *   **`eda.py` (Análisis Exploratorio de Datos)**:
        *   Carga los datos Parquet procesados (`ubicaciones_limpias.parquet`, `usuarios_conexiones.parquet`).
        *   Realiza verificaciones de nulos y estadísticas descriptivas.
        *   Detecta y visualiza outliers geográficos usando Z-score (`graficos/distribucion_outliers.png`).
        *   Genera un mapa de distribución geográfica general de usuarios (`graficos/distribucion_geografica.png`).
        *   Utiliza `logger_config.py`.
    *   **`analisis_comunidades.py`**:
        *   Carga el grafo con comunidades (`data/grafo_con_comunidades.pkl`).
        *   Permite analizar una comunidad específica por ID o realizar un análisis general de todas las comunidades (número de nodos, aristas internas, grado promedio, etc.).
    *   **`dijkstra.py`**:
        *   Carga el grafo con comunidades.
        *   Implementa el algoritmo de Dijkstra para encontrar el camino más corto (ponderado por distancia) entre dos nodos especificados.
        *   Visualiza el camino encontrado en un mapa interactivo usando Plotly y lo guarda en `graficos/dijkstra/camino_mas_corto.html`.
    *   **Visualización de Mapas (Plotly)**:
        *   `mapa_BFS.py`: Realiza un recorrido BFS (Breadth-First Search) a partir de un nodo inicial para obtener un subgrafo conectado. Visualiza este subgrafo en un mapa, coloreando nodos por comunidad y ajustando su tamaño según el in-degree. Guarda el mapa en `graficos/BFS/grafo_bfs.html`.
        *   `mapa_comunidad.py`: Muestra una muestra de nodos en un mapa, coloreados según la comunidad a la que pertenecen. Se enfoca en las N comunidades más grandes. Guarda el mapa en `graficos/grafo_top_N_comunidades.html`.
        *   `mapa_por_comunidad.py`: Visualiza todos los nodos pertenecientes a una comunidad específica en un mapa. Puede mostrar aristas internas y resaltar los nodos más populares (mayor in-degree) dentro de esa comunidad. Guarda el mapa en `graficos/comunidades/comunidad_X_con_aristas_Y.html`.

El script `kruskal.py` ahora contiene una implementación del algoritmo de Kruskal para encontrar el Árbol de Expansión Mínima (MST) de un grafo, sin depender de librerías externas para su lógica central. Incluye una clase `DSU` (Disjoint Set Union) y ejemplos de uso. `logger_config.py` proporciona una configuración centralizada para el logging usado por varios scripts.

Adicionalmente, se ha añadido `main.py` como un script principal para orquestar la ejecución de la secuencia de preprocesamiento y construcción del grafo.

## Instrucciones de Uso

### Prerrequisitos

*   Python 3.11 (según `dockerfile`)
*   Dependencias listadas en `requirements.txt`.

### Instalación de Dependencias

1.  Asegúrate de tener Python 3.11 y pip instalados.
2.  Navega al directorio `V1/`.
3.  Ejecuta el siguiente comando para instalar las librerías necesarias:
    ```bash
    pip install -r requirements.txt
    ```

### Ejecución de los Scripts

Existen dos formas principales de ejecutar el flujo de trabajo:

**A. Ejecución del Pipeline Principal con `main.py` (Recomendado para flujo completo)**

El script `V1/main.py` ha sido añadido para orquestar la ejecución de los pasos clave del preprocesamiento de datos, construcción del grafo y detección de comunidades.

1.  **Preparar los datos de entrada**:
    *   Asegúrate de que los archivos `10_million_location.txt` y `10_million_user.txt` estén en el subdirectorio `V1/data/`. (Estos archivos no están incluidos en el repositorio).

2.  **Ejecutar `main.py`**:
    ```bash
    python V1/main.py
    ```
    *   Este script ejecutará secuencialmente:
        1.  `data_to_parquet.py`
        2.  `calc_weight.py`
        3.  `join_weights.py`
        4.  `graph_construction.py`
        5.  `comunidad_igraph.py` (utilizado por defecto en `main.py` para la detección de comunidades)
    *   **Entradas Principales**: `V1/data/10_million_location.txt`, `V1/data/10_million_user.txt`
    *   **Salidas Principales**: `V1/data/grafo_con_comunidades.pkl`, archivos intermedios en `V1/data/`, y logs en `V1/app.log`.

**B. Ejecución Manual de Scripts Individuales**

Si necesitas ejecutar pasos específicos o utilizar alternativas (como `asignar_comunidad.py`), puedes ejecutar los scripts individualmente como se describe a continuación.

1.  **Preparar los datos de entrada**:
    *   Como se mencionó anteriormente, los archivos de datos crudos deben estar en `V1/data/`.

2.  **Preprocesamiento (`data_to_parquet.py`)**:
    ```bash
    python V1/data_to_parquet.py
    ```
    *   **Entrada**: `V1/data/10_million_location.txt`, `V1/data/10_million_user.txt`
    *   **Salida**: `V1/data/ubicaciones_limpias.parquet`, `V1/data/usuarios_conexiones.parquet`, `V1/app.log` (actualizado)

3.  **Cálculo de Pesos de Aristas (`calc_weight.py`)**:
    ```bash
    python V1/calc_weight.py
    ```
    *   **Entrada**: `V1/data/ubicaciones_limpias.parquet`, `V1/data/usuarios_conexiones.parquet`
    *   **Salida**: Archivos Parquet en `V1/data/aristas_parquet/aristas_lote_*.parquet`, `V1/app.log` (actualizado)

4.  **Unión de Archivos de Aristas (`join_weights.py`)**:
    ```bash
    python V1/join_weights.py
    ```
    *   **Entrada**: Archivos en `V1/data/aristas_parquet/`
    *   **Salida**: `V1/data/aristas_completo.parquet`

5.  **Construcción del Grafo (`graph_construction.py`)**:
    ```bash
    python V1/graph_construction.py
    ```
    *   **Entrada**: `V1/data/aristas_completo.parquet`, `V1/data/ubicaciones_limpias.parquet`
    *   **Salida**: `V1/data/grafo_guardado.pkl`

6.  **Detección de Comunidades**:
    *   Elige una de las implementaciones:
        *   Usando `asignar_comunidad.py` (implementación manual de Louvain):
            ```bash
            python V1/asignar_comunidad.py
            ```
        *   O usando `comunidad_igraph.py` (usa la librería igraph, por defecto en `main.py`):
            ```bash
            python V1/comunidad_igraph.py
            ```
    *   **Entrada**: `V1/data/grafo_guardado.pkl`
    *   **Salida**: `V1/data/grafo_con_comunidades.pkl`

7.  **Análisis y Visualización (Scripts independientes)**:
    Estos scripts generalmente se ejecutan después de que `grafo_con_comunidades.pkl` (o al menos `grafo_guardado.pkl` para Kruskal) esté disponible.
    *   **Análisis Exploratorio de Datos (`eda.py`)**:
        ```bash
        python V1/eda.py
        ```
        *   **Entrada**: `V1/data/ubicaciones_limpias.parquet`, `V1/data/usuarios_conexiones.parquet`
        *   **Salida**: Gráficos en `V1/graficos/`, `V1/app.log` (actualizado)
    *   **Análisis de Comunidades Específicas (`analisis_comunidades.py`)**:
        ```bash
        python V1/analisis_comunidades.py
        ```
        *   **Entrada**: `V1/data/grafo_con_comunidades.pkl`. Interactivo.
    *   **Algoritmo de Dijkstra (`dijkstra.py`)**:
        ```bash
        python V1/dijkstra.py
        ```
        *   **Entrada**: `V1/data/grafo_con_comunidades.pkl`. Origen/destino hardcodeados.
        *   **Salida**: `V1/graficos/dijkstra/camino_mas_corto.html`
    *   **Algoritmo de Kruskal (`kruskal.py`)**:
        El script `kruskal.py` contiene su propio ejemplo de ejecución en el bloque `if __name__ == "__main__":`.
        ```bash
        python V1/kruskal.py
        ```
        *   **Entrada (para el ejemplo interno)**: `V1/data/grafo_guardado.pkl`.
        *   **Salida**: Imprime en consola el peso total del MST y el número de aristas. No genera archivos por defecto, pero el código puede ser adaptado.
    *   **Visualizaciones de Mapas (Plotly)**:
        *   BFS (`mapa_BFS.py`):
            ```bash
            python V1/mapa_BFS.py
            ```
            *   **Entrada**: `V1/data/grafo_con_comunidades.pkl`. Nodo de inicio hardcodeado.
            *   **Salida**: `V1/graficos/BFS/grafo_bfs.html`
        *   Comunidades Top N (`mapa_comunidad.py`):
            ```bash
            python V1/mapa_comunidad.py
            ```
            *   **Entrada**: `V1/data/grafo_con_comunidades.pkl`.
            *   **Salida**: `V1/graficos/grafo_top_N_comunidades.html`.
        *   Mapa por Comunidad Específica (`mapa_por_comunidad.py`):
            ```bash
            python V1/mapa_por_comunidad.py
            ```
            *   **Entrada**: `V1/data/grafo_con_comunidades.pkl`. Comunidad objetivo hardcodeada.
            *   **Salida**: `V1/graficos/comunidades/comunidad_X_con_aristas_Y.html`.

### Uso con Docker

El `dockerfile` proporcionado permite construir una imagen de Docker con el entorno y las dependencias necesarias.

1.  **Construir la imagen Docker**:
    Desde el directorio raíz del proyecto (que contiene `V1/`), ejecuta:
    ```bash
    docker build -t proyecto-redes-v1 -f V1/dockerfile .
    ```
    *Nota: El `COPY requirements.txt .` en el Dockerfile asume que `requirements.txt` está en el contexto de build. Si el Dockerfile se mueve o el contexto cambia, esta ruta podría necesitar ajuste.*

2.  **Ejecutar un contenedor (ejemplo interactivo)**:
    ```bash
    docker run -it --rm \
        -v $(pwd)/V1/data:/app/data \
        -v $(pwd)/V1/graficos:/app/graficos \
        -v $(pwd)/V1:/app/V1 \
        proyecto-redes-v1 bash
    ```
    Esto montará los directorios locales `V1/data`, `V1/graficos` y el código fuente de `V1` dentro del contenedor, permitiéndote ejecutar los scripts y guardar los resultados en tu máquina local.
    *   Dentro del contenedor, navega a `/app/` o `/app/V1/` y ejecuta los scripts como se describió anteriormente (e.g., `python data_to_parquet.py`).
    *   Asegúrate de que los datos de entrada (`10_million_location.txt`, `10_million_user.txt`) estén en `V1/data/` en tu máquina host antes de ejecutar el contenedor con los volúmenes montados.

## Estructura de Directorios Esperada

```
V1/
├── README.md                 # Este archivo
├── analisis_comunidades.py
├── app.log                   # Archivo de log generado por los scripts
├── asignar_comunidad.py
├── calc_weight.py
├── comunidad_igraph.py
├── data/
│   ├── README.md             # README para datos (actualmente vacío)
│   ├── 10_million_location.txt # DATOS DE ENTRADA (NO EN REPO)
│   ├── 10_million_user.txt   # DATOS DE ENTRADA (NO EN REPO)
│   ├── ubicaciones_limpias.parquet # Salida de data_to_parquet.py
│   ├── usuarios_conexiones.parquet # Salida de data_to_parquet.py
│   ├── aristas_parquet/        # Salida de calc_weight.py
│   │   └── aristas_lote_*.parquet
│   ├── aristas_completo.parquet # Salida de join_weights.py
│   ├── grafo_guardado.pkl      # Salida de graph_construction.py
│   └── grafo_con_comunidades.pkl # Salida de asignar_comunidad.py o comunidad_igraph.py
├── data_to_parquet.py
├── dijkstra.py
├── dockerfile
├── eda.py
├── graficos/                 # Directorio para gráficos generados
│   ├── BFS/
│   │   └── grafo_bfs.html
│   ├── comunidades/
│   │   └── comunidad_*.html
│   ├── dijkstra/
│   │   └── camino_mas_corto.html
│   ├── distribucion_geografica.png # Salida de eda.py
│   └── distribucion_outliers.png   # Salida de eda.py
├── graphObj.py
├── graphObj_alt.py
├── graph_construction.py
├── join_weights.py
├── kruskal.py                # Implementación de Kruskal con ejemplo
├── logger_config.py
├── main.py                   # Script principal para ejecutar el pipeline
├── mapa_BFS.py
├── mapa_comunidad.py
├── mapa_por_comunidad.py
└── requirements.txt
```

Este README proporciona una visión general del proyecto V1, su flujo de trabajo y cómo utilizarlo.
