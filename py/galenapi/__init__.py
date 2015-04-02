import logging
from logging import config
from galenapi.utils.logger import get_logger_config_path

__version__ = "0.1.0"

logging.config.fileConfig(get_logger_config_path())
