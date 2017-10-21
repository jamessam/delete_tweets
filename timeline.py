from json import dumps, loads
from sys import exit
from TwitterAPI import TwitterAPI
from keys import API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET

api = TwitterAPI(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)

max_id = 914561491872780288

# r = api.request('statuses/mentions_timeline')

def get_tweets():
    r = api.request('statuses/user_timeline', { 'screen_name': 'jamessamsf', 'count': 200 })
    data = loads(r.text)
    if len(data) < 2:
        yield 'The end'

    for datum in data:
        yield datum

tweets = get_tweets()

good_tweets = []

while(True):
    try:
        tweet = next(tweets)
        if tweet['text'] == 'The end':
            break
        # retweeted
        if tweet['retweet_count'] > 0:
            good_tweets.append(tweet)
        # favorited
        if tweet['favorite_count'] > 0:
            good_tweets.append(tweet)
        # replied to someone
        if tweet['in_reply_to_screen_name']:
            good_tweets.append(tweet)
        # someone replied


        max_id = tweet['id']
    except StopIteration:
        # tweets = get_tweets()
        print('done')

# 'created_at', 'id', 'id_str', 'text', 'truncated', 'entities', 'source',
# 'in_reply_to_status_id', 'in_reply_to_status_id_str', 'in_reply_to_user_id',
# 'in_reply_to_user_id_str', 'in_reply_to_screen_name', 'user', 'geo',
# 'coordinates', 'place', 'contributors', 'is_quote_status', 'quoted_status_id',
# 'quoted_status_id_str', 'quoted_status', 'retweet_count', 'favorite_count',
# 'favorited', 'retweeted', 'possibly_sensitive', 'lang'])
