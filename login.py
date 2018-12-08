import constants
import oauth2
import urllib.parse as urlparse
import json
from user import User
from database import Database


Database.initialise(user='jagxthtr',
                    password='puasVa9LZh0D58Dy7Z-h8VdmCppGNbko',
                    database='jagxthtr',
                    host='baasu.db.elephantsql.com',
                    port=5432)
consumer = oauth2.Consumer(constants.CONSUMER_KEY, constants.CONSUMER_SECRET)
user_email = input('Enter your email: ')
user = User.load_from_db_by_email(user_email)
if user is None:
    client = oauth2.Client(consumer)

    response, content = client.request(constants.REQUEST_TOKEN_URL, 'POST')
    if response.status is not 200:
        print("An error occurred")

    request_token = dict(urlparse.parse_qsl(content.decode('UTF-8')))

    print('Go to the following site in your browser: ')
    print("{}?oauth_token={}".format(constants.AUTHORIZATION_URL, request_token['oauth_token']))

    oauth_verifier = input('What is the PIN? ')

    token = oauth2.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
    token.set_verifier(oauth_verifier)
    client = oauth2.Client(consumer, token)

    response, content = client.request(constants.ACCESS_TOKEN_URL, 'POST')
    if response.status is not 200:
        pass
    access_token = dict(urlparse.parse_qsl(content.decode('UTF-8')))

    print(access_token)

    first_name = input('Name: ')
    last_name = input('Surname: ')

    user = User(user_email, first_name, last_name, access_token['oauth_token'], access_token['oauth_token_secret'], None)

    user.save_to_db()

print('oauth_token = {},\noauth_token_success = {}'.format(user.oauth_token, user.oauth_token_secret))
authorized_token = oauth2.Token(user.oauth_token, user.oauth_token_secret)
authorized_client = oauth2.Client(consumer, authorized_token)

response, content = authorized_client.request('https://api.twitter.com/1.1/search/tweets.json'
                                              '?q=computers+filter:images', 'GET')
if response.status is not 200:
    print('Error: response.status = {}'.format(response.status))

tweets = json.loads(content.decode('UTF-8'))
for tweet in tweets['statuses']:
    print(tweet['text'])
print('end')
