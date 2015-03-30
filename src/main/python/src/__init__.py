import logging
from logging import config
from src.utils.logger import get_logger_config_path

logging.config.fileConfig(get_logger_config_path())
