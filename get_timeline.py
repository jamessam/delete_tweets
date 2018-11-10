'''This python3 script copies all available tweets to an AWS DynamoDB datastore.'''

import datetime
import json
import os

import boto3
from TwitterAPI import TwitterAPI


API_KEY=os.environ['API_KEY']
API_SECRET_KEY=os.environ['API_SECRET_KEY']
ACCESS_TOKEN=os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET=os.environ['ACCESS_TOKEN_SECRET']

DYNAMO_CLIENT = boto3.client('dynamodb')
TWITTER_API = TwitterAPI(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)


def main():
    max_id = os.environ['MAX_TWEET_ID']
    tweets = get_tweets(max_id)
    while len(tweets) > 1:
        [insert_tweet(tweet) for tweet in tweets]
        max_id = tweets[len(tweets)-1]['id']
        tweets = get_tweets(max_id)


def get_tweets(max_id):
    r = TWITTER_API.request('statuses/user_timeline',
        { 'screen_name': 'jamessamsf', 'count': 200, 'max_id': max_id })
    return json.loads(r.text)


def insert_tweet(tweet):
    print(f"Saving {tweet['id']} to DynamoDB.")
    DYNAMO_CLIENT.put_item(
        TableName=os.environ['DYNAMO_TABLE_ID'],
        Item={
            'ID': {
                'N': str(tweet['id'])
            },
            'Tweet': {
                'S': tweet['text']
            },
            'ReplyCount': {
                'N': '0'
            },
            'RetweetCount': {
                'N': str(tweet['retweet_count'])
            },
            'FavoriteCount': {
                'N': str(tweet['favorite_count'])
            },
            'TweetAsString': {
                'S': str(tweet)
            }
        }
    )


if __name__ == '__main__':
    main()
