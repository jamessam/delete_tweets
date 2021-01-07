import json
import os
from sys import argv

import boto3
from boto3.dynamodb.conditions import Key, Attr
from TwitterAPI import TwitterAPI


API_KEY = os.environ["API_KEY"]
API_SECRET_KEY = os.environ["API_SECRET_KEY"]
ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = os.environ["ACCESS_TOKEN_SECRET"]

DYNAMO_CLIENT = boto3.resource("dynamodb")
DYNAMO_TABLE = DYNAMO_CLIENT.Table(os.environ["DYNAMO_TABLE_ID"])
TWITTER_API = TwitterAPI(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)


def main():
    tweet_id = int(argv[1])
    tweet = get_tweet(tweet_id)
    insert_tweet(tweet)
    delete_tweet(tweet_id)


def get_tweet(tweet_id):
    r = TWITTER_API.request(f"statuses/show/:{tweet_id}")
    return json.loads(r.text)


def insert_tweet(tweet):
    tweet_id = tweet["id"]
    print(f"Saving {tweet_id} to DynamoDB.")
    DYNAMO_TABLE.put_item(
        Item={
            "ID": tweet_id,
            "Tweet": tweet["text"],
            "RetweetCount": tweet["retweet_count"],
            "FavoriteCount": tweet["favorite_count"],
            "TweetAsString": str(tweet),
        },
    )


def delete_tweet(tweet_id):
    r = TWITTER_API.request(f"statuses/destroy/:{tweet_id}")
    if r.status_code == 200:
        print(f"Successfully deleted {tweet_id}")
        update_deleted_status(tweet_id)
    else:
        print(f"Could not delete {tweet_id}")


def update_deleted_status(tweet_id):
    DYNAMO_TABLE.update_item(
        Key={"ID": tweet_id},
        UpdateExpression="SET Deleted = :value",
        ExpressionAttributeValues={":value": True},
    )


if __name__ == "__main__":
    main()
