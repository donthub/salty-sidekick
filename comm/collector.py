import datetime as datetime
import logging

from model.log import Log
from util.mode import Mode


class Collector:

    def __init__(self, database, model, better):
        self.database = database
        self.model = model
        self.better = better
        self.state = None

        self.p1_name = None
        self.p2_name = None
        self.tier = None
        self.mode = None

        self.p1_amount = None
        self.p1_streak = None
        self.p2_amount = None
        self.p2_streak = None

        self.winner = None

    def start_match(self, p1_name, p2_name, tier, mode, left):
        # logging.info(f'--- P1 name: {p1_name}, P2 name: {p2_name}, tier: {tier}')
        if self.state is not None and self.state != 'end':
            # logging.info(f'--- Invalid state: {self.state}. Skipping...')
            return

        self.state = 'start'
        self.p1_name = p1_name
        self.p2_name = p2_name
        self.tier = tier
        self.mode = mode

        player_stats = self.model.get_player_stats(p1_name, p2_name, tier, mode, left)
        player_stats.print()

        self.better.bet(player_stats)

    def lock_match(self, p1_streak, p1_amount, p2_streak, p2_amount):
        # logging.info(
            # f'--- P1 streak: {p1_streak}, P1 amount: {p1_amount}, P2 streak: {p2_streak}, P2 amount: {p2_amount}')
            # f'--- P1 amount: {p1_amount}, P2 amount: {p2_amount}')
        if self.state != 'start':
            # logging.info(f'--- Invalid state: {self.state}. Skipping...')
            return

        self.state = 'lock'
        self.p1_streak = int(p1_streak)
        self.p1_amount = self.trim_amount(p1_amount)
        self.p2_streak = int(p2_streak)
        self.p2_amount = self.trim_amount(p2_amount)

    def trim_amount(self, amount):
        return ''.join(c for c in amount if c in '0123456789')

    def end_match(self, winner):
        logging.info(self.get_winner_text(winner))

        if self.state != 'lock':
            # logging.info(f'--- Invalid state: {self.state}. Skipping...')
            return

        self.state = 'end'
        if winner != self.p1_name and winner != self.p2_name:
            # logging.info(f'--- Invalid result. Resetting...')
            return

        if self.mode == Mode.EXHIBITION:
            return

        self.winner = winner
        self.p1_streak = self.get_player_streak(winner, self.p1_name, self.p1_streak)
        self.p2_streak = self.get_player_streak(winner, self.p2_name, self.p2_streak)

        date_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log = Log(self.p1_name, self.p1_amount, self.p1_streak, self.p2_name, self.p2_amount, self.p2_streak, self.tier,
                  self.winner, self.mode, date_time)
        self.database.add_log(log)
        self.model.add_log(log)

    def get_player_streak(self, winner, player_name, player_streak):
        if winner == player_name:
            if player_streak <= 0:
                return 1
            else:
                return player_streak + 1
        else:
            if player_streak >= 0:
                return -1
            else:
                return player_streak - 1

    def get_winner_text(self, winner):
        probability_text = self.get_probability_text(winner)
        odds_text = self.get_odds_text(winner)
        if probability_text is None and odds_text is None:
            return f'Winner: {winner}'

        text = ''
        if odds_text is None:
            text += probability_text
        elif probability_text is None:
            text += f'{odds_text:.2f}'
        else:
            text += f'{probability_text} | {odds_text:.2f}'
        return f'Winner: {winner} ({text})'

    def get_probability_text(self, winner):
        player_name = self.model.get_probability_player_name(self.p1_name, self.p2_name, self.tier)
        if player_name is None:
            return None
        elif player_name == winner:
            return 'expected'
        else:
            return 'upset'

    def get_odds_text(self, winner):
        if self.p1_name is None or self.p2_name is None:
            return None
        if self.p1_amount is None or self.p2_amount is None:
            return None
        elif self.p1_name == winner:
            return self.get_odds(self.p1_amount, self.p2_amount)
        else:
            return self.get_odds(self.p2_amount, self.p1_amount)

    def get_odds(self, winner_amount, loser_amount):
        winner_amount = int(self.trim_amount(winner_amount))
        loser_amount = int(self.trim_amount(loser_amount))
        return loser_amount / winner_amount
