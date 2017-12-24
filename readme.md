# About
Some python scripts I used to clear out tweets from my account. Done as a personal project for fun, it's not the cleanest code, and it's totally lacking tests (which were done manually). Unfortunately, what's not here is the SQL code used to populate the reply_count.

* favorites.py removes most likes before a certain date/tweet.
* get_notifications.py stores all notifications I've received in a sqlite table.
* get_timeline.py stores a little under 3k of my tweets in a sqlite table.
* get_users.py should have been built into the notifications script. It collections account information of people that have mentioned me.
* delete_timeline.py deletes from my timeline.

Requires a `keys.py` with the following:

* **API_KEY**
* **API_SECRET**
* **ACCESS_TOKEN**
* **ACCESS_SECRET**
* twitter_user
* database

The API key and secret and the access token and secret are retrieved from https://apps.twitter.com. The *twitter_user* is the twitter username for the user you are retrieving information for. *database* is the path for the sqlite database file.

# Usage

## timeline

`python3 get_timeline.py tweet_id`

*tweet_id* is the latest tweet you want to retrieve.

## notifications

`python3 get_notifications.py tweet_id`

*tweet_id* is the latest tweet you want to retrieve.