from json import dumps, loads

from TwitterAPI import TwitterAPI

from connection import MySQLConnector
from keys import API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET
from keys import DATABASE, SERVER, USERNAME, PASSWORD


def main():
    with MySQLConnector(user=USERNAME, password=argv[1], database=DATABASE,
        host=SERVER) as connection:

        c = connection.cursor()

        # Get users
        query = 'SELECT DISTINCT tweeter_id FROM notifications'
        c.execute(query)
        tweeters = c.fetchall()

        # Deposit in the users table
        for tweeter in tweeters:
            r = api.request('users/show', { 'id': tweeter[0] })
            account = loads(r.text)
            query = 'INSERT IGNORE INTO accounts (id, screen_name, name) \
                VALUES (%s, %s, %s)'
            c.execute(query, (account['id'], account['screen_name'],
                account['name']))

        connection.commit()
        c.close()


if __name__ == '__main__':
    api = TwitterAPI(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
    main()
