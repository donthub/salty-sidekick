# Description

Collects and displays SaltyBet match information.

# Pre-requisites
## General
Python version `3.9` or greater.

`config.json`:

* `username`: Twitch username
* `oauth_token`: OAuth token for Twitch username.
    * E.g.: https://twitchapps.com/tmi/

`pip install -r requirements.txt`: Installs Python dependencies.

## Betting

For automatic betting to be enabled, Chrome is required, as well as the ChromeDriver executable in the root path.

`config.json`:

* `bet`: `true` to enable automatic betting, `false` otherwise
* `amount`: Automatic betting amount.

# Usage

* `py main.py`: Imports `database.sql`, if `database.db` does not exist. Records match outcomes in `database.db`. Prints
  collected match data for current players.
* `py export.py`: Exports `database.db` into `database.sql`.