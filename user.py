import oauth2
import json
from database import CursorFromConnectionFromPool
from twitter_utils import consumer


class User:
    def __init__(self, screen_name, oauth_token, oauth_token_secret, id=None):
        self.screen_name = screen_name
        self.id = id
        self.oauth_token = oauth_token
        self.oauth_token_secret = oauth_token_secret

    def __repr__(self):
        return '<Class User object:\n' \
               'screen_name: {}\n' \
               'id: {}\n' \
               'token: {}\n' \
               'token secret: {}>'.format(self.screen_name, self.id,
                                          self.oauth_token, self.oauth_token_secret)

    def save_to_db(self):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('INSERT INTO users(screen_name, oauth_token, oauth_token_secret) '
                           'VALUES (%s, %s, %s)',
                           (self.screen_name, self.oauth_token, self.oauth_token_secret))

    @classmethod
    def load_from_db_by_screen_name(cls, screen_name):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('SELECT * FROM users WHERE screen_name = %s LIMIT 1', (screen_name,))
            data = cursor.fetchone()
            if data is not None:
                return cls(screen_name=data[1], oauth_token=data[2], oauth_token_secret=data[3], id=data[0])

    def twitter_request(self, url, verb='GET'):
        authorized_token = oauth2.Token(self.oauth_token, self.oauth_token_secret)
        authorized_client = oauth2.Client(consumer, authorized_token)

        response, content = authorized_client.request(url, verb)
        if response.status is not 200:
            print('Error: response.status = {}'.format(response.status))
            print(response)
            print(content)

        return json.loads(content.decode('utf-8'))

