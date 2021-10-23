import trueskill

from model.log import Log
from model.player import Player
from model.stats.playerstats import PlayerStats
from model.stats.totalstats import TotalStats
from model.total import Total
from util.util import Util


class Model:

    def __init__(self, database):
        self.database = database
        self.players = {}
        self.total = Total()
        self.init()

    def init(self):
        db_logs = self.database.get_logs()
        for db_log in db_logs:
            log = Log(db_log[0], db_log[1], db_log[2], db_log[3], db_log[4], db_log[5], db_log[6], db_log[7], db_log[8])
            self.add_log(log)
        total_stats = TotalStats(total=self.total)
        total_stats.print()

    def add_log(self, log):
        if log.winner != log.p1_name and log.winner != log.p2_name:
            return

        p1 = self.get_player(log.p1_name, log.tier)
        p2 = self.get_player(log.p2_name, log.tier)

        p1.add_log(log)
        p2.add_log(log)

        self.total.add_log(log, p1, p2)

        p1.streak = log.p1_streak
        p2.streak = log.p2_streak

        winner, loser = (p1, p2) if log.winner == log.p1_name else (p2, p1)

        winner.total_games += 1
        winner.total_wins += 1
        loser.total_games += 1
        loser.total_losses += 1

        if Util.get_probability(loser.skill, winner.skill) > 0.5:
            loser.job += 1
            winner.upset += 1

        winner.skill, loser.skill = trueskill.rate_1vs1(winner.skill, loser.skill)

    def get_player(self, name, tier):
        if name not in self.players:
            self.players[name] = {}
        if tier not in self.players[name]:
            self.players[name][tier] = Player(name, tier)
        return self.players[name][tier]

    def get_player_stats(self, p1_name, p2_name, tier, mode, left):
        p1 = self.get_player(p1_name, tier)
        p2 = self.get_player(p2_name, tier)
        player_stats = PlayerStats(p1, p2, tier, mode, left)
        return player_stats

    def get_probability_player_name(self, p1_name, p2_name, tier):
        p1 = self.get_player(p1_name, tier)
        p2 = self.get_player(p2_name, tier)
        player_stats = PlayerStats(p1, p2, tier, mode=None, left=None)
        return player_stats.get_bet_player_name()
