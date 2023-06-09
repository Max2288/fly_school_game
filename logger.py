"""Logger config for project."""
import logging


def init_logger(name: str):
    """Logger initialization.

    Args:
        name (str): application's name.
    """
    logger = logging.getLogger(name)
    log_format = '%(asctime)s - %(name)s:%(lineno)s - %(levelname)s - %(message)s'
    logger.setLevel(logging.DEBUG)
    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter(log_format))
    sh.setLevel(logging.DEBUG)
    sh.setLevel(logging.DEBUG)
    logger.addHandler(sh)
    logger.debug('logger was initialized')
