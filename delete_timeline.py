import mysql.connector
import tweepy
from keys import API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET
from keys import DATABASE, SERVER, USERNAME, PASSWORD

query = 'select id, tweet_text from statuses where created between "2016-01-01" and "2016-12-31"'

# Connect to database
connection = mysql.connector.connect(database=DATABASE, host=SERVER, port=3306, user=USERNAME, password=PASSWORD)
c = connection.cursor()

c.execute(query)
tweets_to_delete = c.fetchall()

auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth)

for tweet in tweets_to_delete:
    identifier = tweet[0]
    print(identifier)
    try:
        api.destroy_status(identifier)
    except Exception as e:
        print(e)
        # c.execute('DELETE FROM statuses WHERE id = %s', identifier)
        # connection.commit()

connection.commit()
c.close()
connection.close()
connection.disconnect()
