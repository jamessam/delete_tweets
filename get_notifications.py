from datetime import datetime
from json import loads

from TwitterAPI import TwitterAPI

from connection import MySQLConnector
from keys import API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET
from keys import DATABASE, SERVER, USERNAME, PASSWORD

max_id = 755835471675072512

def insert_tweet(c, tweet):
    created = datetime.strptime(tweet['created_at'], "%a %b %d %H:%M:%S %z %Y")
    query = '''
        INSERT IGNORE INTO notifications (id, created, favorite_count, favorited,
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
    tweets = loads(r.text)
    if len(tweets) < 2:
        yield 'The end'
    else:
        for tweet in tweets:
            yield tweet

def main():
    tweets = get_tweets()

    with MySQLConnector(user=USERNAME, password=argv[1], database=DATABASE,
        host=SERVER) as connection:
        c = connection.cursor()

        while(True):
            try:
                tweet = next(tweets)
                if tweet == 'The end':
                    break
                if tweet['id'] == max_id:
                    continue
                else:
                    print(tweet['id'])
                    insert_tweet(c, tweet)
                max_id = tweet['id']
            except StopIteration:
                tweets = get_tweets()
            except TypeError as e:
                print(e)
                break

        connection.commit()
        c.close()


if __name__ == '__main__':
    api = TwitterAPI(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
    main()
