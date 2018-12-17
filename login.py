from user import User
from database import Database
from twitter_utils import get_request_token, get_oauth_verifier, get_access_token

# there is nothing interested in that database, I have it for learning only, so do not bother with accessing it
Database.initialise(user='jagxthtr',
                    password='puasVa9LZh0D58Dy7Z-h8VdmCppGNbko',
                    database='jagxthtr',
                    host='baasu.db.elephantsql.com',
                    port=5432)

user_email = input('Enter your email: ')
user = User.load_from_db_by_email(user_email)

if user is None:

    request_token = get_request_token()

    oauth_verifier = get_oauth_verifier(request_token)

    access_token = get_access_token(request_token, oauth_verifier)

    first_name = input('Name: ')
    last_name = input('Surname: ')

    user = User(user_email, first_name, last_name, access_token['oauth_token'], access_token['oauth_token_secret'], None)
    user.save_to_db()

tweets = user.twitter_request('https://api.twitter.com/1.1/search/tweets.json?q=computers+filter:images')

for tweet in tweets['statuses']:
    print(tweet['text'])
print('end')
