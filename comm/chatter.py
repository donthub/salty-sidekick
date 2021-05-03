import logging
import re
import time
from datetime import datetime, timedelta

import irc.bot


class Chatter(irc.bot.SingleServerIRCBot):
    class MessageFound(Exception):
        pass

    def __init__(self, config, collector, channel='saltybet'):
        self.collector = collector
        self.channel = '#' + channel
        self.last_message_date = datetime.now()

        server = 'irc.chat.twitch.tv'
        port = 6667
        logging.info(f'Connecting to {server} on port {port}...')

        auth = config.get_auth()
        username = auth[0]
        oauth_token = auth[1]
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, oauth_token)], username, username)

    def run_infinitely(self):
        self.start()

        while True:
            if datetime.now() - self.last_message_date > timedelta(minutes=10):
                logging.info('Chat has timed out. Restarting...')
                self.disconnect()
                self.start()
                logging.info('Restarted...')
            time.sleep(60)

    def on_welcome(self, connection, event):
        logging.info(f'Joining {self.channel}...')

        connection.join(self.channel)
        logging.info('Joined.')

    def on_pubmsg(self, connection, event):
        self.last_message_date = datetime.now()
        if event.source.nick != 'waifu4u':
            return

        message = event.arguments[0]
        logging.debug(f'{event.source.nick}: {message}')

        try:
            self.parse(message)
        except self.MessageFound:
            return

    def parse(self, message):
        self.parse_start(message)
        self.parse_locked(message)
        self.parse_payout(message)

    def parse_start(self, message):
        self.parse_start_matchmaking(message)
        self.parse_start_tournament(message)
        self.parse_start_exhibition(message)

    def parse_start_matchmaking(self, message):
        pattern = r'^Bets are OPEN for (.+) vs (.+)! \((.) Tier\) {2}\(matchmaking\) www\.saltybet\.com$'
        match = re.compile(pattern).match(message)
        if match:
            logging.info('--- Matchmaking players')
            self.collector.start_match(p1_name=match.group(1), p2_name=match.group(2), tier=match.group(3),
                                       mode='MATCHMAKING')
            # Matchmaking players
            # Bets are OPEN for Gene vs Sannomiya_shiho! (S Tier)  (matchmaking) www.saltybet.com
            raise self.MessageFound()

    def parse_start_tournament(self, message):
        pattern = r'^Bets are OPEN for (.+) vs (.+)! \((.) Tier\) {2}tournament bracket: http://www\.saltybet\.com/shaker\?bracket=1$'
        match = re.compile(pattern).match(message)
        if match:
            logging.info('--- Tournament players')
            self.collector.start_match(p1_name=match.group(1), p2_name=match.group(2), tier=match.group(3),
                                       mode='TOURNAMENT')
            # Tournament players
            # Bets are OPEN for Reimu hm vs Akane ex! (S Tier)  tournament bracket: http://www.saltybet.com/shaker?bracket=1
            raise self.MessageFound()

    def parse_start_exhibition(self, message):
        pattern = r'^Bets are OPEN for (.+) vs (.+)! \(Requested by (.+)\) {2}\(exhibitions\) www\.saltybet\.com$'
        if re.compile(pattern).match(message):
            logging.info('--- Exhibition players')
            # Exhibition players
            # Bets are OPEN for Carriage driver vs Servant emiya! (Requested by Alipheese)  (exhibitions) www.saltybet.com
            raise self.MessageFound()

    def parse_locked(self, message):
        self.parse_locked_matchmaking_tournament(message)
        self.parse_locked_exhibition(message)

    def parse_locked_matchmaking_tournament(self, message):
        pattern = r'^Bets are locked\. (.+) \((.+)\) - \$(.+), (.+) \((.+)\) - \$(.+)$'
        match = re.compile(pattern).match(message)
        if match:
            logging.info('--- Matchmaking / Tournament locked')
            self.collector.lock_match(p1_streak=match.group(2), p1_amount=match.group(3), p2_streak=match.group(5),
                                      p2_amount=match.group(6))
            # Matchmaking locked
            # Bets are locked. Zerozuchi (-2) - $1,563,354, Koishi komeiji (-1) - $3,855,254
            raise self.MessageFound()

    def parse_locked_exhibition(self, message):
        pattern = r'^Bets are locked\. (.+)- \$(.+), (.+)- \$(.+)$'
        if re.compile(pattern).match(message):
            logging.info('--- Exhibition locked')
            # Exhibition locked
            # Bets are locked. Carriage driver- $1,480,823, Servant emiya- $3,008,605
            raise self.MessageFound()

    def parse_payout(self, message):
        pattern = r'^(.+) wins! Payouts to Team (.+)\.(.*)$'
        match = re.compile(pattern).match(message)
        if match:
            logging.info('--- Payout')
            self.collector.end_match(winner=match.group(1))
            # Matchmaking payout
            # Gyarados wins! Payouts to Team Blue. 93 more matches until the next tournament!
            # Ninja_kun wins! Payouts to Team Red. 10 characters are left in the bracket!
            # Spera wins! Payouts to Team Blue. FINAL ROUND! Stay tuned for exhibitions after the tournament!
            # Team HordesofLaw wins! Payouts to Team Red. 2 exhibition matches left!
            raise self.MessageFound()
