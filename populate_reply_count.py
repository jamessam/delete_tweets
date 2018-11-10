import datetime
import json
import os

import boto3
from TwitterAPI import TwitterAPI


API_KEY=os.environ['API_KEY']
API_SECRET_KEY=os.environ['API_SECRET_KEY']
ACCESS_TOKEN=os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET=os.environ['ACCESS_TOKEN_SECRET']

DYNAMO_CLIENT = boto3.resource('dynamodb')
DYNAMO_TABLE = DYNAMO_CLIENT.Table(os.environ['DYNAMO_TABLE_ID'])
TWITTER_API = TwitterAPI(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)


def main():
    max_id = os.environ['MAX_TWEET_ID']
    tweets = get_tweets_at_me(max_id)
    while len(tweets) > 1:
        for tweet_at_me in tweets:
            print(f'Processing tweet_at_me {tweet_at_me["id"]}')
            max_id = tweet_at_me['id']
            my_tweet = get_tweet_by_id(tweet_at_me['in_reply_to_status_id'])
            if not my_tweet:
                continue
            update_reply_count(my_tweet)
            tweets = get_tweets_at_me(max_id)
        tweets = get_tweets_at_me(max_id)


def get_tweets_at_me(max_id):
    r = TWITTER_API.request('statuses/mentions_timeline', {'max_id': max_id})
    return json.loads(r.text)


def update_reply_count(tweet):
    reply_count = int(tweet['ReplyCount']) + 1
    DYNAMO_TABLE.update_item(
        Key = { 'ID': tweet['ID'] },
        UpdateExpression='SET ReplyCount = :value',
        ExpressionAttributeValues={ ':value': reply_count }
    )


def get_tweet_by_id(identifier):
    try:
        response = DYNAMO_TABLE.get_item(Key = { 'ID': identifier })
        tweet = response['Item']
    except:
        tweet = None
    return tweet


if __name__ == "__main__":
    main()