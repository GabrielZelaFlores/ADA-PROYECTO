# Proyecto de Análisis de Redes Espaciales V2

## 🧠 ¿De qué trata este proyecto?

Este repositorio contiene un conjunto de scripts en Python diseñados para realizar un análisis completo sobre **redes espaciales**. El proceso abarca desde la **lectura y limpieza de datos crudos**, la **construcción del grafo**, la **detección de comunidades**, hasta la aplicación de algoritmos clásicos como **Dijkstra** y **Kruskal**, incluyendo también herramientas para visualizar los resultados en mapas interactivos.

Se ha pensado en un flujo de trabajo modular y escalable, capaz de manejar grandes volúmenes de datos. Para ello se utilizan formatos eficientes como **Parquet** para almacenamiento intermedio y **Pickle** para guardar el grafo ya procesado. Las visualizaciones se generan principalmente con **Plotly**.

---

## 📁 Estructura del proyecto

Aquí te explicamos qué encontrarás dentro del directorio `V2`:

### Directorios principales

* `data/`: Aquí se guardan tanto los datos crudos (por ejemplo, `10_million_location.txt`) como los procesados (`.parquet`, `.pkl`).
* `graficos/`: Contiene las visualizaciones generadas (mapas, recorridos, etc.) en formato HTML.
* `__pycache__/`: Caché generada automáticamente por Python.

### Archivos principales

* `graphObj.py`: Define la clase `Graph`, que representa la estructura principal del grafo.
* `logger_config.py`: Configura el sistema de logs del proyecto.
* `requirements.txt`: Lista de librerías necesarias.

### Scripts para procesar los datos

* `data_raw_to_parquet.py`: Limpia los datos crudos y los convierte a formato Parquet.
* `data_weights_to_parquet.py`: Asigna pesos a las conexiones y guarda el resultado.
* `data_graph_construction.py`: Crea el grafo a partir de los datos limpios y lo guarda como Pickle.
* `data_asignar_comunidad.py`: Aplica algoritmos de detección de comunidades sobre el grafo.

### Scripts de análisis

* `analisis_comunidades.py`: Realiza estadísticas y análisis de las comunidades encontradas.
* `analisis_dijkstra.py`: Calcula el camino más corto entre nodos y lo visualiza.
* `analisis_kruskal.py`: Aplica el algoritmo de Kruskal (por ejemplo, para encontrar árboles de expansión mínima).
* `analisis_eda.py`: Exploración general de los datos (EDA).

### Scripts de visualización

* `mapa_comunidad.py`: Muestra los nodos en el mapa según la comunidad a la que pertenecen.
* `mapa_BFS.py`: Visualiza recorridos BFS.
* `mapa_por_comunidad.py`: Permite ver en detalle comunidades específicas en un mapa.

---

## 🔁 Flujo de trabajo recomendado

Para aprovechar todo el potencial del proyecto, sigue este orden:

1. **Preparar los datos:**

   ```bash
   python V2/data_raw_to_parquet.py
   python V2/data_weights_to_parquet.py
   ```

2. **Construir el grafo:**

   ```bash
   python V2/data_graph_construction.py
   ```

3. **Detectar comunidades:**

   ```bash
   python V2/data_asignar_comunidad.py
   ```

4. **Analizar y visualizar:**

   ```bash
   python V2/analisis_comunidades.py
   python V2/analisis_dijkstra.py
   python V2/analisis_kruskal.py
   python V2/mapa_comunidad.py
   ```

Cada uno de estos scripts generará archivos intermedios en `data/` y visualizaciones en `graficos/`.

---

## ⚙️ ¿Cómo empezar?

1. **Prepara tu entorno:**

   Asegúrate de tener Python 3 instalado. Luego, instala los paquetes necesarios:

   ```bash
   pip install -r requirements.txt
   ```

2. **Crea los directorios si no existen:**

   ```bash
   mkdir -p data graficos
   ```

3. **Ejecuta los scripts siguiendo el flujo de trabajo.**

4. **Consulta los resultados:**

   * Los datos procesados estarán en `data/`.
   * Las visualizaciones (mapas interactivos en HTML) se guardan en `graficos/` y pueden abrirse en cualquier navegador.
   * El archivo `carga.log` puede ayudarte a revisar mensajes de error o progreso.

---
