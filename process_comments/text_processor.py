import re
import nltk
nltk.download('punkt_tab')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')

def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters and digits
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Tokenize the text
    tokens = word_tokenize(text)
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    
    # Join the tokens back into a string
    processed_text = ' '.join(tokens)
    
    return processed_text

# Test the function
if __name__ == "__main__":
    sample_text = "This is a sample comment! It has some punctuation, and some numbers like 123."
    processed = preprocess_text(sample_text)
    print(f"Original: {sample_text}")
    print(f"Processed: {processed}")