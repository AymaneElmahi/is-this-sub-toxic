from flask import Flask, render_template, jsonify
import sqlite3
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/toxicity-data')
def toxicity_data():
    conn = sqlite3.connect('reddit_comments.db')
    df = pd.read_sql_query("SELECT created_utc, toxicity_score FROM comments", conn)
    conn.close()
    
    df['created_utc'] = pd.to_datetime(df['created_utc'], unit='s')
    daily_avg = df.groupby(df['created_utc'].dt.date)['toxicity_score'].mean().reset_index()
    
    return jsonify(daily_avg.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)