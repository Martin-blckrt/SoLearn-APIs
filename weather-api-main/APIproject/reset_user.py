import sqlite3
from sqlite3 import Error
import os

PATH = os.path.join(os.getcwd(), 'db.sqlite3')

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def delete_users(conn):
    """
    Delete all users from the table users_user
    :param conn:
    :param task:
    :return: project id
    """
    sql = ''' DELETE FROM users_user'''
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()


def main():
    conn = create_connection(PATH)
    with conn:
        delete_users(conn)


if __name__ == '__main__':
    main()