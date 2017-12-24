from datetime import datetime
from json import loads
import sys
import sqlite3
import argparse
from TwitterAPI import TwitterAPI
from keys import API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET, database, twitter_user

class notifications:

    def __init__(self):
        # twitter API
        self.api = TwitterAPI(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
        
        # Connect to database
        self.db = sqlite3.connect(database)
        self.c = self.db.cursor()

        # Create table for notifications if it doesn't exist
        self.c.execute('''CREATE TABLE IF NOT EXISTS notifications(id INT UNIQUE,
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

        self.c.execute('''CREATE TABLE IF NOT EXISTS accounts(id INT UNIQUE,
            screen_name TEXT,
            name TEXT)''')

    def insert_tweet(self, tweet):
        created = datetime.strptime(tweet['created_at'], "%a %b %d %H:%M:%S %z %Y")
        query = '''
            INSERT or IGNORE INTO notifications (id, created, favorite_count, favorited,
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

        # insert users
        r = self.api.request('users/show', { 'id': tweet['user']['id'] })
        account = loads(r.text)
        query = 'INSERT OR IGNORE INTO accounts (id, screen_name, name) VALUES (?, ?, ?)'
        self.c.execute(query, (account['id'], account['screen_name'], account['name']))

        self.db.commit()

    def get_tweets(self, max_id):
        r = self.api.request('statuses/mentions_timeline', {'max_id': max_id})
        tweets = loads(r.text)
        if len(tweets) < 2:
            yield 'The end'
        else:
            for tweet in tweets:
                yield tweet

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='''Get notifications 
        and insert them into a sqlite database''')
    parser.add_argument("max_id",
        help="maximum tweet ID to pull from. Pull tweets prior to this id.")
    parser.add_argument("-n", help="number of tweets to pull per request")
    args = parser.parse_args()

    notifications = notifications()

    tweets = notifications.get_tweets(args.max_id)

    while(True):
        try:
            tweet = next(tweets)
            if tweet == 'The end':
                sys.exit()
            if tweet['id'] == args.max_id:
                continue
            else:
                print(tweet['id'])
                notifications.insert_tweet(tweet)
            max_id = tweet['id']
        except StopIteration:
            tweets = notifications.get_tweets(max_id)
        except TypeError as e:
            sys.exit(e)
