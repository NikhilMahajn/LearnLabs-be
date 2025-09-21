import logging
logging.basicConfig(
    level=logging.INFO,  # or DEBUG
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

def get_logger(module):
    logger = logging.getLogger(module)
    return logger

