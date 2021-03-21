import json
import os


class Config:

    def __init__(self, path='config.json'):
        self.path = path
        self.auth = self.get_auth()

    def get_auth(self):
        if not os.path.isfile(self.path):
            with open(self.path, 'w', encoding='utf-8') as file:
                json.dump({'username': '', 'oauth_token': ''}, file)
            print('"config.json" created in root. Please modify it with the required values.')
            exit(-1)

        with open(self.path, 'r', encoding='utf-8') as file:
            auth = json.load(file)

        username = self.strip(auth['username'])
        oauth_token = self.strip(auth['oauth_token'])
        if len(username) == 0 or self.is_invalid_token(oauth_token):
            print('"config.json" in root is not configured properly. Please fill "username" and "oauth_token" values.')
            exit(-1)

        if not oauth_token.startswith('oauth:'):
            oauth_token = f"oauth:{auth['oauth_token']}"

        return username, oauth_token

    def strip(self, value):
        if value is None:
            return ''
        else:
            return value.strip()

    def is_invalid_token(self, value):
        oauth_prefix = 'oauth:'
        return len(value) == 0 or value.startswith(oauth_prefix) and len(value) == len(oauth_prefix)