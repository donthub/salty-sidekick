import logging

from model.stats.statsbase import StatsBase


class TotalStats(StatsBase):

    def __init__(self, total):
        self.total = total

    def print(self):
        logging.info(self.to_text())

    def to_text(self):
        stats_amount = self.format(self.get_amount(self.total.stats_amount))
        stats_games = self.format(self.total.stats_games)
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

        return f"""
            |---------------------------------------------------------------------------------------|
            | Tier games          | {tier_games} |
            | Tier characters     | {tier_characters} |
            | Tier directs        | {tier_directs} |
            | Target stats        | {stats_amount} | {stats_games} |
            | P1 stats            | {total_games} | {total_p1_wins} | {total_p1_amount} |
            | P2 stats            | {total_games} | {total_p2_wins} | {total_p2_amount} |
            | Direct stats        | {total_direct_games} | {total_direct_wins} | {total_direct_amount} |
            | Winrate stats       | {total_wl_games} | {total_wl_wins} | {total_wl_amount} |
            | Probability stats   | {total_probability_games} | {total_probability_wins} | {total_probability_amount} |
            |---------------------------------------------------------------------------------------|"""

    def get_amount(self, amount):
        prefix = self.get_prefix(amount)
        amount_from = str(abs(round(amount)))
        amount_to = ''

        index = 0
        for character in amount_from:
            amount_to += character
            if (len(amount_from) - index - 1) % 3 == 0 and index != len(amount_from) - 1:
                amount_to += ','
            index += 1

        return prefix + amount_to

    def get_prefix(self, amount):
        if amount > 0:
            return '+'
        elif amount < 0:
            return '-'
        else:
            return ''

    def get_last_amount(self, amounts, last):
        return self.get_amount(sum(amounts[-last:]))

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

    def get_tier_games(self):
        return ' | '.join(list(map(lambda item: self.format(value=f'{item[0]}: {item[1]}', width=10), self.total.tier_games.items())))

    def get_tier_characters(self):
        return ' | '.join(list(map(lambda item: self.format(value=f'{item[0]}: {len(item[1])}', width=10), self.total.tier_characters.items())))

    def get_tier_directs(self):
        return ' | '.join(list(map(lambda item: self.format(value=f'{item[0]}: {item[1]}', width=10), self.total.tier_directs.items())))