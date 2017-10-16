from json import loads
from sys import exit
from TwitterAPI import TwitterAPI
from keys import API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET

delete_after = 512718759794974720
api = TwitterAPI(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)

def favorite_tweets():
    count = 0
    r = api.request('favorites/list', { 'screen_name': 'jamessamsf', 'count': 200, 'max_id': delete_after })
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
        if favorite[1] == 'Hoodline':
            pass
        elif favorite[1] == 'mattVDileo':
            pass
        elif 'aesorg' in favorite[3].lower():
            pass
        else:
            r = api.request('favorites/destroy', { 'screen_name': 'jamessamsf', 'id': favorite[2] })
        delete_after = favorite[2]
    except StopIteration:
        favorites = favorite_tweets()

print(delete_after)
