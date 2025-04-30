# PROYECTO ADA  
## Primera Revisión de Avance: Carga Masiva + EDA en Python (20 puntos)

**Integrantes:**  
- Huamani Vasquez Juan Jose  
- Zela Flores Gabriel Frank  

---

## 1. Introducción

### Motivación
Las redes sociales constituyen una fuente inagotable de datos relacionales entre personas. Analizar estas estructuras permite entender cómo se forman comunidades, cómo fluye la información y qué patrones emergen a gran escala. Este proyecto busca explorar dichas dinámicas a través del análisis y visualización del grafo de la red social 'X', compuesto por 10 millones de usuarios.

### Objetivos
- Procesar eficientemente grandes volúmenes de datos (10M de registros).
- Preparar los datos para la construcción de un grafo social.
- Sentar las bases para análisis posteriores como detección de comunidades y visualización de métricas de red.

---

## 2. Carga Masiva y Preprocesamiento de Datos

### Descripción del Dataset
Se utilizaron dos archivos:
- `10_million_location.txt`: contiene latitud y longitud de cada usuario.
- `10_million_user.txt`: contiene las listas de adyacencia (usuarios seguidos por cada nodo).

### Tecnología Utilizada
- **Lenguaje**: Python 3.11  
- **Librerías**: `polars` para procesamiento eficiente en modo lazy/streaming, `logging` para trazabilidad del procesamiento.  

### Objetivo de esta etapa
- Cargar los datos de manera eficiente y escalable.
- Validar y limpiar las ubicaciones geográficas.
- Procesar las listas de adyacencia asegurando un formato estructurado y uniforme.

---

## 3. Código Explicado

A continuación se describe el proceso implementado:

```python
import polars as pl
import logging
import sys
```
Se importan las librerías necesarias. `polars` permite procesamiento en modo streaming (`lazy`), ideal para grandes volúmenes de datos.

```python
logging.basicConfig(...)
```
Se configura el logging para registrar mensajes informativos durante la ejecución.

### Carga de Archivos

```python
locations_lazy = pl.scan_csv(
    "social_network_data/10_million_location.txt",
    separator=",",
    has_header=False,
    new_columns=["latitude", "longitude"]
)
```
Carga el archivo de ubicaciones en modo `lazy`, sin cargar todos los datos en memoria.

```python
users_lazy = pl.scan_csv(
    "social_network_data/10_million_user.txt",
    separator="\n",
    has_header=False,
    new_columns=["connections"],
    truncate_ragged_lines=True
)
```
Carga la lista de adyacencias, línea por línea. La opción `truncate_ragged_lines` evita errores si hay líneas mal formateadas.

### Limpieza y Validación

```python
locations_valid = locations_lazy.filter(...)
```
Se asegura que las coordenadas estén dentro de los rangos válidos de latitud (-90 a 90) y longitud (-180 a 180).

```python
users_processed = users_lazy.with_columns([
    pl.col("connections").str.strip_chars().str.split(",")
])
```
Convierte las listas de conexiones en vectores. Se eliminan caracteres vacíos y se separan los IDs por coma.

### Ejecución y Guardado

```python
locations_final = locations_valid.collect(engine="streaming")
users_final = users_processed.collect(engine="streaming")
```
Se ejecutan las operaciones `lazy` y se recolectan los resultados de forma eficiente.

```python
locations_final.write_parquet("ubicaciones_limpias.parquet")
users_final.write_parquet("usuarios_conexiones.parquet")
```
Los datos limpios se guardan en formato `Parquet`, ideal para análisis posterior por su compresión y rapidez de lectura.

---

## 4. Resultados de la Fase de Preprocesamiento

- ✔️ Lectura y validación exitosa de los 10 millones de coordenadas.
- ✔️ Procesamiento estructurado de listas de adyacencia.
- ✔️ Datos convertidos a formato binario columnar `.parquet`, listos para análisis avanzado.

---

## 5. Próximos Pasos

- Construcción del grafo usando `networkx` o estructuras propias.
- Cálculo de métricas básicas del grafo (nodos, aristas, grado).
- Visualización básica y exploración de la estructura.
- Preparación para análisis de comunidades y caminos mínimos.

---

## 6. Conclusión

Se ha completado satisfactoriamente la primera etapa del proyecto: el preprocesamiento masivo y validación de datos de la red social 'X'. Este paso es fundamental para asegurar la calidad y eficiencia en los análisis posteriores.

---

## 7. Referencias

- [Polars Documentation](https://pola-rs.github.io/polars/)
- Dataset: Red Social 'X' - [Drive Link](https://drive.google.com/drive/folders/1XvzgZ3NKo3EruGOHDirM6bQwfc8fejpl?usp=sharing)
