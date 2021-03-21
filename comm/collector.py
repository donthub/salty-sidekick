class Collector:

    def __init__(self, model):
        self.model = model
        self.state = None
        self.p1_name = None
        self.p1_amount = None
        self.p1_streak = None
        self.p2_name = None
        self.p2_amount = None
        self.p2_streak = None
        self.tier = None
        self.winner = None

    def start_match(self, p1_name, p2_name, tier):
        # print(f'--- P1 name: {p1_name}, P2 name: {p2_name}, tier: {tier}')
        if self.state is not None and self.state != 'end':
            # print(f'--- Invalid state: {self.state}. Skipping...')
            return

        self.state = 'start'
        self.p1_name = p1_name
        self.p2_name = p2_name
        self.tier = tier

        stats = self.model.get_stats(p1_name, p2_name, tier)
        print(stats.to_text())

    def lock_match(self, p1_streak, p1_amount, p2_streak, p2_amount):
        # print(f'--- P1 streak: {p1_streak}, P1 amount: {p1_amount}, P2 streak: {p2_streak}, P2 amount: {p2_amount}')
        if self.state != 'start':
            # print(f'--- Invalid state: {self.state}. Skipping...')
            return

        self.state = 'lock'
        self.p1_streak = int(p1_streak)
        self.p1_amount = self.trim_amount(p1_amount)
        self.p2_streak = int(p2_streak)
        self.p2_amount = self.trim_amount(p2_amount)

    def trim_amount(self, amount):
        return ''.join(c for c in amount if c in '0123456789')

    def end_match(self, winner):
        # print(f'--- Winner: {winner}')
        if self.state != 'lock':
            # print(f'--- Invalid state: {self.state}. Skipping...')
            return

        self.state = 'end'
        if winner != self.p1_name and winner != self.p2_name:
            # print(f'--- Invalid result. Resetting...')
            return

        self.winner = winner
        self.update_streak()
        self.model.add_log(self.p1_name, self.p1_amount, self.p1_streak, self.p2_name, self.p2_amount, self.p2_streak,
                           self.tier, self.winner)

    def update_streak(self):
        if self.winner == self.p1_name:
            if self.p1_streak <= 0:
                self.p1_streak = 1
            else:
                self.p1_streak += 1

            if self.p2_streak >= 0:
                self.p2_streak = -1
            else:
                self.p2_streak -= 1
        else:
            if self.p1_streak >= 0:
                self.p1_streak = -1
            else:
                self.p1_streak -= 1

            if self.p2_streak <= 0:
                self.p2_streak = 1
            else:
                self.p2_streak += 1
