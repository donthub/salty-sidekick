import json
import logging
import os
import shutil


class Config:

    def __init__(self, path='config.json', sample_path='config_sample.json'):
        self.path = path
        self.sample_path = sample_path

        self.stats_amount = 0
        self.stats_games = 0
        self.close_range = 20
        self.simple_ui = False
        self.auth = None
        self.bet = False
        self.amount = 0
        self.amount_direct = 0
        self.min_balance = 0
        self.loyalties = []
        self.amount_loyalty = 0
        self.bet_p1 = True
        self.bet_p2 = True
        self.init()

    def init(self):
        if not os.path.isfile(self.path):
            if os.path.isfile(self.sample_path):
                shutil.copyfile(self.sample_path, self.path)
            else:
                logging.warning(
                    '"config_sample.json" is missing in root. Please restore it or create "config.json" manually.')
                exit(-1)

        with open(self.path, 'r', encoding='utf-8') as file:
            config = json.load(file)

        self.auth = self.get_auth(config)

        if 'stats_amount' in config:
            self.stats_amount = int(config['stats_amount'])
        if 'stats_games' in config:
            self.stats_games = int(config['stats_games'])
        if 'close_range' in config:
            self.close_range = int(config['close_range'])

        self.bet = 'bet' in config and bool(config['bet'])
        if self.bet:
            if 'simple_ui' in config:
                self.simple_ui = bool(config['simple_ui'])
            if 'amount' in config:
                self.amount = int(config['amount'])
            if 'amount_direct' in config:
                self.amount_direct = int(config['amount_direct'])
            if 'min_balance' in config:
                self.min_balance = int(config['min_balance'])
            if 'loyalties' in config:
                self.loyalties = config['loyalties']
            if 'amount_loyalty' in config:
                self.amount_loyalty = int(config['amount_loyalty'])
            if 'bet_p1' in config:
                self.bet_p1 = bool(config['bet_p1'])
            if 'bet_p2' in config:
                self.bet_p2 = bool(config['bet_p2'])

    def get_auth(self, config):
        username = self.strip(config['username'])
        oauth_token = self.strip(config['oauth_token'])
        if len(username) == 0 or self.is_invalid_token(oauth_token):
            logging.warning(
                '"config.json" in root is not configured properly. Please fill "username" and "oauth_token" values.')
            exit(-1)

        if not oauth_token.startswith('oauth:'):
            oauth_token = f"oauth:{oauth_token}"

        return username, oauth_token

    def strip(self, value):
        if value is None:
            return ''
        else:
            return value.strip()

    def is_invalid_token(self, value):
        oauth_prefix = 'oauth:'
        return len(value) == 0 or value.startswith(oauth_prefix) and len(value) == len(oauth_prefix)
