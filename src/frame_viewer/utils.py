import logging

def get_logger():
    """Get logger.
    Get same name logger and set format and so on.
    """
    logger = logging.getLogger("logger")
    if logger.hasHandlers():
        return logger
    st_handler = logging.StreamHandler()
    format = "[%(levelname)s] %(message)s"
    st_handler.setFormatter(logging.Formatter(format))
    logger.setLevel(logging.INFO)
    logger.addHandler(st_handler)
    return logger