# logger_config.py
import logging
import sys

def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S',
        handlers=[
            logging.FileHandler("app.log", mode='a'),  # Append al archivo log
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)
