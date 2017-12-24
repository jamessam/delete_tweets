from datetime import datetime
from json import loads
import sqlite3
from TwitterAPI import TwitterAPI
from keys import API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET, database, twitter_user

api = TwitterAPI(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)

max_id = 569238353364717569

def get_tweets():
    r = api.request('statuses/user_timeline',
        { 'screen_name': twitter_user, 'count': 200, 'max_id': max_id })
    data = loads(r.text)
    if len(data) < 2:
        yield 'The end'
    for datum in data:
        yield datum

def insert_tweet(c, tweet):
    created = datetime.strptime(tweet['created_at'], "%a %b %d %H:%M:%S %z %Y")
    query = '''
        INSERT OR IGNORE INTO statuses (id, created, favorite_count, favorited,
            in_reply_to_screen_name, in_reply_to_status_id, in_reply_to_user_id,
            is_quote_status, lang, retweet_count, retweeted, source_app,
            tweet_text, truncated, tweeter_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
    c.execute(query, (tweet['id'], str(created), tweet['favorite_count'],
        tweet['favorited'], tweet['in_reply_to_screen_name'],
        tweet['in_reply_to_status_id'], tweet['in_reply_to_user_id'],
        tweet['is_quote_status'], tweet['lang'], tweet['retweet_count'],
        tweet['retweeted'], tweet['source'], tweet['text'],
        tweet['truncated'], tweet['user']['id'] ))

tweets = get_tweets()

good_tweets = []

# Connect to database
db = sqlite3.connect(database)
c = db.cursor()

# create table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS 
    statuses(id INT, 
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

while(True):
    try:
        tweet = next(tweets)
        if tweet == 'The end':
            break
        print(tweet['id'])
        insert_tweet(c, tweet)
        max_id = tweet['id']
    except StopIteration:
        db.commit()
        tweets = get_tweets()
    except TypeError as e:
        print(e)

db.commit()
