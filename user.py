from database import CursorFromConnectionFromPool


class User:
    def __init__(self, email, first_name, last_name, oauth_token, oauth_token_secret, id=None):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.id = id
        self.oauth_token = oauth_token
        self.oauth_token_secret = oauth_token_secret

    def __repr__(self):
        return '<User {}>'.format(self.email)

    def save_to_db(self):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('INSERT INTO users(first_name, last_name, email, oauth_token, oauth_token_secret) '
                           'VALUES (%s, %s, %s, %s, %s)',
                           (self.first_name, self.last_name, self.email, self.oauth_token, self.oauth_token_secret))

    @classmethod
    def load_from_db_by_email(cls, email):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('SELECT * FROM users WHERE users.email = %s LIMIT 1', (email,))
            data = cursor.fetchone()
            if data is not None:
                return cls(email=data[1], first_name=data[2], last_name=data[3]
                           , oauth_token=data[4], oauth_token_secret=data[5], id=data[0])
