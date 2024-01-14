import logging

def get_logger():
    logger = logging.getLogger("logger")
    if logger.hasHandlers():
        return logger
    st_handler = logging.StreamHandler()
    format = "[%(levelname)s] %(message)s"
    st_handler.setFormatter(logging.Formatter(format))
    logger.setLevel(logging.INFO)
    logger.addHandler(st_handler)
    return logger