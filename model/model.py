from model.log import Log
from model.stats import Stats


class Model:
    def __init__(self, database):
        self.database = database
        self.logs = self.init_logs()

    def init_logs(self):
        logs = []
        db_logs = self.database.get_logs()
        for db_log in db_logs:
            log = Log(db_log[0], db_log[1], db_log[2], db_log[3], db_log[4], db_log[5], db_log[6], db_log[7])
            logs.append(log)
        return logs

    def add_log(self, p1_name, p1_amount, p1_streak, p2_name, p2_amount, p2_streak, tier, winner):
        self.database.add_log(p1_name, p1_amount, p1_streak, p2_name, p2_amount, p2_streak, tier, winner)
        self.logs.append(Log(p1_name, p1_amount, p1_streak, p2_name, p2_amount, p2_streak, tier, winner))

    def get_stats(self, p1_name, p2_name, tier):
        stats = Stats(p1_name, p2_name, tier)
        for log in self.logs:
            if log.p1_name != p1_name and log.p1_name != p2_name and log.p2_name != p1_name and log.p2_name != p2_name:
                continue

            if log.tier != tier:
                continue

            self.calc_totals(stats, log, p1_name, p2_name)
            self.calc_level1(stats, log, p1_name, p2_name)
            self.calc_streaks(stats, log, p1_name, p2_name)
        return stats

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

    def calc_level1(self, stats, log, p1_name, p2_name):
        if log.p1_name == p1_name and log.p2_name == p2_name or log.p1_name == p2_name and log.p2_name == p1_name:
            if log.p1_name == p1_name:
                stats.p1_level1_amount = self.get_amount(stats.p1_level1_amount, log.p1_amount)
                stats.p2_level1_amount = self.get_amount(stats.p2_level1_amount, log.p2_amount)
                if log.winner == p1_name:
                    stats.p1_level1_wins = self.increment(stats.p1_level1_wins)
                else:
                    stats.p2_level1_wins = self.increment(stats.p2_level1_wins)
            else:
                stats.p1_level1_amount = self.get_amount(stats.p1_level1_amount, log.p2_amount)
                stats.p2_level1_amount = self.get_amount(stats.p2_level1_amount, log.p1_amount)
                if log.winner == p2_name:
                    stats.p1_level1_wins = self.increment(stats.p1_level1_wins)
                else:
                    stats.p2_level1_wins = self.increment(stats.p2_level1_wins)

    def calc_streaks(self, stats, log, p1_name, p2_name):
        if log.p1_name == p1_name:
            stats.p1_streak = log.p1_streak
        elif log.p2_name == p1_name:
            stats.p1_streak = log.p2_streak

        if log.p1_name == p2_name:
            stats.p2_streak = log.p1_streak
        elif log.p2_name == p2_name:
            stats.p2_streak = log.p2_streak

    def increment(self, value):
        if value is None:
            return 1
        else:
            return value + 1

    def get_amount(self, current, added):
        if current is None:
            return added
        else:
            return current + added
