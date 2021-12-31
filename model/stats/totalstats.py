import logging

from model.stats.statsbase import StatsBase
from util.util import Util


class TotalStats(StatsBase):

    def __init__(self, total):
        self.total = total

    def print(self):
        logging.info(self.to_text())

    def to_text(self):
        amount = self.format_very_small2(Util.get_amount(self.total.amount))
        amount_direct = self.format_very_small(Util.get_amount(self.total.amount_direct))
        amount_close = self.format_very_small2(Util.get_amount(self.total.amount_close))
        stats_games = self.format_very_small(self.total.stats_games)
        tier_games = self.format_big(self.get_tier_games())
        tier_directs = self.format_big(self.get_tier_directs())
        tier_characters = self.format_big(self.get_tier_characters())
        total_games = self.format_slightly_small(self.total.games)
        total_p1_wins = self.format_percent_slightly_small2(self.get_ratio(self.total.p1_wins, self.total.games))
        total_p1_amount = self.format(self.get_last_amount(self.total.p1_amount, self.total.stats_games))
        total_p2_wins = self.format_percent_slightly_small2(self.get_ratio(self.total.p2_wins, self.total.games))
        total_p2_amount = self.format(self.get_last_amount(self.total.p2_amount, self.total.stats_games))
        total_direct_games = self.format_slightly_small(self.total.direct_games)
        total_direct_wins = self.format_percent_slightly_small2(self.get_ratio(self.total.direct_wins, self.total.direct_games))
        total_direct_amount = self.format(self.get_last_amount(self.total.direct_amount, self.total.stats_games))
        total_wl_games = self.format_slightly_small(self.total.wl_games)
        total_wl_wins = self.format_percent_slightly_small2(self.get_ratio(self.total.wl_wins, self.total.wl_games))
        total_wl_amount = self.format(self.get_last_amount(self.total.wl_amount, self.total.stats_games))
        total_probability_games = self.format_slightly_small(self.total.probability_games)
        total_probability_wins = self.format_percent_slightly_small2(
            self.get_ratio(self.total.probability_wins, self.total.probability_games))
        total_probability_amount = self.format(self.get_last_amount(self.total.probability_amount, self.total.stats_games))
        total_compare_games = self.format_very_small2(self.total.compare_games)
        total_compare_wins = self.format_percent_very_small(self.get_ratio(self.total.compare_wins, self.total.compare_games))
        total_compare_expected_amount = self.format_very_small(self.get_last_amount(self.total.compare_expected_amount, self.total.stats_games))
        total_compare_upset_amount = self.format_very_small2(self.get_last_amount(self.total.compare_upset_amount, self.total.stats_games))
        total_close_games = self.format_very_small2(self.total.close_games)
        total_close_wins = self.format_percent_very_small(self.get_ratio(self.total.close_wins, self.total.close_games))
        total_close_expected_amount = self.format_very_small(self.get_last_amount(self.total.close_expected_amount, self.total.stats_games))
        total_close_upset_amount = self.format_very_small2(self.get_last_amount(self.total.close_upset_amount, self.total.stats_games))
        total_far_games = self.format_very_small2(self.total.far_games)
        total_far_wins = self.format_percent_very_small(self.get_ratio(self.total.far_wins, self.total.far_games))
        total_far_expected_amount = self.format_very_small(self.get_last_amount(self.total.far_expected_amount, self.total.stats_games))
        total_far_upset_amount = self.format_very_small2(self.get_last_amount(self.total.far_upset_amount, self.total.stats_games))

        return f"""
            |---------------------------------------------------------------------------------------|
            | Tier games          | {tier_games} |
            | Tier characters     | {tier_characters} |
            | Tier directs        | {tier_directs} |
            | Target stats        | {amount} | {amount_direct} | {amount_close} | {stats_games} |
            | P1 stats            | {total_games} | {total_p1_wins} | {total_p1_amount} |
            | P2 stats            | {total_games} | {total_p2_wins} | {total_p2_amount} |
            | Direct stats        | {total_direct_games} | {total_direct_wins} | {total_direct_amount} |
            | Winrate stats       | {total_wl_games} | {total_wl_wins} | {total_wl_amount} |
            | Probability stats   | {total_probability_games} | {total_probability_wins} | {total_probability_amount} |
            | Compare stats       | {total_compare_games} | {total_compare_wins} | {total_compare_expected_amount} | {total_compare_upset_amount} |
            | Close stats         | {total_close_games} | {total_close_wins} | {total_close_expected_amount} | {total_close_upset_amount} |
            | Far stats           | {total_far_games} | {total_far_wins} | {total_far_expected_amount} | {total_far_upset_amount} |
            |---------------------------------------------------------------------------------------|"""

    def get_last_amount(self, amounts, last):
        return Util.get_amount(sum(amounts[-last:]))

    def format_big(self, value):
        return self.format(value=value, width=63)

    def format_slightly_small(self, value):
        return self.format(value=value, width=13)

    def format_slightly_small2(self, value):
        return self.format(value=value, width=14)

    def format_percent_slightly_small2(self, probability):
        if probability is None:
            return self.format_slightly_small2(None)
        return self.format_slightly_small2(value=f'{probability:.2%}')

    def format_percent_very_small(self, probability):
        if probability is None:
            return self.format_very_small(None)
        return self.format_very_small(value=f'{probability:.2%}')

    def get_tier_games(self):
        return ' | '.join(list(map(lambda item: self.format(value=f'{item[0]}: {item[1]}', width=10), self.total.tier_games.items())))

    def get_tier_characters(self):
        return ' | '.join(list(map(lambda item: self.format(value=f'{item[0]}: {len(item[1])}', width=10), self.total.tier_characters.items())))

    def get_tier_directs(self):
        return ' | '.join(list(map(lambda item: self.format(value=f'{item[0]}: {item[1]}', width=10), self.total.tier_directs.items())))