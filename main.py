from comm.chatter import Chatter
from comm.collector import Collector
from data.config import Config
from data.database import Database
from model.model import Model

if __name__ == '__main__':
    config = Config()
    database = Database()
    model = Model(database)
    collector = Collector(model)
    bot = Chatter(config, collector)
    bot.start()
