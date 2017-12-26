import mysql.connector
import tweepy
from sys import argv
from keys import API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET
from keys import DATABASE, SERVER, USERNAME

query = 'select id, tweet_text from statuses where created <= "2016-06-15" and retweet_count !=0 and favorite_count !=0'

# Connect to database
connection = mysql.connector.connect(database=DATABASE, host=SERVER, port=3306, user=USERNAME, password=argv[1])
c = connection.cursor()

c.execute(query)
tweets_to_delete = c.fetchall()

auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth)

for tweet in tweets_to_delete:
    print(tweet)
#     identifier = tweet[0]
#     print(identifier)
#     try:
#         api.destroy_status(identifier)
#     except Exception as e:
#         print(e)
#         # c.execute('DELETE FROM statuses WHERE id = %s', identifier)
#         # connection.commit()

connection.commit()
c.close()
connection.close()
connection.disconnect()



#  r = api.request('statuses/update', { 'status': 'test' })
# r = api.request('favorites/destroy', { 'screen_name': 'jamessamsf', 'id': 923079678738309120 })
# r = api.request('statuses/destroy/:id', { 'id_str': '923079678738309120' })
