"""Setup a SQLite database for storing Reddit comments."""

import sqlite3
from sqlite3 import Error

def create_connection():
    """
    Create a database connection to the SQLite database.
    
    Returns:
        conn: SQLite connection object or None if an error occurs.
    """
    connection = None
    try:
        connection = sqlite3.connect('reddit_comments.db')
        print("Successfully connected to SQLite database")
        return connection
    except Error as e:
        print(f"Error connecting to SQLite database: {e}")

    return connection

def create_table(connection):
    """
    Create the comments table in the database if it does not exist.
    
    Args:
        connection: SQLite connection object.
    """
    try:
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS comments (
                id TEXT PRIMARY KEY,
                body TEXT NOT NULL,
                created_utc INTEGER,
                score INTEGER,
                toxicity_score REAL
            )
        ''')
        print("Table 'comments' created successfully")
    except Error as e:
        print(f"Error creating table: {e}")

def insert_comment(connection, comment):
    """
    Insert or replace a comment into the comments table.
    
    Args:
        connection: SQLite connection object.
        comment: A tuple containing comment data (id, body, created_utc, score).
    
    Returns:
        The row ID of the inserted comment, or None if an error occurs.
    """
    sql = ''' INSERT OR REPLACE INTO comments(id, body, created_utc, score)
              VALUES(?,?,?,?) '''
    try:
        cur = connection.cursor()
        cur.execute(sql, comment)
        connection.commit()
        return cur.lastrowid
    except Error as e:
        print(f"Error inserting comment: {e}")
        return None

if __name__ == '__main__':
    conn = create_connection()
    if conn is not None:
        create_table(conn)
        conn.close()
    else:
        print("Error! Cannot create the database connection.")
