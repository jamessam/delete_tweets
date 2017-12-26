from contextlib import contextmanager
from mysql.connector import connect

@contextmanager
def MySQLConnector(user,password,database,host):
    handle = connect(user=user, password=password, database=database, host=host)
    yield handle
    handle.close()
