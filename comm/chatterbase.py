import logging
from datetime import datetime, timedelta

import irc.bot


class ChatterBase(irc.bot.SingleServerIRCBot):

    def __init__(self, server, port, oauth_token, username):
        self.last_message_date = datetime.now()
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, oauth_token)], username, username)

    def start(self):
        self._connect()
        while True:
            if self.is_timeout():
                self.restart()
            self.reactor.process_once(timeout=0.2)

    def is_timeout(self):
        return datetime.now() - self.last_message_date > timedelta(minutes=5)

    def restart(self):
        logging.info('Chat has timed out. Restarting...')
        self.disconnect()
        self.last_message_date = datetime.now()
        self._connect()
        logging.info('Restarted...')
