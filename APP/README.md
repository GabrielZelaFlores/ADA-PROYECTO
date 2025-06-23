# Como ejecutar todo
## Pasos previos
- La estructura del proyecto es la misma que esta carpeta, debes tener la carpeta "data" y "graficos"
- En la carpeta "data" deben estar los archivos: `10_million_location.txt` y `10_million_user.txt`
- En la carpeta "graficos" no importa si hay algo o no.
- Si te falta alguna libreria instalala con `requirements.txt`

## Pasos de ejecución
1. Ejecuta **`app.py`**: esto convierte los `.txt` en `.parquet` y se guardan en `/data`.
2. Ejecuta **`eda.py`**: esto es para el analisis de los `.parquet`, es opcional hacerlo.
3. Ejecuta **`graph.py`**: Esto construye el grafo desde los `.parquet` (paso 1) y lo guarda como  `grafo_guardado.pkl` para su posterior analisis
4. Ejecuta **`comunidad.py`**: Esto usa el grafo `grafo_guardado.pkl` (paso 3) hace el analisis de comunidades y genera `grafo_con_comunidades.pkl` donde cada nodo ya tiene la comunidad a la que pertenece.
### Ahora tienes todo lo necesario
## Explora los demás archivos a tu gusto
Te indico que hace cada uno:
- **`analisis_comunidades.py`**: (Ejecuta) Tienes dos opciones 1 o 2, la primera te permite hacer un análisis de la comunidad que deesees y si no sabes cuantas hay escoge la opción dos, esta te otorga un analisis general de todas las comunidades incluyendo cuantas hay para que pruebes la opción 1.
- **`mapa_comunidad.py`**: Te permite crear un mapa simple (sin aristas) de `n` nodos, guarda el archivo en `/graficos` como `html` y luego lo visualiza en tu navegador principal.
- **`mapa_por_comunidad.py`**: Permite crear el mapa de una comunidad a tu elección y acentuando los nodos más populares de esa comunidad, puedes limitar la cantidad de nodos que se muestra y seleccionar si quieres visualizar aristas o no
- **`mapaBFS.py`**: Esto te permite crear un mapa desde el nodo de tu elección usando BFS, puedes limitar la cantidad de nodos que se muestran


**IMPORTANTE**: Todas las configuraciones que te menciono estan al inicio del codigo para que las puedas modificar a tu gusto, te muestro un ejemplo:
```python
# mapa_por_comunidad.py
# ========================
# Parámetros configurables
# ========================
comunidad_objetivo = 29       # Comunidad a visualizar
max_nodos = 500             # Límite de nodos a mostrar (None para sin límite)
mostrar_aristas = True       # Mostrar o no las conexiones (aristas)
top_n = 10                   # Número de nodos más populares a resaltar

```
**AVISO**: Las configuraciones como estan actualmente funcionan bien, si funcionase mal en las vistas, reduce el numero de nodos visibles o quita la visualizacion de aristas
