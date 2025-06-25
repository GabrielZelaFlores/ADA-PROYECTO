import argparse
import subprocess
import os
import time # Importar el módulo time
from analisis_comunidades import analisis_comunidades_main
from analisis_kruskal import ejecutar_visualizacion_mst
# Configuración del logger
from logger_config import setup_logger
logger = setup_logger()

# Definir los scripts para cada sección
SCRIPTS_CARGA_DATOS = [
    "data_raw_to_parquet.py",
    "data_weights_to_parquet.py",
    "data_graph_construction.py",
    "data_asignar_comunidad.py",
]

SCRIPTS_ANALISIS = [
    "analisis_eda.py",
    "analisis_comunidades.py",
    "analisis_dijkstra.py",
    "analisis_kruskal.py",
]

SCRIPTS_VISUALIZACIONES = [
    "mapa_BFS.py",
    "mapa_comunidad.py",
    "mapa_por_comunidad.py",
]

def ejecutar_script(script_name):
    """Ejecuta un script de Python y maneja errores."""
    script_path = os.path.join(os.path.dirname(__file__), script_name)
    if not os.path.exists(script_path):
        logger.error(f"El script {script_name} no se encontró en {script_path}.")
        print(f"Error: El script {script_name} no se encontró en {script_path}.")
        return 0 # Retornar 0 si el script no se encuentra o no se ejecuta

    start_time = time.time()
    try:
        logger.info(f"Ejecutando script: {script_name}...")
        print(f"--- Ejecutando script: {script_name} ---")
        # Usar python para ejecutar el script, en lugar de hacerlo ejecutable directamente
        result = subprocess.run(['python', script_path], capture_output=True, text=True, check=True, timeout=1800) # Timeout de 5 minutos por script
        
        end_time = time.time()
        duration = end_time - start_time
        
        logger.info(f"Salida de {script_name}:\n{result.stdout}")
        if result.stderr:
            logger.warning(f"Salida de error de {script_name}:\n{result.stderr}")
        logger.info(f"Script {script_name} completado exitosamente en {duration:.2f} segundos.")
        print(f"--- Script {script_name} finalizado en {duration:.2f} segundos ---")
        return duration
    except subprocess.TimeoutExpired:
        end_time = time.time()
        duration = end_time - start_time
        logger.error(f"El script {script_name} excedió el tiempo límite de ejecución (Timeout). Duración: {duration:.2f} segundos.")
        print(f"Error: El script {script_name} excedió el tiempo límite. Duración: {duration:.2f} segundos.")
        return duration # Retornar la duración hasta el timeout
    except subprocess.CalledProcessError as e:
        end_time = time.time()
        duration = end_time - start_time
        logger.error(f"Error al ejecutar {script_name} (Duración: {duration:.2f} segundos):")
        logger.error(f"Return code: {e.returncode}")
        logger.error(f"Output:\n{e.stdout}")
        logger.error(f"Error output:\n{e.stderr}")
        print(f"Error al ejecutar {script_name}. Ver app.log para detalles.")
        return duration # Retornar la duración hasta el error
    except FileNotFoundError:
        end_time = time.time()
        duration = end_time - start_time # Esto será casi 0
        logger.error(f"Error: El script {script_name} no fue encontrado (Duración: {duration:.2f} segundos).")
        print(f"Error: El script {script_name} no fue encontrado.")
        return duration
    except Exception as e:
        end_time = time.time()
        duration = end_time - start_time
        logger.error(f"Ocurrió un error inesperado al ejecutar {script_name} (Duración: {duration:.2f} segundos): {e}")
        print(f"Ocurrió un error inesperado al ejecutar {script_name}. Ver app.log para detalles.")
        return duration
    return 0 # En caso de que alguna lógica no retorne explícitamente

def seccion_carga_datos():
    """Ejecuta los scripts de la sección de carga de datos."""
    section_start_time = time.time()
    logger.info("Iniciando sección: Carga de Datos")
    print("\n=== Iniciando sección: Carga de Datos ===")
    total_scripts_time = 0
    for script in SCRIPTS_CARGA_DATOS:
        total_scripts_time += ejecutar_script(script)
    section_end_time = time.time()
    section_duration = section_end_time - section_start_time
    logger.info(f"Sección Carga de Datos completada en {section_duration:.2f} segundos.")
    print(f"=== Sección Carga de Datos finalizada en {section_duration:.2f} segundos (Tiempo acumulado de scripts: {total_scripts_time:.2f}s) ===")

def seccion_analisis():
    
    print("\n=== Scripts de Análisis Disponibles ===")
    for idx, script in enumerate(SCRIPTS_ANALISIS, 1):
        print(f"{idx}. {script}")
    
    seleccion = input(
        "\nIngresa el número(s) del script a ejecutar (ej. 1 o 1,3,4): "
    ).strip()

    if not seleccion:
        print(" No se seleccionó ningún script. Saliendo de sección análisis.")
        return

    try:
        indices = [int(i) - 1 for i in seleccion.split(",") if i.strip().isdigit()]
        scripts_elegidos = [SCRIPTS_ANALISIS[i] for i in indices if 0 <= i < len(SCRIPTS_ANALISIS)]
    except Exception as e:
        print(f"Error al interpretar la selección: {e}")
        return

    if not scripts_elegidos:
        print(" No se seleccionó ningún script válido.")
        return

    section_start_time = time.time()
    logger.info(f"Scripts de análisis seleccionados: {scripts_elegidos}")
    print("\n=== Ejecutando scripts seleccionados de análisis ===")

    total_scripts_time = 0
    for script in scripts_elegidos:
        if script == "analisis_comunidades.py":
            analisis_comunidades_main(script,logger)
        elif script == "analisis_kruskal.py" :
            comunidad_id = input("ID de comunidad para Kruskal: ")
            max_nodes = input("Nodos maximos a mostrar: ")
            ejecutar_visualizacion_mst(comunidad_id,max_nodes,logger)
        else:  
            total_scripts_time += ejecutar_script(script)

    section_end_time = time.time()
    section_duration = section_end_time - section_start_time

    logger.info(f"Sección Análisis completada en {section_duration:.2f} segundos.")
    print(f"\n=== Sección Análisis finalizada en {section_duration:.2f} segundos (Tiempo acumulado: {total_scripts_time:.2f}s) ===")

def seccion_visualizaciones():
    """Ejecuta los scripts de la sección de visualizaciones."""
    section_start_time = time.time()
    logger.info("Iniciando sección: Visualizaciones")
    print("\n=== Iniciando sección: Visualizaciones ===")
    total_scripts_time = 0
    for script in SCRIPTS_VISUALIZACIONES:
        total_scripts_time += ejecutar_script(script)
    section_end_time = time.time()
    section_duration = section_end_time - section_start_time
    logger.info(f"Sección Visualizaciones completada en {section_duration:.2f} segundos.")
    print(f"=== Sección Visualizaciones finalizada en {section_duration:.2f} segundos (Tiempo acumulado de scripts: {total_scripts_time:.2f}s) ===")

def main():
    parser = argparse.ArgumentParser(description="Script principal para ejecutar diferentes secciones del proyecto V2.")
    parser.add_argument(
        "seccion",
        choices=["carga", "analisis", "visualizaciones", "todo"],
        help="La sección del proyecto a ejecutar: 'carga', 'analisis', 'visualizaciones', o 'todo' para ejecutar todas las secciones en orden."
    )

    args = parser.parse_args()

    logger.info(f"Sección seleccionada: {args.seccion}")
    print(f"Sección seleccionada: {args.seccion}")

    if args.seccion == "carga":
        seccion_carga_datos()
    elif args.seccion == "analisis":
        seccion_analisis()
    elif args.seccion == "visualizaciones":
        seccion_visualizaciones()
    elif args.seccion == "todo":
        seccion_carga_datos()
        seccion_analisis()
        seccion_visualizaciones()
    else:
        logger.error("Sección no válida. Por favor, elija entre 'carga', 'analisis', 'visualizaciones', o 'todo'.")
        print("Sección no válida. Por favor, elija entre 'carga', 'analisis', 'visualizaciones', o 'todo'.")
        parser.print_help()

if __name__ == "__main__":
    main()