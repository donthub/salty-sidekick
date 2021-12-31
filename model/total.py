from util.mode import Mode
from util.util import Util


class Total:

    def __init__(self, config):
        self.amount = config.amount
        self.amount_direct = config.amount_direct
        self.amount_close = config.amount_close
        self.stats_games = config.stats_games
        self.close_range = config.close_range

        self.tier_games = {}
        self.tier_characters = {}
        self.tier_directs = {}
        self.games = 0
        self.p1_wins = 0
        self.p1_amount = []
        self.p2_wins = 0
        self.p2_amount = []
        self.direct_games = 0
        self.direct_wins = 0
        self.direct_losses = 0
        self.direct_amount = []
        self.wl_games = 0
        self.wl_wins = 0
        self.wl_losses = 0
        self.wl_amount = []
        self.probability_games = 0
        self.probability_wins = 0
        self.probability_losses = 0
        self.probability_amount = []
        self.compare_games = 0
        self.compare_wins = 0
        self.compare_losses = 0
        self.compare_expected_amount = []
        self.compare_upset_amount = []
        self.close_games = 0
        self.close_wins = 0
        self.close_losses = 0
        self.close_expected_amount = []
        self.close_upset_amount = []
        self.far_games = 0
        self.far_wins = 0
        self.far_losses = 0
        self.far_expected_amount = []
        self.far_upset_amount = []

    def add_log(self, log, p1, p2):
        winner, loser = (p1, p2) if log.winner == log.p1_name else (p2, p1)

        self.add_log_tier(log, p1, p2)

        if log.mode != Mode.MATCHMAKING:
            return

        winner_odds = self.get_odds(log, winner, self.amount)
        winner_odds_direct = self.get_odds(log, winner, self.amount_direct)
        winner_odds_close = self.get_odds(log, winner, self.amount_close)

        self.add_log_games(log, winner_odds)
        self.add_log_direct(winner, loser, winner_odds_direct)
        self.add_log_wl(winner, loser, winner_odds)
        self.add_log_probability(winner, loser, winner_odds)
        self.add_log_compare(winner, loser, winner_odds)
        self.add_log_close(winner, loser, winner_odds_close)
        self.add_log_far(winner, loser, winner_odds)

    def add_log_tier(self, log, p1, p2):
        if log.tier not in self.tier_games:
            self.tier_games[log.tier] = 0
        if log.tier not in self.tier_characters:
            self.tier_characters[log.tier] = set()
        if log.tier not in self.tier_directs:
            self.tier_directs[log.tier] = 0

        self.tier_games[log.tier] += 1
        self.tier_characters[log.tier].add(p1.name)
        self.tier_characters[log.tier].add(p2.name)
        if p1.get_direct(p2.name).total > 0:
            self.tier_directs[log.tier] += 1

    def add_log_games(self, log, winner_odds):
        self.games += 1
        if log.winner == log.p1_name:
            self.p1_wins += 1
            self.p1_amount.append(winner_odds * self.amount)
            self.p2_amount.append(-1 * self.amount)
        if log.winner == log.p2_name:
            self.p2_wins += 1
            self.p2_amount.append(winner_odds * self.amount)
            self.p1_amount.append(-1 * self.amount)

    def add_log_direct(self, winner, loser, winner_odds):
        winner_direct = winner.get_direct(loser.name)
        if winner_direct.total == 0:
            return

        if winner_direct.wins == winner_direct.losses:
            return

        self.direct_games += 1
        if winner_direct.wins > winner_direct.losses:
            self.direct_wins += 1
            self.direct_amount.append(winner_odds * self.amount)
        else:
            self.direct_losses += 1
            self.direct_amount.append(-1 * self.amount)

    def add_log_wl(self, winner, loser, winner_odds):
        winner_wl_probability = self.get_wl_probability(winner, loser)
        if winner_wl_probability == 0.5:
            return

        self.wl_games += 1
        if winner_wl_probability > 0.5:
            self.wl_wins += 1
            self.wl_amount.append(winner_odds * self.amount)
        if winner_wl_probability < 0.5:
            self.wl_losses += 1
            self.wl_amount.append(-1 * self.amount)

    def add_log_probability(self, winner, loser, winner_odds):
        winner_probability = Util.get_probability(winner.skill, loser.skill)
        if winner_probability == 0.5:
            return

        self.probability_games += 1
        if winner_probability > 0.5:
            self.probability_wins += 1
            self.probability_amount.append(winner_odds * self.amount)
        if winner_probability < 0.5:
            self.probability_losses += 1
            self.probability_amount.append(-1 * self.amount)

    def add_log_compare(self, winner, loser, winner_odds):
        winner_wl_probability = self.get_wl_probability(winner, loser)
        winner_probability = Util.get_probability(winner.skill, loser.skill)
        if winner_wl_probability == 0.5 and winner_probability == 0.5 or \
                winner_wl_probability > 0.5 and winner_probability > 0.5 or \
                winner_wl_probability < 0.5 and winner_probability < 0.5:
            return

        self.compare_games += 1
        if winner_probability > 0.5:
            self.compare_wins += 1
            self.compare_expected_amount.append(winner_odds * self.amount)
            self.compare_upset_amount.append(-1 * self.amount)
        if winner_probability < 0.5:
            self.compare_losses += 1
            self.compare_expected_amount.append(-1 * self.amount)
            self.compare_upset_amount.append(winner_odds * self.amount)

    def add_log_close(self, winner, loser, winner_odds):
        winner_wl_probability = self.get_wl_probability(winner, loser)
        diff = self.close_range / 200
        if winner_wl_probability > 0.5 + diff or winner_wl_probability < 0.5 - diff or winner_wl_probability == 0.5:
            return

        self.close_games += 1
        if winner_wl_probability > 0.5:
            self.close_wins += 1
            self.close_expected_amount.append(winner_odds * self.amount_close)
            self.close_upset_amount.append(-1 * self.amount_close)
        if winner_wl_probability < 0.5:
            self.close_losses += 1
            self.close_expected_amount.append(-1 * self.amount_close)
            self.close_upset_amount.append(winner_odds * self.amount_close)

    def add_log_far(self, winner, loser, winner_odds):
        winner_wl_probability = self.get_wl_probability(winner, loser)
        diff = self.close_range / 200
        if 0.5 - diff < winner_wl_probability < 0.5 + diff or winner_wl_probability == 0.5:
            return

        self.far_games += 1
        if winner_wl_probability > 0.5:
            self.far_wins += 1
            self.far_expected_amount.append(winner_odds * self.amount)
            self.far_upset_amount.append(-1 * self.amount)
        if winner_wl_probability < 0.5:
            self.far_losses += 1
            self.far_expected_amount.append(-1 * self.amount)
            self.far_upset_amount.append(winner_odds * self.amount)

    def get_odds(self, log, player, amount):
        p1_amount = int(log.p1_amount) + amount if log.p1_name == player.name else int(log.p1_amount)
        p2_amount = int(log.p2_amount) + amount if log.p2_name == player.name else int(log.p2_amount)
        odds = p1_amount / p2_amount
        if log.p1_name == player.name:
            odds = 1 / odds
        return odds

    def get_wl_probability(self, p1, p2):
        p1_wl = p1.total_wins / p1.total_games if p1.total_games != 0.0 else 0.5
        p2_wl = p2.total_wins / p2.total_games if p2.total_games != 0.0 else 0.5
        return p1_wl / (p1_wl + p2_wl) if p1_wl != 0.0 or p2_wl != 0.0 else 0.5