class Stats:
    def __init__(self, p1_name, p2_name, tier):
        self.p1_name = p1_name
        self.p2_name = p2_name
        self.tier = tier

        self.p1_total_wins = None
        self.p1_total_losses = None
        self.p2_total_wins = None
        self.p2_total_losses = None

        self.p1_level1_wins = None
        self.p1_level1_amount = None
        self.p2_level1_wins = None
        self.p2_level1_amount = None

        self.p1_streak = None
        self.p2_streak = None

    def to_text(self):
        tier = self.tier
        p1_name = self.format(self.p1_name)
        p2_name = self.format(self.p2_name)
        p1_level1_wins = self.format(self.p1_level1_wins)
        p2_level1_wins = self.format(self.p2_level1_wins)
        p1_level1_wl_ratio = self.format(self.get_ratio(self.p1_level1_wins, self.p2_level1_wins))
        p2_level1_wl_ratio = self.format(self.get_ratio(self.p2_level1_wins, self.p1_level1_wins))
        p1_level1_amount = self.format(self.p1_level1_amount)
        p2_level1_amount = self.format(self.p2_level1_amount)
        p1_level1_odds = self.format(self.get_p1_level1_odds())
        p2_level1_odds = self.format(self.get_p2_level1_odds())
        p1_total_wins = self.format(self.p1_total_wins)
        p2_total_wins = self.format(self.p2_total_wins)
        p1_total_losses = self.format(self.p1_total_losses)
        p2_total_losses = self.format(self.p2_total_losses)
        p1_total_wl_ratio = self.format(self.get_ratio(self.p1_total_wins, self.p1_total_losses))
        p2_total_wl_ratio = self.format(self.get_ratio(self.p2_total_wins, self.p2_total_losses))
        p1_streak = self.format(self.p1_streak)
        p2_streak = self.format(self.p2_streak)

        return f"""
            |-----------------------------------------------------------------------------------|
            | {tier} tier          | {p1_name} | {p2_name} |
            |-----------------------------------------------------------------------------------|
            | level1 wins     | {p1_level1_wins} | {p2_level1_wins} | 
            | level1 wl ratio | {p1_level1_wl_ratio} | {p2_level1_wl_ratio} |
            | level1 amount   | {p1_level1_amount} | {p2_level1_amount} |
            | level1 odds     | {p1_level1_odds} | {p2_level1_odds} |
            |-----------------------------------------------------------------------------------|
            | total wins      | {p1_total_wins} | {p2_total_wins} |
            | total losses    | {p1_total_losses} | {p2_total_losses} |
            | total wl ratio  | {p1_total_wl_ratio} | {p2_total_wl_ratio} |
            | streak          | {p1_streak} | {p2_streak} |
            |-----------------------------------------------------------------------------------|
        """

    def get_ratio(self, dividend, divisor):
        if dividend is None and divisor is None:
            return None

        if dividend is None:
            return f'None/{divisor}'

        if divisor is None:
            return f'{dividend}/None'

        return round(dividend / (dividend + divisor / 100))

    def get_p1_level1_odds(self):
        if self.p1_level1_amount is None or self.p2_level1_amount is None:
            return '-'

        if self.p1_level1_amount > self.p2_level1_amount:
            return round(self.p1_level1_amount / self.p2_level1_amount, 2)
        else:
            return 1

    def get_p2_level1_odds(self):
        if self.p1_level1_amount is None or self.p2_level1_amount is None:
            return '-'

        if self.p1_level1_amount > self.p2_level1_amount:
            return 1
        else:
            return round(self.p2_level1_amount / self.p1_level1_amount, 2)

    def format(self, value, width=30):
        if value is None:
            return f"{'-':<{width}}"
        else:
            return f'{value:<{width}}'
