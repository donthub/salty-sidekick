import logging
import os.path
import random
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, \
    ElementNotInteractableException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from util.mode import Mode
from util.util import Util


class Better:

    def __init__(self, config):
        self.is_active = config.bet
        self.simple_ui = config.simple_ui
        self.amount = config.amount
        self.amount_direct = config.amount_direct
        self.amount_close = config.amount_close
        self.min_balance = config.min_balance
        self.close_range = config.close_range

        self.driver = None
        self.init()

    def init(self):
        if not self.is_active:
            return
        self.init_driver()
        self.log_in()
        if self.simple_ui:
            self.remove_unused()

    def init_driver(self):
        if os.path.exists('chromedriver.exe'):
            self.driver = webdriver.Chrome(executable_path='chromedriver.exe')
        else:
            self.driver = webdriver.Chrome()

    def log_in(self):
        self.driver.get('https://www.saltybet.com/authenticate?signin=1')
        wait = WebDriverWait(self.driver, 300)
        wait.until(expected_conditions.url_to_be('https://www.saltybet.com/'))
        wait.until(self.is_loaded)

    def remove_unused(self):
        self.driver.execute_script('document.getElementById("video-embed").remove()')
        self.driver.execute_script('document.getElementById("chat-frame-stream").remove()')
        self.driver.execute_script('document.getElementById("sbettorswrapper").remove()')

    def is_loaded(self, driver):
        return driver.execute_script('return document.readyState') == 'complete'

    def bet(self, player_stats):
        try:
            self.try_bet(player_stats)
        except (NoSuchElementException, StaleElementReferenceException, ElementNotInteractableException):
            logging.warning('Error occurred while trying to bet!')

    def try_bet(self, player_stats):
        if not self.is_active or player_stats.mode == Mode.EXHIBITION:
            return

        amount = self.get_normal_amount(player_stats)
        if amount <= 0:
            return

        time.sleep(random.randint(5, 8))

        self.bet_amount(amount)

        if self.is_probability_range(player_stats, player_stats.p1):
            self.bet_player_p1(player_stats, amount)
        elif self.is_probability_range(player_stats, player_stats.p2):
            self.bet_player_p2(player_stats, amount)

    def is_probability_range(self, player_stats, player):
        wl_probability = player_stats.get_bet_wl_probability_player(player)
        skill_probability = player_stats.get_bet_probability_player(player)
        if wl_probability is None or skill_probability is None:
            return False
        if skill_probability > 0.5 > wl_probability:
            return True
        if skill_probability < 0.5 < wl_probability:
            return False
        if wl_probability == 0.5:
            return skill_probability > 0.5
        diff = self.close_range / 200
        return wl_probability > 0.5 + diff or 0.5 > wl_probability >= 0.5 - diff

    def bet_player_p1(self, player_stats, amount):
        self.bet_player('player1', player_stats, amount)

    def bet_player_p2(self, player_stats, amount):
        self.bet_player('player2', player_stats, amount)

    def bet_player(self, player_id, player_stats, amount):
        player = player_stats.p1 if player_id == 'player1' else player_stats.p2
        player_input = self.driver.find_element(value=player_id)
        player_input.click()
        logging.info(f'Betting: {player.name} ({Util.get_amount(amount)})')

    def bet_amount(self, amount):
        wager_input = self.driver.find_element(value='wager')
        wager_input.send_keys(str(amount))

    def get_normal_amount(self, player_stats):
        if player_stats.is_direct_explicitly():
            return self.get_amount(player_stats, self.amount_direct)

        wl_probability = player_stats.get_bet_wl_probability_player(player_stats.p1)
        if wl_probability is None:
            return 0

        diff = self.close_range / 200
        if 0.5 - diff < wl_probability < 0.5 + diff:
            return self.get_amount(player_stats, self.amount_close)
        else:
            return self.get_amount(player_stats, self.amount)

    def get_amount(self, player_stats, amount):
        mode = player_stats.mode
        if mode == Mode.MATCHMAKING or mode == Mode.TOURNAMENT:
            balance = self.get_balance()
            if mode == Mode.MATCHMAKING:
                return min(balance, amount)
            if mode == Mode.TOURNAMENT:
                return balance
        return 0

    def get_balance(self):
        balance_text = self.driver.find_element(value='balance').text
        balance_text = balance_text.replace(',', '')
        return int(balance_text) if balance_text else 0
