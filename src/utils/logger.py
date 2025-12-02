import logging


def get_logger(name=__name__):
    """
    Get or create a logger instance with INFO level.

    Args:
        name: Logger name (defaults to module name __name__)

    Returns:
        logging.Logger: Configured logger instance set to INFO level
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger