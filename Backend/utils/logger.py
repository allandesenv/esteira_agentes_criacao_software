import logging
import sys

def setup_logger(name: str = "EsteiraAgentes"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Evita duplicar logs se chamar a função mais de uma vez
    if not logger.handlers:
        # Log no Console
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '%(asctime)s - [%(levelname)s] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        # Log em Arquivo (Auditabilidade)
        file_handler = logging.FileHandler("esteira_execution.log")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger