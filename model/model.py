import math

import trueskill

from model.log import Log
from model.stats import Stats


class Model:
    def __init__(self, database):
        self.database = database
        self.logs = self.init_logs()
        self.skills = self.init_skills()

    def init_logs(self):
        logs = []
        db_logs = self.database.get_logs()
        for db_log in db_logs:
            log = Log(db_log[0], db_log[1], db_log[2], db_log[3], db_log[4], db_log[5], db_log[6], db_log[7], db_log[8])
            logs.append(log)
        return logs

    def init_skills(self):
        skills = {}
        for log in self.logs:
            self.add_skill(skills, log)
        return skills

    def add_log(self, p1_name, p1_amount, p1_streak, p2_name, p2_amount, p2_streak, tier, winner, mode):
        log = Log(p1_name, p1_amount, p1_streak, p2_name, p2_amount, p2_streak, tier, winner, mode)
        self.database.add_log(log)
        self.logs.append(log)
        self.add_skill(self.skills, log)

    def get_stats(self, p1_name, p2_name, tier, mode, left):
        stats = Stats(p1_name, p2_name, tier, mode, left)

        for log in self.logs:
            if log.tier != tier:
                continue

            if log.p1_name != log.winner and log.p2_name != log.winner:
                continue

            if log.p1_name != p1_name and log.p1_name != p2_name and log.p2_name != p1_name and log.p2_name != p2_name:
                continue

            self.calc_totals(stats, log, p1_name, p2_name)
            self.calc_direct(stats, log, p1_name, p2_name)
            self.calc_streaks(stats, log, p1_name, p2_name)

        self.calc_skills(stats, self.skills, p1_name, p2_name, tier)
        return stats

    def add_skill(self, skills, log):
        if log.p1_name != log.winner and log.p2_name != log.winner:
            return

        self.create_skill(skills, log.p1_name, log.tier)
        self.create_skill(skills, log.p2_name, log.tier)

        winner = log.winner
        if winner == log.p1_name:
            loser = log.p2_name
        else:
            loser = log.p1_name

        skills[winner][log.tier], skills[loser][log.tier] = trueskill.rate_1vs1(skills[winner][log.tier],
                                                                                skills[loser][log.tier])

    def create_skill(self, skills, name, tier):
        if name not in skills:
            skills[name] = {}
        if tier not in skills[name]:
            skills[name][tier] = trueskill.Rating()

    def calc_totals(self, stats, log, p1_name, p2_name):
        if log.p1_name == p1_name or log.p2_name == p1_name:
            if log.winner == p1_name:
                stats.p1_total_wins = self.increment(stats.p1_total_wins)
            else:
                stats.p1_total_losses = self.increment(stats.p1_total_losses)

        if log.p1_name == p2_name or log.p2_name == p2_name:
            if log.winner == p2_name:
                stats.p2_total_wins = self.increment(stats.p2_total_wins)
            else:
                stats.p2_total_losses = self.increment(stats.p2_total_losses)

    def calc_direct(self, stats, log, p1_name, p2_name):
        if log.p1_name == p1_name and log.p2_name == p2_name or log.p1_name == p2_name and log.p2_name == p1_name:
            if log.p1_name == p1_name:
                stats.p1_direct_amount = self.get_amount(stats.p1_direct_amount, log.p1_amount)
                stats.p2_direct_amount = self.get_amount(stats.p2_direct_amount, log.p2_amount)
                if log.winner == p1_name:
                    stats.p1_direct_wins = self.increment(stats.p1_direct_wins)
                else:
                    stats.p2_direct_wins = self.increment(stats.p2_direct_wins)
            else:
                stats.p1_direct_amount = self.get_amount(stats.p1_direct_amount, log.p2_amount)
                stats.p2_direct_amount = self.get_amount(stats.p2_direct_amount, log.p1_amount)
                if log.winner == p2_name:
                    stats.p1_direct_wins = self.increment(stats.p1_direct_wins)
                else:
                    stats.p2_direct_wins = self.increment(stats.p2_direct_wins)

    def calc_streaks(self, stats, log, p1_name, p2_name):
        if log.p1_name == p1_name:
            stats.p1_streak = log.p1_streak
        elif log.p2_name == p1_name:
            stats.p1_streak = log.p2_streak

        if log.p1_name == p2_name:
            stats.p2_streak = log.p1_streak
        elif log.p2_name == p2_name:
            stats.p2_streak = log.p2_streak

    def calc_skills(self, stats, skills, p1_name, p2_name, tier):
        self.create_skill(skills, p1_name, tier)
        self.create_skill(skills, p2_name, tier)
        stats.p1_skill = skills[p1_name][tier]
        stats.p2_skill = skills[p2_name][tier]
        stats.p1_probability = self.calc_probability(skills[p1_name][tier], skills[p2_name][tier])
        stats.p2_probability = self.calc_probability(skills[p2_name][tier], skills[p1_name][tier])

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
