from datetime import datetime
from json import loads
from sys import argv

from TwitterAPI import TwitterAPI

from connection import MySQLConnector
from keys import API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET
from keys import DATABASE, SERVER, USERNAME


def get_tweets(max_id):
    r = api.request('statuses/user_timeline',
        { 'screen_name': 'jamessamsf', 'count': 200, 'max_id': max_id })
    data = loads(r.text)
    if len(data) < 2:
        yield 'The end'
    for datum in data:
        yield datum

def insert_tweet(c, tweet):
    created = datetime.strptime(tweet['created_at'], "%a %b %d %H:%M:%S %z %Y")
    query = '''
        INSERT IGNORE INTO statuses (id, created, favorite_count, favorited,
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

def main():
    max_id = 947601267206930432
    tweets = get_tweets(max_id)
    good_tweets = []

    with MySQLConnector(USERNAME, argv[1], DATABASE, SERVER) as connection:
        cursor = connection.cursor()

        while(True):
            try:
                tweet = next(tweets)
                if tweet == 'The end':
                    break
                print(tweet['id'])
                insert_tweet(cursor, tweet)
                max_id = tweet['id']
            except StopIteration:
                connection.commit()
                tweets = get_tweets(max_id)
            except TypeError as e:
                print(e)

        connection.commit()
        cursor.close()


if __name__ == '__main__':
    api = TwitterAPI(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
    main()
