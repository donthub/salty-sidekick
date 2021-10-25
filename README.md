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

`pip install -r requirements.txt`: Installs Python dependencies.

## Automatic betting

For automatic betting to be enabled, the following is required:

* Chrome / Chromium installed.
* ChromeDriver executable:
    * Windows: In project root, or via PATH.
    * Linux: Via PATH.

`config.json`:

* `simple_ui`: `true` to display Twitch stream and chat, `false` otherwise.
* `bet`: `true` to enable automatic betting, `false` otherwise.
* `amount`: Automatic betting amount for matchmaking. Tournaments are all in, exhibitions are ignored.
* `min_balance`: If automatic betting would result in balance lower than this amount, betting will not be performed.

# Usage

* `py main.py`:
    * Imports `database.sql`, if `database.db` does not exist.
    * Records match outcomes in `database.db`.
    * Prints collected match data for current players.
    * Bets on matches automatically, if enabled.
* `py export.py`: Exports `database.db` into `database.sql`.