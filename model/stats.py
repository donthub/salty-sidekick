class Stats:
    def __init__(self, p1_name, p2_name, tier):
        self.p1_name = p1_name
        self.p2_name = p2_name
        self.tier = tier

        self.p1_total_wins = None
        self.p1_total_losses = None
        self.p2_total_wins = None
        self.p2_total_losses = None

        self.p1_direct_wins = None
        self.p1_direct_amount = None
        self.p2_direct_wins = None
        self.p2_direct_amount = None

        self.p1_streak = None
        self.p2_streak = None

    def to_text(self):
        tier = self.tier
        p1_name = self.format(self.p1_name)
        p2_name = self.format(self.p2_name)
        p1_direct_wins = self.format(self.p1_direct_wins)
        p2_direct_wins = self.format(self.p2_direct_wins)
        p1_direct_wl_ratio = self.format(self.get_ratio(self.p1_direct_wins, self.p2_direct_wins))
        p2_direct_wl_ratio = self.format(self.get_ratio(self.p2_direct_wins, self.p1_direct_wins))
        p1_direct_amount = self.format(self.p1_direct_amount)
        p2_direct_amount = self.format(self.p2_direct_amount)
        p1_direct_odds = self.format(self.get_p1_direct_odds())
        p2_direct_odds = self.format(self.get_p2_direct_odds())
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
            | direct wins     | {p1_direct_wins} | {p2_direct_wins} | 
            | direct wl ratio | {p1_direct_wl_ratio} | {p2_direct_wl_ratio} |
            | direct amount   | {p1_direct_amount} | {p2_direct_amount} |
            | direct odds     | {p1_direct_odds} | {p2_direct_odds} |
            |-----------------------------------------------------------------------------------|
            | total wins      | {p1_total_wins} | {p2_total_wins} |
            | total losses    | {p1_total_losses} | {p2_total_losses} |
            | total wl ratio  | {p1_total_wl_ratio} | {p2_total_wl_ratio} |
            | streak          | {p1_streak} | {p2_streak} |
            |-----------------------------------------------------------------------------------|
        """

    def get_ratio(self, dividend, divisor):
        if dividend is None or divisor is None:
            return None
        else:
            return round(dividend / (dividend + divisor / 100))

    def get_p1_direct_odds(self):
        if self.p1_direct_amount is None or self.p2_direct_amount is None:
            return '-'

        if self.p1_direct_amount > self.p2_direct_amount:
            return round(self.p1_direct_amount / self.p2_direct_amount, 2)
        else:
            return 1

    def get_p2_direct_odds(self):
        if self.p1_direct_amount is None or self.p2_direct_amount is None:
            return '-'

        if self.p1_direct_amount > self.p2_direct_amount:
            return 1
        else:
            return round(self.p2_direct_amount / self.p1_direct_amount, 2)

    def format(self, value, width=30):
        if value is None:
            return f"{'-':<{width}}"
        else:
            return f'{value:<{width}}'
