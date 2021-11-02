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


class Better:
    class BetException(Exception):
        pass

    def __init__(self, config):
        self.is_active = config.bet
        self.simple_ui = config.simple_ui
        self.amount = config.amount
        self.amount_direct = config.amount_direct
        self.min_balance = config.min_balance

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
        if not self.is_active:
            return

        if player_stats.mode == Mode.EXHIBITION:
            return

        p1_probability = player_stats.get_bet_probability_player(player_stats.p1)
        if p1_probability is None or p1_probability == 0.5:
            return

        balance = self.get_balance()
        amount = self.get_amount(player_stats, balance)

        if amount <= 0:
            return

        time.sleep(random.randint(5, 10))

        self.bet_amount(amount)
        if p1_probability > 0.5:
            self.bet_p1()
        else:
            self.bet_p2()

    def bet_p1(self):
        self.bet_player('player1')

    def bet_p2(self):
        self.bet_player('player2')

    def bet_player(self, player_id):
        player_input = self.driver.find_element(value=player_id)
        player_input.click()

    def bet_amount(self, amount):
        wager_input = self.driver.find_element(value='wager')
        wager_input.send_keys(str(amount))

    def get_amount(self, player_stats, balance):
        if player_stats.mode == Mode.MATCHMAKING:
            amount = self.amount if not player_stats.is_direct_explicitly() else self.amount_direct
            return min(balance - self.min_balance, amount)
        elif player_stats.mode == Mode.TOURNAMENT:
            return balance
        else:
            return 0

    def get_balance(self):
        balance_text = self.driver.find_element(value='balance').text
        balance_text = balance_text.replace(',', '')
        return int(balance_text) if balance_text else 0
