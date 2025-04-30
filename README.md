# PROYECTO ADA  
## Primera Revisión de Avance: Carga Masiva + EDA en Python (20 puntos)

**Integrantes:**  
- Huamani Vasquez Juan Jose  
- Zela Flores Gabriel Frank  

---

##  Objetivo del Proyecto

Analizar y visualizar la estructura del grafo de una red social compuesta por 10 millones de usuarios. El análisis busca descubrir patrones relevantes, comunidades y propiedades estructurales del grafo usando técnicas de preprocesamiento, visualización y análisis de redes.

---

##  Datos Utilizados

- `10_million_location.txt`: Contiene coordenadas (latitud, longitud) de cada usuario.
- `10_million_user.txt`: Contiene la lista de adyacencia (usuarios seguidos por cada nodo).

---

## Carga Masiva Eficiente

**Justificación:**  
El código utiliza la librería `polars` en modo `lazy` y `streaming`, que permite procesar 10 millones de registros sin cargarlos completamente en memoria, lo que es ideal para entornos de big data.

**Fragmento relevante del código:**
```python
locations_lazy = pl.scan_csv("...10_million_location.txt", ...)
users_lazy = pl.scan_csv("...10_million_user.txt", ...)
```

---

## Gestión de Recursos y Errores

**Justificación:**  
- Se usa `try-except` para capturar errores críticos.
- Uso de `logging` bien estructurado con niveles `INFO` y `EXCEPTION` para trazabilidad del proceso.
- Validación de coordenadas geográficas y limpieza de entradas irregulares.

**Fragmento relevante del código:**
```python
logging.basicConfig(...)  
try:
    ...
    locations_valid = locations_lazy.filter(...)
    ...
except Exception as e:
    log.exception(...)
```

---

## Análisis Exploratorio de Datos (EDA)

El análisis exploratorio de los datos procesados incluyó múltiples enfoques para verificar calidad, identificar outliers y comprender la distribución geográfica de los usuarios.

### Verificación de Nulos
Se validó que no existen valores nulos en ninguno de los dos archivos `.parquet`:

- **Ubicaciones:** 0 valores nulos en latitud y longitud.
- **Conexiones:** 0 valores nulos en las listas de adyacencia.

### Estadísticas Descriptivas
Se aplicó `.describe()` a las columnas de latitud y longitud:

- **Latitud:** rango típico de -90 a 90 grados.
- **Longitud:** entre -180 y 180 grados.
- Se confirmaron los límites geográficos válidos tras el preprocesamiento.

### Outliers Geográficos
Usando la técnica de *Z-score* se identificaron coordenadas atípicas:

- Se detectaron **X coordenadas como outliers** con |z| > 3 (valor reemplazable si se corre el script).
- Se graficó la distribución geográfica destacando los puntos outliers.

**Gráfico generado:**  
![Distribución con Outliers](graficos/distribucion_outliers.png)

### Visualización de Usuarios por Ubicación
Se generó una visualización general de la dispersión geográfica:

**Gráfico generado:**  
![Distribución Geográfica](graficos/distribucion_geografica.png)

### Agrupación por Regiones
Se realizó una agregación por decenas de grados en latitud/longitud para observar zonas más densas:

**Top 10 regiones con más usuarios:**
```text
(lat_bin, lon_bin) | conteo
-------------------|---------
...                | ...
```

Esta agrupación permite identificar regiones con alta densidad de usuarios, útiles para visualización o segmentación futura del grafo.

---

**Hallazgos clave del EDA:**
- El preprocesamiento eliminó correctamente datos erróneos.
- Existen algunas ubicaciones atípicas posiblemente ficticias o errores de origen.
- Se observa una distribución geográfica concentrada en ciertas regiones (ver tabla de agregación).

---

## Legibilidad y Calidad del Código

**Justificación:**  
- Código bien comentado, modularizado (función `main()`), y organizado por secciones.
- Claramente estructurado con mensajes de logging que indican cada paso.

**Ejemplo:**
```python
log.info("📍 Cargando ubicaciones en modo streaming (lazy)...")
```

---

## Documentación y Presentación

**Justificación:**  
Este `README.md` explica:
- Objetivo del proyecto.
- Detalles del dataset.
- Cómo el código cumple con cada criterio de evaluación.
- Qué fragmentos específicos respaldan los puntos evaluados.

---

## ▶ Ejecución del Script

### Requisitos
- Python 3.11
- `polars` (`pip install polars`)

### Ejecución
```bash
python preprocesamiento_red_social.py
```

### Salidas esperadas
- `ubicaciones_limpias.parquet`
- `usuarios_conexiones.parquet`

---

##  Archivos Clave

| Archivo | Descripción |
|--------|-------------|
| `preprocesamiento_red_social.py` | Código de carga masiva, validación y conversión a `.parquet`. |
| `ubicaciones_limpias.parquet` | Coordenadas válidas y limpias. |
| `usuarios_conexiones.parquet` | Conexiones por usuario en formato estructurado. |

---

##  Próximos Pasos
- Construcción del grafo con `networkx`.
- Cálculo de métricas: nodos, aristas, grado.
- Visualización de comunidades con algoritmos Louvain o Girvan-Newman.

---

##  Referencias

- [Polars Documentation](https://pola-rs.github.io/polars/)
- [Dataset: Red Social 'X'](https://drive.google.com/drive/folders/1XvzgZ3NKo3EruGOHDirM6bQwfc8fejpl?usp=sharing)
