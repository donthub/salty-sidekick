import logging
import os
import sys
from logging import Formatter
from logging import StreamHandler
from logging.handlers import RotatingFileHandler


class LogUtil:

    def initialize(self):
        log_formatter = Formatter('%(asctime)s %(message)s')
        file_handler = self.init_file_handler(log_formatter)
        console_handler = self.init_console_handler(log_formatter)
        self.init_root_logger(file_handler, console_handler)

    def init_file_handler(self, log_formatter):
        log_filename = "logs/output.log"
        os.makedirs(os.path.dirname(log_filename), exist_ok=True)
        handler = RotatingFileHandler(filename=log_filename, maxBytes=1000000000, backupCount=10, encoding='utf-8')
        handler.setFormatter(log_formatter)
        return handler

    def init_console_handler(self, log_formatter):
        handler = StreamHandler(sys.stdout)
        handler.setFormatter(log_formatter)
        return handler

    def init_root_logger(self, file_handler, console_handler):
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.INFO)
        root_logger.addHandler(file_handler)
        root_logger.addHandler(console_handler)
