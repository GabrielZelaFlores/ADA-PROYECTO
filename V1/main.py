import subprocess
import os
from logger_config import setup_logger

# Configure logger
log = setup_logger()

# Define the sequence of scripts to run
# We'll use comunidad_igraph.py for community detection by default.
SCRIPTS_TO_RUN = [
    "data_to_parquet.py",
    "calc_weight.py",
    "join_weights.py",
    "graph_construction.py",
    "comunidad_igraph.py",
    # EDA and other analyses can be run manually as they are for exploration
    # "eda.py",
    # "analisis_comunidades.py",
    # "dijkstra.py",
    # "mapa_BFS.py",
    # "mapa_comunidad.py",
    # "mapa_por_comunidad.py",
]

def run_script(script_name):
    """Executes a Python script using subprocess and logs its output."""
    script_path = os.path.join(os.path.dirname(__file__), script_name)
    if not os.path.exists(script_path):
        log.error(f"❌ Script '{script_name}' not found at '{script_path}'. Skipping.")
        return False

    log.info(f"🚀 Iniciando ejecución de: {script_name}")
    try:
        # Using sys.executable to ensure the same Python interpreter is used
        process = subprocess.Popen(
            [os.sys.executable, script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=os.path.dirname(__file__) # Execute in the V1 directory context
        )
        stdout, stderr = process.communicate()

        if stdout:
            log.info(f"Salida de {script_name}:\n{stdout}")
        if stderr:
            if process.returncode == 0:
                log.warning(f"Salida de error (pero con código 0) de {script_name}:\n{stderr}")
            else:
                log.error(f"Errores de {script_name}:\n{stderr}")

        if process.returncode == 0:
            log.info(f"✅ {script_name} completado exitosamente.")
            return True
        else:
            log.error(f"❌ {script_name} falló con código de error {process.returncode}.")
            return False
    except Exception as e:
        log.exception(f"💥 Excepción al ejecutar {script_name}: {e}")
        return False

def main():
    """
    Función principal para ejecutar el pipeline de scripts del proyecto V1.
    """
    log.info("🏁 Iniciando pipeline principal del Proyecto V1...")

    # Create necessary subdirectories if they don't exist
    # (some scripts might do this, but it's good to ensure)
    os.makedirs(os.path.join(os.path.dirname(__file__), "data", "aristas_parquet"), exist_ok=True)
    os.makedirs(os.path.join(os.path.dirname(__file__), "graficos", "BFS"), exist_ok=True)
    os.makedirs(os.path.join(os.path.dirname(__file__), "graficos", "comunidades"), exist_ok=True)
    os.makedirs(os.path.join(os.path.dirname(__file__), "graficos", "dijkstra"), exist_ok=True)

    total_scripts = len(SCRIPTS_TO_RUN)
    successful_scripts = 0

    for i, script_name in enumerate(SCRIPTS_TO_RUN):
        log.info(f"--- Paso {i+1}/{total_scripts} ---")
        if run_script(script_name):
            successful_scripts += 1
        else:
            log.error(f"Pipeline detenido debido a error en {script_name}.")
            break
            # Option: continue running other scripts if they are independent
            # log.warning(f"Continuando con el siguiente script a pesar del error en {script_name}.")
            # continue

    log.info("--- Fin del Pipeline ---")
    if successful_scripts == total_scripts:
        log.info("🎉 Todos los scripts del pipeline principal se ejecutaron exitosamente.")
    else:
        log.warning(f"⚠️ {successful_scripts}/{total_scripts} scripts del pipeline principal se completaron. "
                    f"{total_scripts - successful_scripts} fallaron o fueron omitidos.")

if __name__ == "__main__":
    # Note: Ensure that the required input data files (e.g., 10_million_location.txt)
    # are present in the V1/data/ directory before running this main script.
    log.info("=================================================================")
    log.info("== BIENVENIDO AL EJECUTOR DEL PIPELINE DEL PROYECTO V1 ==")
    log.info("=================================================================")
    log.info("Este script ejecutará la secuencia principal de procesamiento de datos y construcción del grafo.")
    log.info("Asegúrate de que los archivos de datos iniciales (ej: 10_million_location.txt) estén en V1/data/")
    log.info("-----------------------------------------------------------------\n")

    main()
