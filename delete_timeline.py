import os

import boto3
from boto3.dynamodb.conditions import Key, Attr
from TwitterAPI import TwitterAPI


API_KEY=os.environ['API_KEY']
API_SECRET_KEY=os.environ['API_SECRET_KEY']
ACCESS_TOKEN=os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET=os.environ['ACCESS_TOKEN_SECRET']

DYNAMO_CLIENT = boto3.resource('dynamodb')
DYNAMO_TABLE = DYNAMO_CLIENT.Table(os.environ['DYNAMO_TABLE_ID'])
TWITTER_API = TwitterAPI(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)


def main():
    tweets = get_tweets(int(os.environ['MIN_TWEET_ID']), int(os.environ['MAX_TWEET_ID']))
    for tweet in tweets:
        if tweet['ReplyCount'] > 0 or tweet['FavoriteCount'] > 0 or tweet['RetweetCount'] > 0:
            continue
        update_deleted_status(tweet)
        delete_tweet(tweet)


def get_tweets(min_id, max_id):
    fe = Key('ID').gte(min_id) & Attr('ReplyCount').eq('0') & Attr('RetweetCount').eq('0') & Attr('FavoriteCount').eq('0')
    response = DYNAMO_TABLE.scan(FilterExpression=fe)
    return response['Items']


def update_deleted_status(tweet):
    DYNAMO_TABLE.update_item(
        Key = { 'ID': tweet['ID'] },
        UpdateExpression='SET Deleted = :value',
        ExpressionAttributeValues={ ':value': True }
    )


def delete_tweet(tweet):
    tweet_id = tweet['ID']
    r = TWITTER_API.request(f'statuses/destroy/:{tweet_id}')
    if r.status_code == 200:
        print(f'Successfully deleted {tweet_id}')
    else:
        print(f'Could not delete {tweet_id}')


if __name__ == '__main__':
    main()
