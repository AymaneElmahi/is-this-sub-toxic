import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import sys
import os

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from reddit_scrapper.setup_database import create_connection

tokenizer = AutoTokenizer.from_pretrained("minh21/XLNet-Reddit-Toxic-Comment-Classification")
model = AutoModelForSequenceClassification.from_pretrained("minh21/XLNet-Reddit-Toxic-Comment-Classification")

def predict_toxicity(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    outputs = model(**inputs)
    probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
    toxic_prob = probabilities[0][1].item()
    return toxic_prob

def load_data():
    conn = create_connection()
    query = "SELECT id, body FROM comments WHERE toxicity_score IS NULL"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def update_database(predictions):
    conn = create_connection()
    cursor = conn.cursor()
    for id, score in predictions:
        cursor.execute("UPDATE comments SET toxicity_score = ? WHERE id = ?", (score, id))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    df = load_data()
    predictions = [(row['id'], predict_toxicity(row['body'])) for _, row in df.iterrows()]
    update_database(predictions)
    print("Database updated with ML toxicity scores.")