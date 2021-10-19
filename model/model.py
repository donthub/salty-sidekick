import logging

from model.log import Log
from model.common import Common
from model.stats import Stats


class Model:

    def __init__(self, database):
        self.database = database
        self.common = Common()
        self.init()

    def init(self):
        db_logs = self.database.get_logs()
        for db_log in db_logs:
            log = Log(db_log[0], db_log[1], db_log[2], db_log[3], db_log[4], db_log[5], db_log[6], db_log[7], db_log[8])
            self.add_log(log)
        logging.info(self.get_stats(None, None, None, None, None).to_text())

    def add_log(self, log):
        self.common.add_log(log)

    def get_stats(self, p1_name, p2_name, tier, mode, left):
        p1 = self.common.get_player(p1_name, tier)
        p2 = self.common.get_player(p2_name, tier)
        total = self.common.get_total()
        stats = Stats(p1, p2, total, tier, mode, left)
        return stats
