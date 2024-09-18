import sqlite3
from sqlite3 import Error

def create_connection():
    conn = None;
    try:
        conn = sqlite3.connect('reddit_comments.db')
        print(f"Successfully connected to SQLite database")
        return conn
    except Error as e:
        print(f"Error connecting to SQLite database: {e}")
    
    return conn

def create_table(conn):
    try:
        cursor = conn.cursor()
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

def insert_comment(conn, comment):
    sql = ''' INSERT OR REPLACE INTO comments(id, body, created_utc, score)
              VALUES(?,?,?,?) '''
    try:
        cur = conn.cursor()
        cur.execute(sql, comment)
        conn.commit()
        return cur.lastrowid
    except Error as e:
        print(f"Error inserting comment: {e}")

if __name__ == '__main__':
    conn = create_connection()
    if conn is not None:
        create_table(conn)
        conn.close()
    else:
        print("Error! Cannot create the database connection.")