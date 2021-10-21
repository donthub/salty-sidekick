import logging
from datetime import datetime

from comm.chatterbase import ChatterBase
from comm.messageparser import MessageParser


class Chatter(ChatterBase):
    def __init__(self, config, collector, channel='saltybet'):
        self.collector = collector
        self.parser = MessageParser(collector)

        self.channel = '#' + channel
        self.last_message_date = datetime.now()

        server = 'irc.chat.twitch.tv'
        port = 6667
        logging.info(f'Connecting to {server} on port {port}...')

        username = config.auth[0]
        oauth_token = config.auth[1]
        ChatterBase.__init__(self, server, port, oauth_token, username)

    def on_welcome(self, connection, event):
        self.collector.state = None
        logging.info(f'Joining {self.channel}...')

        connection.join(self.channel)
        logging.info('Joined.')

    def on_pubmsg(self, connection, event):
        self.last_message_date = datetime.now()
        if event.source.nick != 'waifu4u':
            return

        message = event.arguments[0]
        logging.debug(f'{event.source.nick}: {message}')
        self.parser.parse(message)
