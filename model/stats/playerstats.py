import logging

from model.stats.statsbase import StatsBase
from util.util import Util


class PlayerStats(StatsBase):

    def __init__(self, p1, p2, tier, p1_tiers=None, p2_tiers=None, mode=None, left=None):
        self.p1 = p1
        self.p2 = p2
        self.tier = tier
        self.mode = mode
        self.left = left
        self.p1_tiers = p1_tiers
        self.p2_tiers = p2_tiers
        self.p1_direct = self.p1.get_direct(p2.name)
        self.p2_direct = self.p2.get_direct(p1.name)

    def print(self):
        logging.info(self.to_text())

    def to_text(self):
        mode = self.format_mode(self.mode)
        tier = self.format_tier(self.tier)
        left = self.format_left(self.left)
        p1_name = self.format(self.p1.name)
        p2_name = self.format(self.p2.name)
        p1_tiers = self.format(self.get_tiers(self.p1_tiers))
        p2_tiers = self.format(self.get_tiers(self.p2_tiers))
        p1_date_time = self.format(self.p1.date_time)
        p2_date_time = self.format(self.p2.date_time)
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
        bet_p1_name = self.format(self.format_bet_player_name(self.p1, self.get_bet_player_name()))
        bet_p2_name = self.format(self.format_bet_player_name(self.p2, self.get_bet_player_name()))
        bet_p1_probability = self.format_percent_very_small(self.get_bet_probability_player(self.p1))
        bet_p1_matches = self.format_very_small2(self.get_bet_matches(self.p1))
        bet_p2_probability = self.format_percent_very_small(self.get_bet_probability_player(self.p2))
        bet_p2_matches = self.format_very_small2(self.get_bet_matches(self.p2))

        text = f"""
            |---------------------------------------------------------------------------------------|
            | {mode} | {tier} | {left} |
            |---------------------------------------------------------------------------------------|
            | Name                | {p1_name} | {p2_name} |"""

        if self.p1.total_games > 0 or self.p2.total_games > 0:
            text += f"""
            |---------------------------------------------------------------------------------------|
            | Last seen           | {p1_date_time} | {p2_date_time} |
            | Other tiers         | {p1_tiers} | {p2_tiers} |
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

        if self.p1.total_games > 0 or self.p2.total_games > 0:
            column = 'Bet  !!! DIRECT !!!' if self.p1_direct.total > 0 or self.p2_direct.total > 0 else 'Bet character      '
            text += f"""
            |---------------------------------------------------------------------------------------|
            | {column} | {bet_p1_name} | {bet_p2_name} |
            | Bet chance          | {bet_p1_probability} | {bet_p1_matches} | {bet_p2_probability} | {bet_p2_matches} |"""

        text += f"""
            |---------------------------------------------------------------------------------------|"""

        return text

    def get_tiers(self, tiers):
        tiers_text = ', '.join(list(filter(lambda tier: tier != self.tier, tiers)))
        return tiers_text if len(tiers_text) > 0 else None

    def get_direct_wins(self, direct):
        return direct.wins if direct.total > 0 else None

    def get_direct_amount(self, direct):
        return direct.amount if direct.total > 0 else None

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
        return Util.get_probability(p1_skill, p2_skill)

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

    def format_mode(self, mode):
        return self.format(value=str(mode).title(), width=19)

    def format_small(self, value):
        return self.format(value=value, width=19)

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

    def get_odds(self, odds, games):
        if games == 0:
            return None
        return round(odds / games, 2)

    def format_bet_player_name(self, player, player_name):
        if player_name == player.name:
            return player_name
        return None

    def get_bet_player_name(self):
        p1_direct_wins = self.get_direct_wins(self.p1_direct)
        p2_direct_wins = self.get_direct_wins(self.p2_direct)
        if p1_direct_wins is None and p2_direct_wins is None:
            p1_probability = self.get_bet_probability_player(self.p1)
            p2_probability = self.get_bet_probability_player(self.p2)
            if p1_probability is not None and p1_probability > 0.5:
                return self.p1.name
            if p2_probability is not None and p2_probability > 0.5:
                return self.p2.name
        elif p2_direct_wins is None or p1_direct_wins > p2_direct_wins:
            return self.p1.name
        elif p1_direct_wins is None or p2_direct_wins > p1_direct_wins:
            return self.p2.name
        return None

    def get_bet_probability_player(self, player):
        probability = self.get_direct_wl_probability_player(player)
        if probability == 0.5:
            probability = self.get_probability_player(player)
        if probability == 0.5:
            probability = self.get_wl_probability_player(player)
        return probability

    def get_direct_wl_probability_player(self, player):
        if self.p1_direct.total == 0 and self.p2_direct.total == 0:
            return 0.5
        if player.name == self.p1.name:
            return self.get_direct_wl_probability(self.p1_direct, self.p2_direct)
        else:
            return self.get_direct_wl_probability(self.p2_direct, self.p1_direct)

    def get_probability_player(self, player):
        if player.name == self.p1.name:
            return self.get_probability(self.p1.skill, self.p2.skill)
        else:
            return self.get_probability(self.p2.skill, self.p1.skill)

    def get_wl_probability_player(self, player):
        if player.name == self.p1.name:
            return self.get_wl_probability(self.p1, self.p2)
        else:
            return self.get_wl_probability(self.p2, self.p1)

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
