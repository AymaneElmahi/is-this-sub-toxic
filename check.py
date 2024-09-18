import sqlite3
import pandas as pd

def create_connection():
    try:
        conn = sqlite3.connect('reddit_comments.db')
        print("Successfully connected to SQLite database")
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to SQLite database: {e}")
        return None

def get_comments_with_scores():
    conn = create_connection()
    if conn is None:
        return None
    
    query = """
    SELECT id, body, toxicity_score
    FROM comments
    WHERE toxicity_score IS NOT NULL
    ORDER BY toxicity_score DESC
    LIMIT 10
    """
    
    try:
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except sqlite3.Error as e:
        print(f"Error executing query: {e}")
        conn.close()
        return None

def display_comments(df):
    if df is not None and not df.empty:
        for index, row in df.iterrows():
            print(f"Comment ID: {row['id']}")
            print(f"Body: {row['body'][:100]}...")  # Display first 100 characters
            print(f"Toxicity Score: {row['toxicity_score']:.4f}")
            print("-" * 50)
    else:
        print("No comments found or error occurred.")

if __name__ == "__main__":
    comments_df = get_comments_with_scores()
    display_comments(comments_df)