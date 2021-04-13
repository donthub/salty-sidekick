# Description

Collects and displays SaltyBet match information.

# Pre-requisites

Python version `3.9` or greater.

`config.json`:

* `username`: Twitch username
* `oauth_token`: OAuth token for Twitch username.

`py setup.py install`: Installs Python dependencies.

# Usage

* `py main.py`: Imports `database.sql`, if `database.db` does not exist. Records match outcomes in `database.db`. Prints
  collected match data for current players.
* `py export.py`: Exports `database.db` into `database.sql`.