from contextlib import contextmanager
from datetime import datetime
from json import dumps, loads
from sys import exit

import mysql.connector
from TwitterAPI import TwitterAPI

from keys import API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET
from keys import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION
from keys import DATABASE, SERVER, USERNAME, PASSWORD


api = TwitterAPI(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)

max_id = 920670442926481409

def insert_tweet(c, tweet):
    created = datetime.strptime(tweet['created_at'], "%a %b %d %H:%M:%S %z %Y")
    query = '''
        INSERT INTO notifications (id, created, favorite_count, favorited,
            in_reply_to_screen_name, in_reply_to_status_id, in_reply_to_user_id,
            is_quote_status, lang, retweet_count, retweeted, source_app,
            tweet_text, truncated, tweeter_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
    c.execute(query, (tweet['id'], str(created), tweet['favorite_count'],
        tweet['favorited'], tweet['in_reply_to_screen_name'],
        tweet['in_reply_to_status_id'], tweet['in_reply_to_user_id'],
        tweet['is_quote_status'], tweet['lang'], tweet['retweet_count'],
        tweet['retweeted'], tweet['source'], tweet['text'],
        tweet['truncated'], tweet['user']['id'] ))

def get_tweets():
    r = api.request('statuses/mentions_timeline', {'max_id': max_id})
    data = loads(r.text)
    if len(data) < 2:
        yield 'The end'
    for datum in data:
        max_id = datum['id']
        yield datum

a = open('916408912718565377.json')
tweet = loads(a.read())
a.close()

# Connect to database
connection = mysql.connector.connect(database=DATABASE, host=SERVER, port=3306, user=USERNAME, password=PASSWORD)
c = connection.cursor()

try:
    insert_tweet(c, tweet)
except Exception as e:
    print(e)

connection.commit()
c.close()
connection.close()
connection.disconnect()
