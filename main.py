import logging

from comm.chatter import Chatter
from comm.collector import Collector
from data.config import Config
from data.database import Database
from model.model import Model
from util.logutil import LogUtil

if __name__ == '__main__':
    LogUtil().initialize()
    logging.info('Initializing config...')
    config = Config()
    logging.info('Initializing database...')
    database = Database()
    logging.info('Initializing model...')
    model = Model(database)
    collector = Collector(database, model)

    bot = Chatter(config, collector)
    bot.start()
