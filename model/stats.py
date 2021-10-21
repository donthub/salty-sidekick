import math

import trueskill


class Stats:

    def __init__(self, p1, p2, total, tier, mode, left):
        self.p1 = p1
        self.p2 = p2
        self.total = total
        self.tier = tier
        self.mode = mode
        self.left = left
        self.p1_direct = self.p1.get_direct(p2.name)
        self.p2_direct = self.p2.get_direct(p1.name)

    def to_text(self):
        mode = self.format_mode(self.mode)
        tier = self.format_tier(self.tier)
        left = self.format_left(self.left)
        p1_name = self.format(self.p1.name)
        p2_name = self.format(self.p2.name)
        p1_direct_wins = self.format(self.get_direct_wins(self.p1_direct))
        p2_direct_wins = self.format(self.get_direct_wins(self.p2_direct))
        p1_direct_wl_ratio = self.format_percent(self.get_ratio(self.p1_direct.wins, self.p1_direct.total))
        p2_direct_wl_ratio = self.format_percent(self.get_ratio(self.p2_direct.wins, self.p2_direct.total))
        p1_direct_wl_probability = self.format_percent(self.get_direct_wl_probability(self.p1_direct, self.p2_direct))
        p2_direct_wl_probability = self.format_percent(self.get_direct_wl_probability(self.p2_direct, self.p1_direct))
        p1_direct_amount = self.format(self.get_direct_amount(self.p1_direct))
        p2_direct_amount = self.format(self.get_direct_amount(self.p2_direct))
        p1_direct_odds = self.format(self.get_direct_odds(self.p1_direct, self.p2_direct))
        p2_direct_odds = self.format(self.get_direct_odds(self.p2_direct, self.p1_direct))
        p1_total_wins = self.format(self.get_total_wins(self.p1))
        p2_total_wins = self.format(self.get_total_wins(self.p2))
        p1_total_losses = self.format(self.get_total_losses(self.p1))
        p2_total_losses = self.format(self.get_total_losses(self.p2))
        p1_total_wl_ratio = self.format_percent(self.get_ratio(self.p1.total_wins, self.p1.total_games))
        p2_total_wl_ratio = self.format_percent(self.get_ratio(self.p2.total_wins, self.p2.total_games))
        p1_total_wl_probability = self.format_percent(self.get_wl_probability(self.p1, self.p2))
        p2_total_wl_probability = self.format_percent(self.get_wl_probability(self.p2, self.p1))
        p1_streak = self.format(self.get_streak(self.p1))
        p2_streak = self.format(self.get_streak(self.p2))
        p1_skill = self.format(self.get_skill(self.p1.skill))
        p2_skill = self.format(self.get_skill(self.p2.skill))
        p1_confidence = self.format_float(self.get_confidence(self.p1.skill))
        p2_confidence = self.format_float(self.get_confidence(self.p2.skill))
        p1_probability = self.format_percent(self.get_probability(self.p1.skill, self.p2.skill))
        p2_probability = self.format_percent(self.get_probability(self.p2.skill, self.p1.skill))
        p1_upset = self.format_percent(self.get_ratio(self.p1.upset, self.p1.total_games))
        p2_upset = self.format_percent(self.get_ratio(self.p2.upset, self.p2.total_games))
        p1_job = self.format_percent(self.get_ratio(self.p1.job, self.p1.total_games))
        p2_job = self.format_percent(self.get_ratio(self.p2.job, self.p2.total_games))
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
        total_probability_wins = self.format_percent_slightly_small(self.get_ratio(self.total.probability_wins, self.total.probability_games))
        total_probability_wins_amount = self.format_very_small(self.get_amount_percent(self.total.probability_wins_amount))
        total_probability_losses = self.format_percent_slightly_small(self.get_ratio(self.total.probability_losses, self.total.probability_games))
        total_probability_losses_amount = self.format_very_small2(self.get_amount_percent(self.total.probability_losses_amount))
        bet_p1_name = self.format(self.get_bet_player_name(self.p1))
        bet_p2_name = self.format(self.get_bet_player_name(self.p2))
        bet_p1_probability = self.format_percent_very_small(self.get_bet_probability_player(self.p1))
        bet_p1_matches = self.format_very_small2(self.get_bet_matches(self.p1))
        bet_p2_probability = self.format_percent_very_small(self.get_bet_probability_player(self.p2))
        bet_p2_matches = self.format_very_small2(self.get_bet_matches(self.p2))

        text = ''

        if self.mode is not None or self.tier is not None or self.left is not None:
            text += f"""
            |---------------------------------------------------------------------------------------|
            | {mode} | {tier} | {left} |"""

        if self.p1.name is not None or self.p2.name is not None:
            text += f"""
            |---------------------------------------------------------------------------------------|
            | Name                | {p1_name} | {p2_name} |"""

        if self.p1.total_games > 0 or self.p2.total_games > 0:
            text += f"""
            |---------------------------------------------------------------------------------------|
            | Direct wins         | {p1_direct_wins} | {p2_direct_wins} | 
            | Direct winrate      | {p1_direct_wl_ratio} | {p2_direct_wl_ratio} |
            | Direct probability  | {p1_direct_wl_probability} | {p2_direct_wl_probability} |
            | Direct amount       | {p1_direct_amount} | {p2_direct_amount} |
            | Direct odds         | {p1_direct_odds} | {p2_direct_odds} |
            |---------------------------------------------------------------------------------------|
            | Total wins          | {p1_total_wins} | {p2_total_wins} |
            | Total losses        | {p1_total_losses} | {p2_total_losses} |
            | Total winrate       | {p1_total_wl_ratio} | {p2_total_wl_ratio} |
            | Winrate probability | {p1_total_wl_probability} | {p2_total_wl_probability} |
            | Streak              | {p1_streak} | {p2_streak} |
            |---------------------------------------------------------------------------------------|
            | Skill               | {p1_skill} | {p2_skill} |
            | Skill confidence    | {p1_confidence} | {p2_confidence} |
            | Skill probability   | {p1_probability} | {p2_probability} |
            |---------------------------------------------------------------------------------------|
            | Upset               | {p1_upset} | {p2_upset} |
            | Job                 | {p1_job} | {p2_job} |"""

        text += f"""
            |---------------------------------------------------------------------------------------| 
            | Total stats         | {total_games} | {total_p1_wins} | {total_p2_wins} | {total_p1_wins_amount} | {total_p2_wins_amount} |
            | Winrate stats       | {total_wl_games} | {total_wl_wins} | {total_wl_losses} | {total_wl_wins_amount} | {total_wl_losses_amount} |
            | Probability stats   | {total_probability_games} | {total_probability_wins} | {total_probability_losses} | {total_probability_wins_amount} | {total_probability_losses_amount} |"""

        if self.p1.total_games > 0 or self.p2.total_games > 0:
            column = 'Bet  !!! DIRECT !!!' if self.p1_direct.total > 0 or self.p2_direct.total > 0 else 'Bet character      '
            text += f"""
            |---------------------------------------------------------------------------------------|
            | {column} | {bet_p1_name} | {bet_p2_name} |
            | Bet chance          | {bet_p1_probability} | {bet_p1_matches} | {bet_p2_probability} | {bet_p2_matches} |"""


        text += f"""
            |---------------------------------------------------------------------------------------|
        """

        return text

    def get_direct_wins(self, direct):
        return direct.wins if direct.total > 0 else None

    def get_direct_amount(self, direct):
        return direct.amount if direct.total > 0 else None

    def get_ratio(self, num, total):
        if num is None or total is None or total == 0:
            return None
        else:
            return num / total

    def get_direct_odds(self, p1_direct, p2_direct):
        if p1_direct.total == 0 or p2_direct.total == 0 :
            return None

        if p1_direct.amount > p2_direct.amount:
            return round(p1_direct.amount / p2_direct.amount, 2)
        else:
            return 1

    def get_total_wins(self, player):
        return player.total_wins if player.total_games > 0 else None

    def get_total_losses(self, player):
        return player.total_losses if player.total_games > 0 else None

    def get_streak(self, player):
        if player.total_games == 0:
            return None

        if player.streak > 0:
            return f'+{player.streak}'
        else:
            return player.streak

    def get_probability(self, p1_skill, p2_skill):
        if self.p1.total_games == 0 and self.p2.total_games == 0:
            return None

        delta_mu = p1_skill.mu - p2_skill.mu
        sum_sigma = p1_skill.sigma ** 2 + p2_skill.sigma ** 2
        denom = math.sqrt(2 * (trueskill.BETA * trueskill.BETA) + sum_sigma)
        return trueskill.global_env().cdf(delta_mu / denom)

    def get_direct_wl_probability(self, p1_direct, p2_direct):
        if p1_direct.total == 0 and p2_direct.total == 0:
            return None

        p1_wl = p1_direct.wins / p1_direct.total if p1_direct.total != 0 else 0.5
        p2_wl = p2_direct.wins / p2_direct.total if p2_direct.total != 0 else 0.5
        return p1_wl / (p1_wl + p2_wl) if p1_wl != 0.0 or p2_wl != 0.0 else 0.5

    def get_wl_probability(self, p1, p2):
        if p1.total_games == 0 and p2.total_games == 0:
            return None

        p1_wl = p1.total_wins / p1.total_games if p1.total_games != 0 else 0.5
        p2_wl = p2.total_wins / p2.total_games if p2.total_games != 0 else 0.5
        return p1_wl / (p1_wl + p2_wl) if p1_wl != 0.0 or p2_wl != 0.0 else 0.5

    def format(self, value, width=30):
        if value is None:
            return f"{'-':<{width}}"
        else:
            return f'{value:<{width}}'

    def format_mode(self, mode):
        return self.format(value=str(mode).title(), width=19)

    def format_small(self, value):
        return self.format(value=value, width=19)

    def format_slightly_small(self, value):
        return self.format(value=value, width=8)

    def format_very_small(self, value):
        return self.format(value=value, width=14)

    def format_very_small2(self, value):
        return self.format(value=value, width=13)

    def format_tier(self, tier):
        if tier is None:
            tier = '?'
        return self.format(value=f'{tier} tier')

    def format_left(self, left):
        if left is None:
            left = '?'
            match_str = 'matches'
        elif left == 1:
            match_str = 'match'
        else:
            match_str = 'matches'
        return self.format(value=f'{left} {match_str} left')

    def get_confidence(self, skill):
        if self.p1.total_games == 0 and self.p2.total_games == 0:
            return None

        if skill is None:
            return None

        return skill.sigma

    def format_float(self, value):
        if value is None:
            return self.format(None)
        return self.format(value=f'{value:.4f}')

    def get_skill(self, skill):
        if self.p1.total_games == 0 and self.p2.total_games == 0:
            return None

        if skill is None:
            return None

        min = skill.mu - 2 * skill.sigma
        max = skill.mu + 2 * skill.sigma
        return f'{skill.mu:.2f} ({min:.2f} - {max:.2f})'

    def format_percent(self, percent):
        if percent is None:
            return self.format(None)
        return self.format(value=f'{percent:.2%}')

    def format_percent_very_small(self, probability):
        if probability is None:
            return self.format_very_small(None)
        return self.format_very_small(value=f'{probability:.2%}')

    def format_percent_slightly_small(self, probability):
        if probability is None:
            return self.format_slightly_small(None)
        return self.format_slightly_small(value=f'{probability:.2%}')

    def get_odds(self, odds, games):
        if games == 0:
            return None
        return round(odds / games, 2)

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

    def get_amount_percent(self, amount):
        prefix = '+' if amount > 0 else '-'
        return prefix + str(abs(round(amount / self.total.bet_amount))) + '%'

    def get_bet_direct(self):
        p1_direct_wins = self.get_direct_wins(self.p1_direct)
        p2_direct_wins = self.get_direct_wins(self.p2_direct)
        if p1_direct_wins is None and p2_direct_wins is None:
            return None
        if p2_direct_wins is None or p1_direct_wins > p2_direct_wins:
            return 'RED'
        if p1_direct_wins is None or p2_direct_wins > p1_direct_wins:
            return 'BLUE'
        return None

    def get_bet_player_name(self, player):
        p1_probability = self.get_bet_probability_player(self.p1)
        p2_probability = self.get_bet_probability_player(self.p2)
        if p1_probability is not None and p1_probability > 0.5 and player == self.p1:
            return self.p1.name
        if p2_probability is not None and p2_probability > 0.5 and player == self.p2:
            return self.p2.name
        return None

    def get_bet_probability_player(self, player):
        if self.p1_direct.total > 0 or self.p2_direct.total > 0:
            if player.name == self.p1.name:
                return self.get_direct_wl_probability(self.p1_direct, self.p2_direct)
            else:
                return self.get_direct_wl_probability(self.p2_direct, self.p1_direct)
        else:
            if player.name == self.p1.name:
                return self.get_probability(self.p1.skill, self.p2.skill)
            else:
                return self.get_probability(self.p2.skill, self.p1.skill)

    def get_bet_winrate(self):
        winrate_probability = self.get_wl_probability(self.p1, self.p2)
        if winrate_probability is None or winrate_probability == 0.5:
            return None
        return 'RED' if winrate_probability > 0.5 else 'BLUE'

    def get_bet_matches(self, player):
        if self.p1_direct.total > 0 or self.p2_direct.total > 0:
            direct = self.p1_direct if player.name == self.p1.name else self.p2_direct
            return f'{direct.wins} - {direct.losses} ({direct.total})'
        else:
            return f'{player.total_wins} - {player.total_losses} ({player.total_games})'