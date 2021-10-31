from util.mode import Mode
from util.util import Util


class Total:

    def __init__(self, bet_amount=200000, bet_games=10000):
        self.bet_amount = bet_amount
        self.bet_games = bet_games

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

    def add_log(self, log, p1, p2):
        winner, loser = (p1, p2) if log.winner == log.p1_name else (p2, p1)

        self.add_log_tier(log, p1, p2)

        winner_odds = self.get_odds(log, winner)

        self.add_log_games(log, winner_odds)
        self.add_log_direct(log, winner, loser, winner_odds)
        self.add_log_wl(log, winner, loser, winner_odds)
        self.add_log_probability(log, winner, loser, winner_odds)

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
            self.p1_amount.append(winner_odds * self.bet_amount)
            self.p2_amount.append(-1 * self.bet_amount)
        if log.winner == log.p2_name:
            self.p2_wins += 1
            self.p2_amount.append(winner_odds * self.bet_amount)
            self.p1_amount.append(-1 * self.bet_amount)

    def add_log_direct(self, log, winner, loser, winner_odds):
        winner_direct = winner.get_direct(loser.name)
        if winner_direct.total == 0:
            return

        if winner_direct.wins == winner_direct.losses:
            return

        self.direct_games += 1
        if winner_direct.wins > winner_direct.losses:
            self.direct_wins += 1
            if log.mode == Mode.MATCHMAKING:
                self.direct_amount.append(winner_odds * self.bet_amount)
        else:
            self.direct_losses += 1
            if log.mode == Mode.MATCHMAKING:
                self.direct_amount.append(-1 * self.bet_amount)

    def add_log_wl(self, log, winner, loser, winner_odds):
        winner_wl = winner.total_wins / winner.total_games if winner.total_games != 0.0 else 0.5
        loser_wl = loser.total_wins / loser.total_games if loser.total_games != 0.0 else 0.5

        winner_wl_probability = winner_wl / (winner_wl + loser_wl) if winner_wl != 0.0 or loser_wl != 0.0 else 0.5
        if winner_wl_probability == 0.5:
            if log.mode == Mode.MATCHMAKING:
                self.wl_amount.append(0)
            return

        self.wl_games += 1
        if winner_wl_probability > 0.5:
            self.wl_wins += 1
            if log.mode == Mode.MATCHMAKING:
                self.wl_amount.append(winner_odds * self.bet_amount)
        if winner_wl_probability < 0.5:
            self.wl_losses += 1
            if log.mode == Mode.MATCHMAKING:
                self.wl_amount.append(-1 * self.bet_amount)

    def add_log_probability(self, log, winner, loser, winner_odds):
        winner_probability = Util.get_probability(winner.skill, loser.skill)
        if winner_probability == 0.5:
            if log.mode == Mode.MATCHMAKING:
                self.probability_amount.append(0)
            return

        self.probability_games += 1
        if winner_probability > 0.5:
            self.probability_wins += 1
            if log.mode == Mode.MATCHMAKING:
                self.probability_amount.append(winner_odds * self.bet_amount)
        if winner_probability < 0.5:
            self.probability_losses += 1
            if log.mode == Mode.MATCHMAKING:
                self.probability_amount.append(-1 * self.bet_amount)

    def get_odds(self, log, player):
        p1_amount = int(log.p1_amount) + self.bet_amount if log.p1_name == player.name else int(log.p1_amount)
        p2_amount = int(log.p2_amount) + self.bet_amount if log.p2_name == player.name else int(log.p2_amount)
        odds = p1_amount / p2_amount
        if log.p1_name == player.name:
            odds = 1 / odds
        return odds
