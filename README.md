# Description

Collects and displays SaltyBet match information, with optional automatic betting.

# Disclaimer

Using this application - automatic betting specially - may be against SaltyBet's Terms of Service. Use at your own risk.

# Pre-requisites

## General

Python version `3.9` or greater.

`config.json`:

* `username`: Twitch username.
* `oauth_token`: OAuth token for Twitch username.
    * E.g.: https://twitchapps.com/tmi/
* `stats_games`: Total stats calculation with this number of last games.

`pip install -r requirements.txt`: Installs Python dependencies.

## Automatic betting

For automatic betting to be enabled, the following is required:

* Chrome / Chromium installed.
* ChromeDriver executable:
    * Windows: In project root, or via PATH.
    * Linux: Via PATH.

`config.json`:

* `bet`: `true` to enable automatic betting, `false` otherwise.
* `simple_ui`: `true` to display Twitch stream and chat, `false` otherwise.
* `amount`: Betting amount for matchmaking if winrate probability of characters are out of range.
* `amount_direct`: Betting amount for matchmaking between characters with direct match history.
* `amount_close`: Betting amount for matchmaking if winrate probability of characters are within range.
* `min_balance`: Betting will not lower balance below this value.
* `close_range`: Bet upset if winrate probability of the characters are within this range (percent).

Tournaments are all in, exhibitions are ignored.

# Usage

* `py main.py`:
    * Imports `database.sql`, if `database.db` does not exist.
    * Records match outcomes in `database.db`.
    * Prints collected match data for current players.
    * Bets on matches automatically, if enabled.
* `py export.py`: Exports `database.db` into `database.sql`.