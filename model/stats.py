class Stats:
    def __init__(self, p1, p2, tier, mode, left):
        self.p1 = p1
        self.p2 = p2
        self.tier = tier
        self.mode = mode
        self.left = left

    def to_text(self):
        mode = self.format_mode(self.mode)
        tier = self.format_tier(self.tier)
        left = self.format_left(self.left)
        p1_name = self.format(self.p1.name)
        p2_name = self.format(self.p2.name)
        p1_direct_wins = self.format(self.p1.direct_wins)
        p2_direct_wins = self.format(self.p2.direct_wins)
        p1_direct_wl_ratio = self.format(self.get_ratio(self.p1.direct_wins, self.p2.direct_wins))
        p2_direct_wl_ratio = self.format(self.get_ratio(self.p2.direct_wins, self.p1.direct_wins))
        p1_direct_amount = self.format(self.p1.direct_amount)
        p2_direct_amount = self.format(self.p2.direct_amount)
        p1_direct_odds = self.format(self.get_direct_odds(self.p1, self.p2))
        p2_direct_odds = self.format(self.get_direct_odds(self.p2, self.p1))
        p1_total_wins = self.format(self.p1.total_wins)
        p2_total_wins = self.format(self.p2.total_wins)
        p1_total_losses = self.format(self.p1.total_losses)
        p2_total_losses = self.format(self.p2.total_losses)
        p1_total_wl_ratio = self.format(self.get_ratio(self.p1.total_wins, self.p1.total_losses))
        p2_total_wl_ratio = self.format(self.get_ratio(self.p2.total_wins, self.p2.total_losses))
        p1_streak = self.format(self.get_streak(self.p1.streak))
        p2_streak = self.format(self.get_streak(self.p2.streak))
        p1_confidence = self.format_confidence(self.p1.skill)
        p2_confidence = self.format_confidence(self.p2.skill)
        p1_skill = self.format_skill(self.p1.skill)
        p2_skill = self.format_skill(self.p2.skill)
        p1_probability = self.format_probability(self.p1.probability)
        p2_probability = self.format_probability(self.p2.probability)
        p1_upset = self.format_probability(self.p1.upset)
        p2_upset = self.format_probability(self.p2.upset)
        p1_job = self.format_probability(self.p1.job)
        p2_job = self.format_probability(self.p2.job)

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
            | Streak          | {p1_streak} | {p2_streak} |
            |-----------------------------------------------------------------------------------|
            | Skill           | {p1_skill} | {p2_skill} |
            | Confidence      | {p1_confidence} | {p2_confidence} |
            | Probability     | {p1_probability} | {p2_probability} |
            |-----------------------------------------------------------------------------------|
            | Upset           | {p1_upset} | {p2_upset} |
            | Job             | {p1_job} | {p2_job} |
            |-----------------------------------------------------------------------------------|
        """

    def get_ratio(self, wins, losses):
        if wins is None or losses is None:
            return None
        else:
            return f'{round(wins / (wins + losses) * 100)}%'

    def get_direct_odds(self, p1, p2):
        if p1.direct_amount is None or p2.direct_amount is None:
            return '-'

        if p1.direct_amount > p2.direct_amount:
            return round(p1.direct_amount / p2.direct_amount, 2)
        else:
            return 1

    def get_streak(self, value):
        if value is None:
            return None

        if value > 0:
            return f'+{value}'
        else:
            return value

    def format(self, value, width=30):
        if value is None:
            return f"{'-':<{width}}"
        else:
            return f'{value:<{width}}'

    def format_mode(self, mode):
        return self.format(value=str(mode).title(), width=15)

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

    def format_confidence(self, skill):
        if skill is None:
            return self.format(skill)
        return self.format_float(skill.sigma)

    def format_float(self, value):
        return self.format(value=f'{value:.2f}')

    def format_skill(self, skill):
        if skill is None:
            return self.format(skill)

        min = skill.mu - 2 * skill.sigma
        max = skill.mu + 2 * skill.sigma
        return self.format(value=f'{skill.mu:.2f} ({min:.2f} - {max:.2f})')

    def format_probability(self, probability):
        if probability is None:
            return self.format(probability)
        return self.format(value=f'{probability:.1%}')
