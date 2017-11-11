# About
Some python scripts I used to clear out tweets from my account. Done as a personal project for fun, it's not the cleanest code, and it's totally lacking tests (which were done manually). Unfortunately, what's not here is the SQL code used to populate the reply_count.

* favorites.py removes most likes before a certain date/tweet.
* get_notifications.py stores all notifications I've received in a MySQL DB table.
* get_timeline.py stores a little under 3k of my tweets in a MySQL DB table.
* get_users.py should have been built into the notifications script. It collections account information of people that have mentioned me.
* delete_timeline.py deletes from my timeline.
