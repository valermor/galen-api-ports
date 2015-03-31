import logging
from logging import config
from galenapi.utils.logger import get_logger_config_path

logging.config.fileConfig(get_logger_config_path())
