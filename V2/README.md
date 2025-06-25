# Proyecto de Análisis de Redes Espaciales V2

## Descripción del Proyecto

Este directorio (`V2`) contiene un conjunto de scripts de Python diseñados para realizar un análisis completo de datos de redes espaciales. El flujo de trabajo abarca desde la ingesta y limpieza de datos crudos, la construcción de una representación gráfica de la red, la detección y análisis de comunidades dentro de la red, hasta la aplicación de algoritmos de grafos clásicos como Dijkstra y Kruskal. Además, se incluyen herramientas para la visualización geográfica de los nodos, comunidades y resultados de los análisis.

El proyecto está estructurado para manejar conjuntos de datos potencialmente grandes, utilizando formatos eficientes como Parquet para el almacenamiento intermedio de datos y Pickle para serializar el objeto grafo. Las visualizaciones se generan principalmente con la biblioteca Plotly.

## Estructura del Directorio

A continuación, se describen los componentes principales y archivos dentro del directorio `V2`:

*   **`data/` (Directorio)**: Aunque no listado explícitamente en `ls V2`, se infiere que es donde residen los datos crudos (ej: `10_million_location.txt`, `10_million_user.txt`), los datos procesados en formato Parquet (ej: `ubicaciones_limpias.parquet`, `usuarios_conexiones.parquet`, `aristas_completo.parquet`), y los grafos serializados (ej: `grafo_guardado.pkl`, `grafo_con_comunidades.pkl`).
*   **`graficos/` (Directorio)**: Se infiere que es donde se guardan las visualizaciones generadas, como mapas HTML (ej: `dijkstra/camino_mas_corto.html`, `grafo_top_N_comunidades.html`).
*   **`__pycache__/` (Directorio)**: Archivos de caché generados por Python.
*   **`graphObj.py`**: Define la clase `Graph`, la estructura de datos central para representar la red.
*   **`logger_config.py`**: Script para la configuración del sistema de logging utilizado por otros scripts.
*   **`requirements.txt`**: Lista las dependencias de Python necesarias para ejecutar el proyecto.
*   **Scripts de Procesamiento de Datos:**
    *   `data_raw_to_parquet.py`: Lee datos crudos de ubicación y usuarios, los limpia y los guarda en formato Parquet.
    *   `data_weights_to_parquet.py`: (Presumiblemente) Calcula o asigna pesos a las conexiones/aristas y guarda el resultado en Parquet.
    *   `data_graph_construction.py`: Construye el objeto grafo a partir de los archivos Parquet y lo guarda como un archivo Pickle.
    *   `data_asignar_comunidad.py`: (Presumiblemente) Ejecuta algoritmos de detección de comunidades sobre el grafo y guarda el grafo actualizado con esta información.
*   **Scripts de Análisis:**
    *   `analisis_comunidades.py`: Realiza análisis estadísticos sobre las comunidades detectadas en el grafo.
    *   `analisis_dijkstra.py`: Implementa el algoritmo de Dijkstra para encontrar el camino más corto entre nodos y visualiza el resultado.
    *   `analisis_kruskal.py`: (Presumiblemente) Implementa el algoritmo de Kruskal, probablemente para encontrar Árboles de Expansión Mínima.
    *   `analisis_eda.py`: (Presumiblemente) Realiza análisis exploratorio de datos sobre el grafo o sus propiedades.
*   **Scripts de Visualización:**
    *   `mapa_comunidad.py`: Genera un mapa interactivo visualizando nodos coloreados por su comunidad.
    *   `mapa_BFS.py`: (Presumiblemente) Visualiza los resultados de un recorrido BFS (Breadth-First Search) en un mapa.
    *   `mapa_por_comunidad.py`: (Presumiblemente) Genera visualizaciones de mapa específicas para comunidades individuales.
*   **`carga.log`**: Archivo de log generado durante la ejecución de los scripts (probablemente por `logger_config.py`).

## Flujo de Trabajo y Uso

El proyecto sigue un flujo de trabajo secuencial, donde la salida de un script es a menudo la entrada del siguiente:

1.  **Preparación de Datos:**
    *   Ejecutar `data_raw_to_parquet.py` para convertir los datos crudos de ubicación y conexiones de usuario en archivos Parquet limpios y estructurados.
        *   *Entrada*: Archivos de texto con datos crudos (ej: `data/10_million_location.txt`, `data/10_million_user.txt`).
        *   *Salida*: Archivos Parquet (ej: `data/ubicaciones_limpias.parquet`, `data/usuarios_conexiones.parquet`).
    *   Ejecutar `data_weights_to_parquet.py` (si es necesario para generar pesos de aristas).
        *   *Entrada*: Datos de conexiones (posiblemente `data/usuarios_conexiones.parquet`).
        *   *Salida*: Archivo Parquet con aristas ponderadas (ej: `data/aristas_completo.parquet`).

2.  **Construcción del Grafo:**
    *   Ejecutar `data_graph_construction.py` para construir el objeto grafo a partir de los datos procesados y guardarlo.
        *   *Entrada*: Archivos Parquet de ubicaciones y aristas ponderadas (ej: `data/ubicaciones_limpias.parquet`, `data/aristas_completo.parquet`).
        *   *Salida*: Archivo Pickle del grafo (ej: `data/grafo_guardado.pkl`).

3.  **Detección y Asignación de Comunidades:**
    *   Ejecutar `data_asignar_comunidad.py` para identificar comunidades dentro del grafo.
        *   *Entrada*: Archivo Pickle del grafo (ej: `data/grafo_guardado.pkl`).
        *   *Salida*: Archivo Pickle del grafo con información de comunidades (ej: `data/grafo_con_comunidades.pkl`).

4.  **Análisis y Visualización:**
    *   Una vez que el grafo (con o sin comunidades) está disponible, se pueden ejecutar los diversos scripts de análisis y visualización:
        *   `analisis_comunidades.py`: Para obtener estadísticas y detalles sobre las comunidades.
            *   *Entrada*: `data/grafo_con_comunidades.pkl`.
        *   `analisis_dijkstra.py`: Para encontrar y visualizar caminos más cortos.
            *   *Entrada*: `data/grafo_con_comunidades.pkl` (o `data/grafo_guardado.pkl` si las comunidades no son relevantes para el camino).
            *   *Salida*: Visualización HTML en `graficos/dijkstra/`.
        *   `analisis_kruskal.py`: Para análisis basados en MST.
            *   *Entrada*: Grafo Pickled.
        *   `analisis_eda.py`: Para exploración general de datos.
            *   *Entrada*: Grafo Pickled.
        *   `mapa_comunidad.py`: Para visualizar la distribución geográfica de las comunidades.
            *   *Entrada*: `data/grafo_con_comunidades.pkl`.
            *   *Salida*: Visualización HTML en `graficos/`.
        *   `mapa_BFS.py`, `mapa_por_comunidad.py`: Para otras visualizaciones específicas.
            *   *Entrada*: Grafo Pickled.

## Instrucciones de Uso

1.  **Configurar el Entorno:**
    *   Asegúrese de tener Python 3 instalado.
    *   Instale las dependencias necesarias ejecutando:
        ```bash
        pip install -r requirements.txt
        ```
    *   Verifique que los directorios `data/` y `graficos/` existan en la raíz del proyecto `V2/` (créelos si no existen) para almacenar los datos de entrada/salida y las visualizaciones.

2.  **Ejecutar los Scripts:**
    *   Siga el orden descrito en la sección "Flujo de Trabajo y Uso".
    *   Ejecute los scripts desde la línea de comandos, por ejemplo:
        ```bash
        python V2/data_raw_to_parquet.py
        python V2/data_graph_construction.py
        # ... y así sucesivamente
        ```
    *   Algunos scripts, como `analisis_comunidades.py` o `analisis_dijkstra.py`, pueden tener parámetros o requerir interacción del usuario si se ejecutan directamente (por ejemplo, para ingresar IDs de nodos o seleccionar opciones de análisis). Revise el código de cada script para detalles específicos de ejecución si es necesario.

3.  **Consultar Resultados:**
    *   Los datos procesados se encontrarán en el directorio `data/` en formato Parquet o Pickle.
    *   Las visualizaciones interactivas (archivos HTML) se guardarán en el directorio `graficos/` y pueden abrirse con cualquier navegador web.
    *   Revise el archivo `carga.log` para cualquier mensaje informativo o de error durante la ejecución de los scripts.

Este README proporciona una guía general. Para detalles específicos sobre la lógica o configuración de un script en particular, consulte los comentarios y el código fuente del script correspondiente.
