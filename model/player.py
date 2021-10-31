import trueskill

from model.direct import Direct


class Player:

    def __init__(self, name, tier):
        self.name = name
        self.tier = tier

        self.skill = trueskill.Rating()
        self.directs = {}

        self.total_games = 0
        self.total_wins = 0
        self.total_losses = 0
        self.streak = 0
        self.upset = 0
        self.job = 0
        self.date_time = None

    def add_log(self, log):
        self.total_games += 1
        self.streak = log.p1_streak if self.name == log.p1_name else log.p2_streak
        self.date_time = log.datetime

        if self.name == log.winner:
            self.total_wins += 1
        else:
            self.total_losses += 1

        name = log.p1_name if self.name == log.p2_name else log.p2_name
        if name not in self.directs:
            self.directs[name] = Direct()

        direct = self.directs[name]

        direct.total += 1
        if log.winner == self.name:
            direct.wins += 1
        else:
            direct.losses += 1
        direct.amount += int(log.p1_amount) if self.name == log.p1_name else int(log.p2_amount)

    def get_direct(self, name):
        return Direct() if name not in self.directs else self.directs[name]
