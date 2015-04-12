import logging
from logging import config
from galenpy.utils.logger import get_logger_config_path

__version__ = "0.1.0"

logging.config.fileConfig(get_logger_config_path())
