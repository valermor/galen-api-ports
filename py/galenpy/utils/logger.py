from os import path


def get_logger_config_path():
    """
    Locates the logging configuration file.
    """
    return path.join(path.dirname(__file__), 'logging.config')
