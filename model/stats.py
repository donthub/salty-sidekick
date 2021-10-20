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
        p1_direct_wl_ratio = self.format_probability(self.get_ratio(self.p1_direct.wins, self.p1_direct.total))
        p2_direct_wl_ratio = self.format_probability(self.get_ratio(self.p2_direct.wins, self.p2_direct.total))
        p1_direct_amount = self.format(self.get_direct_amount(self.p1_direct))
        p2_direct_amount = self.format(self.get_direct_amount(self.p2_direct))
        p1_direct_odds = self.format(self.get_direct_odds(self.p1_direct, self.p2_direct))
        p2_direct_odds = self.format(self.get_direct_odds(self.p2_direct, self.p1_direct))
        p1_total_wins = self.format(self.get_total_wins(self.p1))
        p2_total_wins = self.format(self.get_total_wins(self.p2))
        p1_total_losses = self.format(self.get_total_losses(self.p1))
        p2_total_losses = self.format(self.get_total_losses(self.p2))
        p1_total_wl_ratio = self.format_probability(self.get_ratio(self.p1.total_wins, self.p1.total_games))
        p2_total_wl_ratio = self.format_probability(self.get_ratio(self.p2.total_wins, self.p2.total_games))
        p1_total_wl_probability = self.format_probability(self.get_wl_probability(self.p1, self.p2))
        p2_total_wl_probability = self.format_probability(self.get_wl_probability(self.p2, self.p1))
        p1_streak = self.format(self.get_streak(self.p1))
        p2_streak = self.format(self.get_streak(self.p2))
        p1_skill = self.format(self.get_skill(self.p1.skill))
        p2_skill = self.format(self.get_skill(self.p2.skill))
        p1_confidence = self.format_float(self.get_confidence(self.p1.skill))
        p2_confidence = self.format_float(self.get_confidence(self.p2.skill))
        p1_probability = self.format_probability(self.get_probability(self.p1.skill, self.p2.skill))
        p2_probability = self.format_probability(self.get_probability(self.p2.skill, self.p1.skill))
        p1_upset = self.format_probability(self.get_ratio(self.p1.upset, self.p1.total_games))
        p2_upset = self.format_probability(self.get_ratio(self.p2.upset, self.p2.total_games))
        p1_job = self.format_probability(self.get_ratio(self.p1.job, self.p1.total_games))
        p2_job = self.format_probability(self.get_ratio(self.p2.job, self.p2.total_games))
        total_games = self.format_small(self.total.games)
        total_p1_wins = self.format_probability_small(self.get_ratio(self.total.p1_wins, self.total.games))
        total_p2_wins = self.format_probability_small(self.get_ratio(self.total.p2_wins, self.total.games))
        total_wl_games = self.format_very_small(self.total.wl_games)
        total_wl_wins_games = self.format_very_small(self.total.wl_wins)
        total_wl_wins = self.format_probability_very_small(self.get_ratio(self.total.wl_wins, self.total.wl_games))
        total_wl_wins_odds = self.format_very_small(self.get_odds(self.total.wl_wins_odds, self.total.wl_wins))
        total_wl_wins_amount = self.format_small(self.get_amount(self.total.wl_wins_amount))
        total_wl_losses = self.format_probability_very_small(self.get_ratio(self.total.wl_losses, self.total.wl_games))
        total_wl_losses_games = self.format_very_small(self.total.wl_losses)
        total_wl_losses_odds = self.format_very_small(self.get_odds(self.total.wl_losses_odds, self.total.wl_losses))
        total_wl_losses_amount = self.format_small(self.get_amount(self.total.wl_losses_amount))
        total_probability_games = self.format_very_small(self.total.probability_games)
        total_probability_wins = self.format_probability_very_small(self.get_ratio(self.total.probability_wins, self.total.probability_games))
        total_probability_wins_games = self.format_very_small(self.total.probability_wins)
        total_probability_wins_odds = self.format_very_small(self.get_odds(self.total.probability_wins_odds, self.total.probability_wins))
        total_probability_wins_amount = self.format_small(self.get_amount(self.total.probability_wins_amount))
        total_probability_losses = self.format_probability_very_small(self.get_ratio(self.total.probability_losses, self.total.probability_games))
        total_probability_losses_games = self.format_very_small(self.total.probability_losses)
        total_probability_losses_odds = self.format_very_small(self.get_odds(self.total.probability_losses_odds, self.total.probability_losses))
        total_probability_losses_amount = self.format_small(self.get_amount(self.total.probability_losses_amount))

        return f"""
            |-----------------------------------------------------------------------------------|
            | {mode} | {tier} | {left} |
            |-----------------------------------------------------------------------------------|
            | Name            | {p1_name} | {p2_name} |
            |-----------------------------------------------------------------------------------|
            | Direct wins     | {p1_direct_wins} | {p2_direct_wins} | 
            | Direct wl ratio | {p1_direct_wl_ratio} | {p2_direct_wl_ratio} |
            | Direct amount   | {p1_direct_amount} | {p2_direct_amount} |
            | Direct odds     | {p1_direct_odds} | {p2_direct_odds} |
            |-----------------------------------------------------------------------------------|
            | Total wins      | {p1_total_wins} | {p2_total_wins} |
            | Total losses    | {p1_total_losses} | {p2_total_losses} |
            | Total wl ratio  | {p1_total_wl_ratio} | {p2_total_wl_ratio} |
            | Wl probability  | {p1_total_wl_probability} | {p2_total_wl_probability} |
            | Streak          | {p1_streak} | {p2_streak} |
            |-----------------------------------------------------------------------------------|
            | Skill           | {p1_skill} | {p2_skill} |
            | Confidence      | {p1_confidence} | {p2_confidence} |
            | Probability     | {p1_probability} | {p2_probability} |
            |-----------------------------------------------------------------------------------|
            | Upset           | {p1_upset} | {p2_upset} |
            | Job             | {p1_job} | {p2_job} |
            |-----------------------------------------------------------------------------------|
            | Total           | {total_games} | {total_p1_wins} | {total_p2_wins} |
            | Winrate wins    | {total_wl_games} | {total_wl_wins_games} | {total_wl_wins} | {total_wl_wins_odds} | {total_wl_wins_amount} |
            | Winrate losses  | {total_wl_games} | {total_wl_losses_games} | {total_wl_losses} | {total_wl_losses_odds} | {total_wl_losses_amount} |
            | Prob. wins      | {total_probability_games} | {total_probability_wins_games} | {total_probability_wins} | {total_probability_wins_odds} | {total_probability_wins_amount} |
            | Prob. losses    | {total_probability_games} | {total_probability_losses_games} | {total_probability_losses} | {total_probability_losses_odds} | {total_probability_losses_amount} |
            |-----------------------------------------------------------------------------------|
        """

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
        return self.format(value=str(mode).title(), width=15)

    def format_small(self, value):
        return self.format(value=value, width=19)

    def format_very_small(self, value):
        return self.format(value=value, width=8)

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

    def format_probability(self, probability):
        if probability is None:
            return self.format(None)
        return self.format(value=f'{probability:.2%}')

    def format_probability_small(self, probability):
        if probability is None:
            return self.format_small(None)
        return self.format_small(value=f'{probability:.2%}')

    def format_probability_very_small(self, probability):
        if probability is None:
            return self.format_very_small(None)
        return self.format_very_small(value=f'{probability:.2%}')

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