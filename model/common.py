import math

import trueskill

from model.player import Player
from model.total import Total


class Common:

    def __init__(self):
        self.players = {}
        self.total = Total()

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

        if self.get_probability(loser.skill, winner.skill) > 0.5:
            winner.job += 1
            loser.upset += 1

        winner.skill, loser.skill = trueskill.rate_1vs1(winner.skill, loser.skill)

    def get_player(self, name, tier):
        if name not in self.players:
            self.players[name] = {}
        if tier not in self.players[name]:
            self.players[name][tier] = Player(name, tier)
        return self.players[name][tier]

    def get_probability(self, p1_skill, p2_skill):
        delta_mu = p1_skill.mu - p2_skill.mu
        sum_sigma = p1_skill.sigma ** 2 + p2_skill.sigma ** 2
        denom = math.sqrt(2 * (trueskill.BETA * trueskill.BETA) + sum_sigma)
        return trueskill.global_env().cdf(delta_mu / denom)
