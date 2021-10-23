class StatsBase:

    def get_ratio(self, num, total):
        if num is None or total is None or total == 0:
            return None
        else:
            return num / total

    def format(self, value, width=30):
        if value is None:
            return f"{'-':<{width}}"
        else:
            return f'{value:<{width}}'

    def format_very_small(self, value):
        return self.format(value=value, width=14)

    def format_very_small2(self, value):
        return self.format(value=value, width=13)