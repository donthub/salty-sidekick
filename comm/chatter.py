import irc.bot
import re


class Chatter(irc.bot.SingleServerIRCBot):
    def __init__(self, config, collector, channel='saltybet'):
        self.collector = collector
        self.channel = '#' + channel

        # Create IRC bot connection
        server = 'irc.chat.twitch.tv'
        port = 6667
        print(f'Connecting to {server} on port {port}...')

        auth = config.get_auth()
        username = auth[0]
        oauth_token = auth[1]
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, oauth_token)], username, username)

    def on_welcome(self, connection, event):
        print(f'Joining {self.channel}...')

        # You must request specific capabilities before you can use them
        # c.cap('REQ', ':twitch.tv/membership')
        # c.cap('REQ', ':twitch.tv/tags')
        # c.cap('REQ', ':twitch.tv/commands')
        connection.join(self.channel)
        print('Joined.')

    def on_pubmsg(self, connection, event):
        message = event.arguments[0]
        # print(f'{event.source.nick}: {message}')

        if event.source.nick != 'waifu4u':
            return

        if re.compile(
                r'^Bets are OPEN for (.+) vs (.+)! \(Requested by (.+)\) {2}\(exhibitions\) www\.saltybet\.com$').match(
                message):
            # print('--- Exhibition players')
            # Exhibition players
            # Bets are OPEN for Carriage driver vs Servant emiya! (Requested by Alipheese)  (exhibitions) www.saltybet.com
            pass

        match = re.compile(
            r'^Bets are OPEN for (.+) vs (.+)! \((.) Tier\) {2}\(matchmaking\) www\.saltybet\.com$').match(message)
        if match:
            # print('--- Match players')
            self.collector.start_match(p1_name=match.group(1), p2_name=match.group(2), tier=match.group(3))
            # Match players
            # Bets are OPEN for Gene vs Sannomiya_shiho! (S Tier)  (matchmaking) www.saltybet.com
            pass

        if re.compile(r'^Bets are locked\. (.+)- \$(.+), (.+)- \$(.+)$').match(message):
            # print('--- Exhibition locked')
            # Exhibition locked
            # Bets are locked. Carriage driver- $1,480,823, Servant emiya- $3,008,605
            pass

        match = re.compile(r'^Bets are locked\. (.+) \((.+)\) - \$(.+), (.+) \((.+)\) - \$(.+)$').match(message)
        if match:
            # print('--- Player locked')
            self.collector.lock_match(p1_streak=match.group(2), p1_amount=match.group(3), p2_streak=match.group(5),
                                      p2_amount=match.group(6))
            # Player locked
            # Bets are locked. Zerozuchi (-2) - $1,563,354, Koishi komeiji (-1) - $3,855,254
            pass

        if re.compile(r'^(.+) wins! Payouts to Team (.+)\. (.+) exhibition matches left!$').match(message):
            # print('--- Exhibition payout')
            # Exhibition payout
            # Team HordesofLaw wins! Payouts to Team Red. 2 exhibition matches left!
            pass

        match = re.compile(r'^(.+) wins! Payouts to Team (.+)\. (.+) more matches until the next tournament!$').match(
            message)
        if match:
            # print('--- Player payout')
            self.collector.end_match(winner=match.group(1))
            # Player payout
            # Gyarados wins! Payouts to Team Blue. 93 more matches until the next tournament!
            pass
