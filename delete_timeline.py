from sys import argv

import tweepy

from connection import MySQLConnector
from keys import API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET
from keys import DATABASE, SERVER, USERNAME

query = 'select id, tweet_text from statuses where created <= "2016-06-15" and retweet_count !=0 and favorite_count !=0'

auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

with MySQLConnector(database=DATABASE, host=SERVER, port=3306, user=USERNAME,
    password=argv[1]) as connection:
    c = connection.cursor()
    c.execute(query)
    for tweet in c.fetchall():
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
