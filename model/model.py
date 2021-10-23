from model.common import Common
from model.log import Log
from model.stats import CommonStats, PlayerStats


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
        common_stats = CommonStats(total=self.common.total)
        common_stats.print()

    def add_log(self, log):
        self.common.add_log(log)

    def get_player_stats(self, p1_name, p2_name, tier, mode, left):
        p1 = self.common.get_player(p1_name, tier)
        p2 = self.common.get_player(p2_name, tier)
        player_stats = PlayerStats(p1, p2, tier, mode, left)
        return player_stats

    def get_probability_player_name(self, p1_name, p2_name, tier):
        p1 = self.common.get_player(p1_name, tier)
        p2 = self.common.get_player(p2_name, tier)
        player_stats = PlayerStats(p1, p2, tier, mode=None, left=None)
        return player_stats.get_bet_player_name()
