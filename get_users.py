from json import dumps, loads
from sys import argv

from TwitterAPI import TwitterAPI

from connection import MySQLConnector
from keys import API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET
from keys import DATABASE, SERVER, USERNAME

def main():
    with MySQLConnector(USERNAME, argv[1], DATABASE, SERVER) as connection:
        cursor = connection.cursor()

        # Get users
        query = 'SELECT DISTINCT tweeter_id FROM notifications'
        cursor.execute(query)
        tweeters = cursor.fetchall()

        # Deposit in the users table
        for tweeter in tweeters:
            r = api.request('users/show', { 'id': tweeter[0] })
            account = loads(r.text)
            query = 'INSERT IGNORE INTO accounts (id, screen_name, name) \
                VALUES (%s, %s, %s)'
            cursor.execute(query, (account['id'], account['screen_name'],
                account['name']))

        connection.commit()
        cursor.close()


if __name__ == '__main__':
    api = TwitterAPI(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
    main()
