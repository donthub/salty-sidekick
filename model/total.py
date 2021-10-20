import math

import trueskill


class Total:

    def __init__(self, probability_threshold=0.0, games_threshold=10, bet_amount=100000, target_amount=8000000):
        self.probability_threshold = probability_threshold
        self.games_threshold = games_threshold
        self.bet_amount = bet_amount
        self.target_amount = target_amount

        self.games = 0
        self.target_games = 0
        self.p1_wins = 0
        self.p1_wins_amount = 0
        self.p2_wins = 0
        self.p2_wins_amount = 0
        self.wl_games = 0
        self.wl_wins = 0
        self.wl_equals = 0
        self.wl_losses = 0
        self.wl_wins_odds = 0
        self.wl_wins_amount = 0
        self.wl_losses_odds = 0
        self.wl_losses_amount = 0
        self.probability_games = 0
        self.probability_wins = 0
        self.probability_wins_amount = 0
        self.probability_wins_amount_lowest = 0
        self.probability_equals = 0
        self.probability_losses = 0
        self.probability_wins_odds = 0
        self.probability_losses_odds = 0
        self.probability_losses_amount = 0

    def add_log(self, log, p1, p2):
        winner, loser = (p1, p2) if log.winner == log.p1_name else (p2, p1)

        self.games += 1
        if log.winner == log.p1_name:
            self.p1_wins += 1
            self.p1_wins_amount += self.get_odds(log, p1) * self.bet_amount
            self.p2_wins_amount -= self.bet_amount
        if log.winner == log.p2_name:
            self.p2_wins += 1
            self.p2_wins_amount += self.get_odds(log, p2) * self.bet_amount
            self.p1_wins_amount -= self.bet_amount

        if winner.total_games < self.games_threshold or loser.total_games < self.games_threshold:
            return

        winner_odds = self.get_odds(log, winner)
        loser_odds = self.get_odds(log, loser)

        winner_wl = winner.total_wins / winner.total_games if winner.total_games != 0.0 else 0.5
        loser_wl = loser.total_wins / loser.total_games if loser.total_games != 0.0 else 0.5

        winner_wl_probability = winner_wl / (winner_wl + loser_wl) if winner_wl != 0.0 or loser_wl != 0.0 else 0.5
        if self.is_above_threshold(winner_wl_probability):
            self.wl_games += 1
            if winner_wl_probability > 0.5:
                self.wl_wins += 1
                self.wl_wins_odds += winner_odds
                self.wl_wins_amount += winner_odds * self.bet_amount
                self.wl_losses_amount -= self.bet_amount
            if winner_wl_probability < 0.5:
                self.wl_losses += 1
                self.wl_losses_odds += loser_odds
                self.wl_losses_amount += loser_odds * self.bet_amount
                self.wl_wins_amount -= self.bet_amount

        winner_probability = self.get_probability(winner.skill, loser.skill)
        if self.is_above_threshold(winner_probability):
            self.probability_games += 1
            if winner_probability > 0.5:
                self.probability_wins += 1
                self.probability_wins_odds += winner_odds
                self.probability_wins_amount += winner_odds * self.bet_amount
                self.probability_losses_amount -= self.bet_amount
                if self.target_games == 0 and self.probability_wins_amount >= self.target_amount:
                    self.target_games = self.probability_games
            if winner_probability < 0.5:
                self.probability_losses += 1
                self.probability_losses_odds += loser_odds
                self.probability_losses_amount += loser_odds * self.bet_amount
                self.probability_wins_amount -= self.bet_amount
                self.probability_wins_amount_lowest = min(self.probability_wins_amount_lowest, self.probability_wins_amount)

    def get_odds(self, log, player):
        p1_amount = int(log.p1_amount) + self.bet_amount if log.p1_name == player.name else int(log.p1_amount)
        p2_amount = int(log.p2_amount) + self.bet_amount if log.p2_name == player.name else int(log.p2_amount)
        odds = p1_amount / p2_amount
        if log.p1_name == player.name:
            odds = 1 / odds
        return odds

    def get_probability(self, p1_skill, p2_skill):
        delta_mu = p1_skill.mu - p2_skill.mu
        sum_sigma = p1_skill.sigma ** 2 + p2_skill.sigma ** 2
        denom = math.sqrt(2 * (trueskill.BETA * trueskill.BETA) + sum_sigma)
        return trueskill.global_env().cdf(delta_mu / denom)

    def is_above_threshold(self, probability):
        return round(abs(probability - (1 - probability)), 4) > self.probability_threshold
