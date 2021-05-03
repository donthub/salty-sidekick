from comm.chatter import Chatter
from comm.collector import Collector
from data.config import Config
from data.database import Database
from model.model import Model
from util.logutil import LogUtil

if __name__ == '__main__':
    LogUtil().initialize()
    config = Config()
    database = Database()
    model = Model(database)
    collector = Collector(model)

    bot = Chatter(config, collector)
    bot.start()
