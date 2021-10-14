import math

import trueskill

from model.log import Log
from model.player import Player
from model.stats import Stats


class Model:
    def __init__(self, database):
        self.database = database
        self.logs = []
        self.skills = {}
        self.stats = {}
        self.init()

    def init(self):
        db_logs = self.database.get_logs()
        for db_log in db_logs:
            log = Log(db_log[0], db_log[1], db_log[2], db_log[3], db_log[4], db_log[5], db_log[6], db_log[7], db_log[8])
            self.process_log(log)

    def add_log(self, p1_name, p1_amount, p1_streak, p2_name, p2_amount, p2_streak, tier, winner, mode):
        log = Log(p1_name, p1_amount, p1_streak, p2_name, p2_amount, p2_streak, tier, winner, mode)
        self.database.add_log(log)
        self.process_log(log)

    def process_log(self, log):
        self.logs.append(log)
        self.add_stats(log)
        self.add_skill(log)

    def add_stats(self, log):
        self.create_skill(log.p1_name, log.tier)
        self.create_skill(log.p2_name, log.tier)
        self.create_stats(log.p1_name, log.tier)
        self.create_stats(log.p2_name, log.tier)
        self.add_stats_player(log.p1_name, log.p2_name, log.tier, log.winner)
        self.add_stats_player(log.p2_name, log.p1_name, log.tier, log.winner)

    def create_stats(self, name, tier):
        if name not in self.stats:
            self.stats[name] = {}
        if tier not in self.stats[name]:
            self.stats[name][tier] = {}
        if 'upset' not in self.stats[name][tier]:
            self.stats[name][tier]['upset'] = 0
        if 'job' not in self.stats[name][tier]:
            self.stats[name][tier]['job'] = 0

    def add_stats_player(self, p1_name, p2_name, tier, winner):
        if self.calc_probability(self.skills[p1_name][tier], self.skills[p2_name][tier]) > 0.5:
            if winner == p2_name:
                self.stats[p1_name][tier]['job'] += 1
                self.stats[p2_name][tier]['upset'] += 1

    def add_skill(self, log):
        if log.p1_name != log.winner and log.p2_name != log.winner:
            return

        self.create_skill(log.p1_name, log.tier)
        self.create_skill(log.p2_name, log.tier)

        winner = log.winner
        if winner == log.p1_name:
            loser = log.p2_name
        else:
            loser = log.p1_name

        self.skills[winner][log.tier], self.skills[loser][log.tier] = trueskill.rate_1vs1(self.skills[winner][log.tier],
                                                                                          self.skills[loser][log.tier])

    def create_skill(self, name, tier):
        if name not in self.skills:
            self.skills[name] = {}
        if tier not in self.skills[name]:
            self.skills[name][tier] = trueskill.Rating()

    def get_stats(self, p1_name, p2_name, tier, mode, left):
        p1 = Player(p1_name)
        p2 = Player(p2_name)
        stats = Stats(p1, p2, tier, mode, left)

        for log in self.logs:
            if log.tier != tier:
                continue

            if log.p1_name != log.winner and log.p2_name != log.winner:
                continue

            if log.p1_name != stats.p1.name and log.p1_name != stats.p2.name and \
                    log.p2_name != stats.p1.name and log.p2_name != stats.p2.name:
                continue

            self.calc_totals(stats, log)
            self.calc_direct(stats, log)
            self.calc_streaks(stats, log)

        self.calc_stats(stats, tier)
        self.calc_skills(stats, tier)
        return stats

    def calc_totals(self, stats, log):
        if log.p1_name == stats.p1.name or log.p2_name == stats.p1.name:
            self.calc_totals_player(stats.p1, log)
        if log.p1_name == stats.p2.name or log.p2_name == stats.p2.name:
            self.calc_totals_player(stats.p2, log)

    def calc_totals_player(self, player, log):
        if log.winner == player.name:
            player.total_wins = self.increment(player.total_wins)
        else:
            player.total_losses = self.increment(player.total_losses)

    def calc_direct(self, stats, log):
        if log.p1_name == stats.p1.name and log.p2_name == stats.p2.name or \
                log.p1_name == stats.p2.name and log.p2_name == stats.p1.name:
            if log.p1_name == stats.p1.name:
                self.calc_direct_player(stats.p1, stats.p2, log.p1_amount, log.p2_amount, log.winner)
            else:
                self.calc_direct_player(stats.p1, stats.p2, log.p2_amount, log.p1_amount, log.winner)

    def calc_direct_player(self, p1, p2, p1_amount, p2_amount, winner):
        p1.direct_amount = self.get_amount(p1.direct_amount, p1_amount)
        p2.direct_amount = self.get_amount(p2.direct_amount, p2_amount)
        if winner == p1.name:
            self.calc_direct_player_wins(p1, p2)
        else:
            self.calc_direct_player_wins(p2, p1)

    def calc_direct_player_wins(self, winner, loser):
        if loser.direct_wins is None:
            loser.direct_wins = 0
        winner.direct_wins = self.increment(winner.direct_wins)

    def calc_streaks(self, stats, log):
        self.calc_streaks_player(stats.p1, log)
        self.calc_streaks_player(stats.p2, log)

    def calc_streaks_player(self, player, log):
        if log.p1_name == player.name:
            player.streak = log.p1_streak
        elif log.p2_name == player.name:
            player.streak = log.p2_streak

    def calc_stats(self, stats, tier):
        self.calc_stats_player(stats.p1, tier)
        self.calc_stats_player(stats.p2, tier)

    def calc_stats_player(self, player, tier):
        if not self.has_player_data(player):
            return

        if player.total_wins is None:
            player.total_wins = 0
            player.upset = 0
        else:
            player.upset = self.stats[player.name][tier]['upset'] / player.total_wins

        if player.total_losses is None:
            player.total_losses = 0
            player.job = 0
        else:
            player.job = self.stats[player.name][tier]['job'] / player.total_losses

    def calc_skills(self, stats, tier):
        self.calc_skills_player(stats.p1, stats.p2, tier)
        self.calc_skills_player(stats.p2, stats.p1, tier)

    def calc_skills_player(self, p1, p2, tier):
        if self.has_player_data(p1):
            p1.skill = self.skills[p1.name][tier]
            if self.has_player_data(p2):
                p1.probability = self.calc_probability(self.skills[p1.name][tier], self.skills[p2.name][tier])

    def calc_probability(self, p1_skill, p2_skill):
        delta_mu = p1_skill.mu - p2_skill.mu
        sum_sigma = p1_skill.sigma ** 2 + p2_skill.sigma ** 2
        denom = math.sqrt(2 * (trueskill.BETA * trueskill.BETA) + sum_sigma)
        return trueskill.global_env().cdf(delta_mu / denom)

    def increment(self, value):
        if value is None:
            return 1
        else:
            return value + 1

    def get_amount(self, current, added):
        if current is None:
            return int(added)
        else:
            return int(current) + int(added)

    def has_player_data(self, player):
        return player.total_wins is not None or player.total_losses is not None
