from datetime import datetime
from json import loads
from TwitterAPI import TwitterAPI
from keys import API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET, database, twitter_user
import sqlite3
import sys
import argparse

class timeline:

    def __init__(self):
        self.api = TwitterAPI(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)

        # Connect to database
        self.db = sqlite3.connect(database)
        self.c = self.db.cursor()

        # create table if it doesn't exist
        self.c.execute('''CREATE TABLE IF NOT EXISTS 
            statuses(id INT UNIQUE, 
            created TEXT, 
            favorite_count INT,
            favorited TEXT,
            in_reply_to_screen_name TEXT,
            in_reply_to_status_id INT,
            in_reply_to_user_id INT,
            is_quote_status TEXT,
            lang TEXT,
            retweet_count INT,
            retweeted TEXT,
            source_app TEXT,
            tweet_text TEXT,
            truncated TEXT,
            tweeter_id INT)''')

    def get_tweets(self,max_id,count=200):
        r = self.api.request('statuses/user_timeline',
            { 'screen_name': twitter_user, 'count': count, 'max_id': max_id })
        data = loads(r.text)
        if len(data) < 2:
            yield 'The end'
        for datum in data:
            yield datum

    def insert_tweet(self, tweet):
        created = datetime.strptime(tweet['created_at'], "%a %b %d %H:%M:%S %z %Y")
        query = '''
            INSERT OR IGNORE INTO statuses (id, created, favorite_count, favorited,
                in_reply_to_screen_name, in_reply_to_status_id, in_reply_to_user_id,
                is_quote_status, lang, retweet_count, retweeted, source_app,
                tweet_text, truncated, tweeter_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        self.c.execute(query, (tweet['id'], str(created), tweet['favorite_count'],
            tweet['favorited'], tweet['in_reply_to_screen_name'],
            tweet['in_reply_to_status_id'], tweet['in_reply_to_user_id'],
            tweet['is_quote_status'], tweet['lang'], tweet['retweet_count'],
            tweet['retweeted'], tweet['source'], tweet['text'],
            tweet['truncated'], tweet['user']['id'] ))

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='''Get tweets from your timeline 
        and insert them into a sqlite database''')
    parser.add_argument("max_id",
        help="maximum tweet ID to pull from. Pull tweets prior to this id.")
    parser.add_argument("-n", help="number of tweets to pull per request")
    args = parser.parse_args()


    timeline = timeline()
    tweets = timeline.get_tweets(args.max_id)

    good_tweets = []

    while(True):
        try:
            tweet = next(tweets)
            if tweet == 'The end':
                sys.exit()
            print(tweet['id'])
            timeline.insert_tweet(tweet)
            max_id = tweet['id']
        except StopIteration:
            timeline.db.commit()
            tweets = timeline.get_tweets(max_id)
        except TypeError as e:
            print(e)

    timeline.db.commit()
