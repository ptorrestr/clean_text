import logging
from clean_text.logger import setup_logging

setup_logging( default_path='etc/logging_test.yaml', default_level=logging.DEBUG, env_key='LOG_CFG')

