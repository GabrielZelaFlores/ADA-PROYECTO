# Proyecto V2 - Análisis de Redes de Transporte

Este directorio contiene la versión 2 del proyecto de análisis de redes de transporte. Se ha estructurado el flujo de trabajo en un script principal (`main.py`) que permite ejecutar diferentes etapas del proceso de forma modular.

## Flujo de Trabajo

El proyecto se divide en tres etapas principales, cada una compuesta por varios scripts específicos:

1.  **Carga de Datos**: Esta etapa se encarga de procesar los datos crudos, construir las estructuras de datos necesarias (como grafos) y prepararlos para el análisis.
2.  **Análisis**: En esta etapa se realizan diversos análisis sobre los datos procesados. Esto incluye análisis exploratorio de datos (EDA), detección de comunidades, y algoritmos de grafos como Dijkstra y Kruskal.
3.  **Visualizaciones**: Esta etapa genera diferentes mapas y visualizaciones para representar los resultados de los análisis, como la distribución geográfica de comunidades, rutas óptimas, etc.

## `main.py`

El script `main.py` es el punto de entrada para ejecutar el flujo de trabajo del proyecto V2. Permite seleccionar qué sección o secciones del proyecto se desean ejecutar.

### Uso

Para ejecutar el script `main.py`, navega al directorio `V2` en tu terminal y utiliza el siguiente comando:

```bash
python main.py [seccion]
```

Donde `[seccion]` puede ser una de las siguientes opciones:

*   `carga`: Ejecuta todos los scripts de la sección de Carga de Datos.
*   `analisis`: Ejecuta todos los scripts de la sección de Análisis.
*   `visualizaciones`: Ejecuta todos los scripts de la sección de Visualizaciones.
*   `todo`: Ejecuta todas las secciones en orden: Carga de Datos, luego Análisis y finalmente Visualizaciones.

**Ejemplo:**

Para ejecutar solo la sección de análisis:

```bash
python main.py analisis
```

Para ejecutar todo el flujo de trabajo:

```bash
python main.py todo
```

Durante la ejecución, la consola mostrará información sobre los scripts que se están ejecutando, incluyendo el tiempo que tarda cada script y el tiempo total para cada sección completada.

### Scripts Invocados por `main.py`

A continuación, se describe brevemente cada script que es invocado por `main.py` según la sección seleccionada:

#### Sección: `carga`

*   **`data_raw_to_parquet.py`**: Convierte los datos crudos (presumiblemente CSVs u otros formatos) a formato Parquet para optimizar la lectura y almacenamiento.
*   **`data_graph_construction.py`**: Construye la estructura del grafo principal a partir de los datos procesados.
*   **`data_weights_to_parquet.py`**: Calcula y almacena los pesos (costos, distancias, etc.) de las aristas del grafo en formato Parquet.
*   **`data_asignar_comunidad.py`**: Asigna nodos del grafo a comunidades, posiblemente utilizando algún algoritmo de detección de comunidades o datos preexistentes.

#### Sección: `analisis`

*   **`analisis_eda.py`**: Realiza un Análisis Exploratorio de Datos sobre los datasets generados.
*   **`analisis_comunidades.py`**: Ejecuta análisis específicos sobre las comunidades detectadas en el grafo.
*   **`analisis_dijkstra.py`**: Implementa y ejecuta el algoritmo de Dijkstra para encontrar caminos mínimos en el grafo.
*   **`analisis_kruskal.py`**: Implementa y ejecuta el algoritmo de Kruskal para encontrar el Árbol de Expansión Mínima (MST) del grafo.

#### Sección: `visualizaciones`

*   **`mapa_BFS.py`**: Genera visualizaciones geográficas o de red utilizando los resultados de un recorrido BFS (Breadth-First Search).
*   **`mapa_comunidad.py`**: Crea mapas que muestran la distribución o estructura de las comunidades identificadas.
*   **`mapa_por_comunidad.py`**: Genera visualizaciones específicas para cada comunidad o un resumen de ellas.

## Logger

El script `main.py` y los scripts que invoca utilizan un sistema de logging configurado a través de `logger_config.py`. Los logs se guardan en `app.log` (este archivo de log podría estar en el directorio raíz o en `V2/`, dependiendo de la configuración exacta de `logger_config.py` y cómo se ejecutan los scripts). Se recomienda revisar este archivo para obtener detalles sobre la ejecución y posibles errores.

## Requisitos

Asegúrate de tener instaladas todas las dependencias listadas en el archivo `requirements.txt` dentro del directorio `V2`. Puedes instalarlas usando pip:

```bash
pip install -r requirements.txt
```
