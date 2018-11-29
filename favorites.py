import os
from json import loads
from sys import exit
from TwitterAPI import TwitterAPI


api = TwitterAPI(
    os.environ['API_KEY'],
    os.environ['API_SECRET_KEY'],
    os.environ['ACCESS_TOKEN'],
    os.environ['ACCESS_TOKEN_SECRET'])


def favorite_tweets():
    count = 0
    r = api.request('favorites/list', {
        'screen_name': 'jamessamsf',
        'count': 200,
        'max_id': os.environ['MAX_TWEET_ID'] })
    data = loads(r.text)
    if len(data) < 2:
        print('We\'ve exhausted favorite tweets.')
        yield 'We\'ve exhausted favorite tweets.'
    else:
        for i in data:
            count += 1
            yield count, i['user']['screen_name'], i['id'], i['text']

favorites = favorite_tweets()

while(True):
    try:
        favorite = next(favorites)
        print(favorite)
        if favorite == 'We\'ve exhausted favorite tweets.':
            break
        else:
            r = api.request('favorites/destroy', {
                'screen_name': 'jamessamsf', 'id': favorite[2] })
        delete_after = favorite[2]
    except StopIteration:
        favorites = favorite_tweets()

print(delete_after)
