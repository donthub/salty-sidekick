import logging
import sys
from logging import Formatter
from logging import StreamHandler
from logging.handlers import RotatingFileHandler


class LogUtil:

    def initialize(self):
        log_formatter = Formatter('%(asctime)s %(message)s')
        file_handler = RotatingFileHandler(filename='logs/app.log', maxBytes=1000000000, backupCount=10, encoding='utf-8')
        file_handler.setFormatter(log_formatter)
        console_handler = StreamHandler(sys.stdout)
        console_handler.setFormatter(log_formatter)
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.INFO)
        root_logger.addHandler(file_handler)
        root_logger.addHandler(console_handler)
