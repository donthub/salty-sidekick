import logging

from model.stats.statsbase import StatsBase


class TotalStats(StatsBase):

    def __init__(self, total):
        self.total = total

    def print(self):
        logging.info(self.to_text())

    def to_text(self):
        bet_amount = self.format_very_small(self.get_amount(self.total.bet_amount))
        lowest_amount = self.format_very_small2(self.get_amount(self.total.probability_wins_amount_lowest))
        target_amount = self.format_very_small(self.get_amount(self.total.target_amount))
        target_games = self.format_very_small2(self.total.target_games)
        total_games = self.format_slightly_small(self.total.games)
        total_p1_wins = self.format_percent_slightly_small(self.get_ratio(self.total.p1_wins, self.total.games))
        total_p1_wins_amount = self.format_very_small(self.get_amount_percent(self.total.p1_wins_amount))
        total_p2_wins = self.format_percent_slightly_small(self.get_ratio(self.total.p2_wins, self.total.games))
        total_p2_wins_amount = self.format_very_small2(self.get_amount_percent(self.total.p2_wins_amount))
        total_wl_games = self.format_slightly_small(self.total.wl_games)
        total_wl_wins = self.format_percent_slightly_small(self.get_ratio(self.total.wl_wins, self.total.wl_games))
        total_wl_wins_amount = self.format_very_small(self.get_amount_percent(self.total.wl_wins_amount))
        total_wl_losses = self.format_percent_slightly_small(self.get_ratio(self.total.wl_losses, self.total.wl_games))
        total_wl_losses_amount = self.format_very_small2(self.get_amount_percent(self.total.wl_losses_amount))
        total_probability_games = self.format_slightly_small(self.total.probability_games)
        total_probability_wins = self.format_percent_slightly_small(
            self.get_ratio(self.total.probability_wins, self.total.probability_games))
        total_probability_wins_amount = self.format_very_small(
            self.get_amount_percent(self.total.probability_wins_amount))
        total_probability_losses = self.format_percent_slightly_small(
            self.get_ratio(self.total.probability_losses, self.total.probability_games))
        total_probability_losses_amount = self.format_very_small2(
            self.get_amount_percent(self.total.probability_losses_amount))

        return f"""
            |---------------------------------------------------------------------------------------|
            | Target stats        | {bet_amount} | {lowest_amount} | {target_amount} | {target_games} | 
            | Total stats         | {total_games} | {total_p1_wins} | {total_p2_wins} | {total_p1_wins_amount} | {total_p2_wins_amount} |
            | Winrate stats       | {total_wl_games} | {total_wl_wins} | {total_wl_losses} | {total_wl_wins_amount} | {total_wl_losses_amount} |
            | Probability stats   | {total_probability_games} | {total_probability_wins} | {total_probability_losses} | {total_probability_wins_amount} | {total_probability_losses_amount} |
            |---------------------------------------------------------------------------------------|"""

    def get_amount(self, amount):
        prefix = '+' if amount > 0 else '-'
        amount_from = str(abs(round(amount)))
        amount_to = ''

        index = 0
        for character in amount_from:
            amount_to += character
            if (len(amount_from) - index - 1) % 3 == 0 and index != len(amount_from) - 1:
                amount_to += ','
            index += 1

        return prefix + amount_to

    def format_slightly_small(self, value):
        return self.format(value=value, width=8)

    def format_percent_slightly_small(self, probability):
        if probability is None:
            return self.format_slightly_small(None)
        return self.format_slightly_small(value=f'{probability:.2%}')

    def get_amount_percent(self, amount):
        prefix = '+' if amount > 0 else '-'
        return prefix + str(abs(round(amount / self.total.bet_amount))) + '%'