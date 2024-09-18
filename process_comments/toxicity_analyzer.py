"""Analyze the comments and assign a toxicity score to each comment."""

import os
import sys
import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)
from reddit_scrapper.setup_database import create_connection

# Load the tokenizer and model for toxicity classification
tokenizer = AutoTokenizer.from_pretrained(
    "minh21/XLNet-Reddit-Toxic-Comment-Classification"
)
model = AutoModelForSequenceClassification.from_pretrained(
    "minh21/XLNet-Reddit-Toxic-Comment-Classification"
)

def predict_toxicity(text):
    """
    Predict the toxicity score for a given text.
    
    Args:
        text (str): The input text for which to predict toxicity.
    
    Returns:
        float: The predicted toxicity probability (0 to 1).
    """
    inputs = tokenizer(text, return_tensors="pt", truncation=False, padding=True)
    outputs = model(**inputs)
    probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
    toxic_prob = probabilities[0][1].item()  # Probability of the text being toxic
    return toxic_prob

def load_data():
    """
    Load comments from the database where the toxicity score is not yet assigned.
    
    Returns:
        pd.DataFrame: DataFrame containing the comments.
    """
    conn = create_connection()
    query = "SELECT id, body FROM comments WHERE toxicity_score IS NULL"
    data_frame = pd.read_sql_query(query, conn)
    conn.close()
    return data_frame

def update_database(toxicity_predictions):
    """
    Update the database with the predicted toxicity scores.
    
    Args:
        toxicity_predictions (list of tuple): A list of tuples containing 
        comment ID and toxicity score.
    """
    conn = create_connection()
    cursor = conn.cursor()
    for comment_id, score in toxicity_predictions:
        cursor.execute(
            "UPDATE comments SET toxicity_score = ? WHERE id = ?", (score, comment_id))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    # Load comments and predict toxicity for each comment
    df_comments = load_data()

    # Generate predictions and store them in a new variable (renamed to avoid shadowing)
    predictions = [(row['id'], predict_toxicity(row['body'])) for _, row in df_comments.iterrows()]

    # Update the database with the predictions
    update_database(predictions)
    print("Database updated with ML toxicity scores.")
