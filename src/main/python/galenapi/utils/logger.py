from os import path


def get_logger_config_path():
    """
    Locates the logging configuration file.
    """
    #TODO it will need to point to config path when released as a lib.
    return path.join(path.dirname(__file__), 'logging.config')
