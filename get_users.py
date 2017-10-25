from json import dumps, loads
import mysql.connector
from TwitterAPI import TwitterAPI
from keys import API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET
from keys import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION
from keys import DATABASE, SERVER, USERNAME, PASSWORD

api = TwitterAPI(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)

# Connect to database
connection = mysql.connector.connect(database=DATABASE, host=SERVER, port=3306, user=USERNAME, password=PASSWORD)
c = connection.cursor()

# Get users
query = 'SELECT DISTINCT tweeter_id FROM notifications'
c.execute(query)
tweeters = c.fetchall()

# Deposit in the users table
for tweeter in tweeters:
    r = api.request('users/show', { 'id': tweeter[0] })
    account = loads(r.text)
    query = 'INSERT IGNORE INTO accounts (id, screen_name, name) VALUES (%s, %s, %s)'
    c.execute(query, (account['id'], account['screen_name'], account['name']))

connection.commit()
c.close()
connection.close()
connection.disconnect()
