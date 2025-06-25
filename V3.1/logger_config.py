# logger_config.py

# Importación de los módulos necesarios
import logging
import sys

# Función para configurar y devolver un logger
def setup_logger():
    # Configuración básica del sistema de logging
    logging.basicConfig(
        level=logging.INFO,  # Nivel mínimo de mensajes que se registrarán (INFO en adelante)
        format='%(asctime)s - %(levelname)s - %(message)s',  # Formato del mensaje de log
        datefmt='%H:%M:%S',  # Formato para la hora en los logs
        handlers=[
            logging.FileHandler("app.log", mode='a'),  # Guardar los logs en un archivo (modo append)
            logging.StreamHandler(sys.stdout)          # También mostrar los logs en la consola
        ]
    )
    # Devolver el logger configurado
    return logging.getLogger(__name__)
