# 🔍 Subreddit Toxicity Analyzer

<p align="left">
<a href="https://www.python.org" target="_blank" rel="noreferrer">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" alt="python" width="40" height="40"/>
</a>
<a href="https://kafka.apache.org/" target="_blank" rel="noreferrer">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/apachekafka/apachekafka-original.svg" alt="kafka" width="40" height="40"/>
</a>
<a href="https://www.tensorflow.org" target="_blank" rel="noreferrer">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/tensorflow/tensorflow-original.svg" alt="tensorflow" width="40" height="40"/>
</a>
<a href="https://flask.palletsprojects.com/" target="_blank" rel="noreferrer">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/flask/flask-original.svg" alt="flask" width="40" height="40"/>
</a>
<a href="https://www.docker.com/" target="_blank" rel="noreferrer">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/docker/docker-original.svg" alt="docker" width="40" height="40"/>
</a>
<a href="https://www.sqlite.org/" target="_blank" rel="noreferrer">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/sqlite/sqlite-original.svg" alt="sqlite" width="40" height="40"/>
</a>
</p>

A real-time toxicity analysis tool that monitors Reddit comments and provides visualization of toxicity trends in subreddits. The system uses machine learning to analyze comment sentiment and displays the results through an interactive web interface.

<img src="images/Screenshot%20subreddit%20analyzer.jpeg" width="800" alt="Toxicity Analysis Dashboard">

## Overview

This tool helps monitor and analyze the toxicity levels in Reddit communities by:
- Collecting real-time comments from specified subreddits
- Analyzing comment toxicity using machine learning
- Visualizing toxicity trends over time
- Storing results for historical analysis

## 🏗️ Architecture

The project consists of several components:
- Reddit Scraper: Collects comments using PRAW
- Kafka Pipeline: Handles real-time data streaming
- ML Analysis: Uses XLNet for toxicity classification
- Flask Backend: Serves the API and web interface
- SQLite Database: Stores comments and analysis results

## ✨ Prerequisites

- Python 3.8+
- Docker and Docker Compose
- Reddit API credentials ([How to obtain](https://www.reddit.com/prefs/apps))

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/is-this-sub-toxic.git
cd is-this-sub-toxic
```

2. Create and activate a virtual environment:
```bash
python -m venv myenv
source myenv/bin/activate  # On Windows: myenv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

1. Set up environment variables by creating a `.env` file:
```bash
cat > .env << EOL
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT=script:is-this-sub-toxic:v1.0 (by /u/username)
REDDIT_USERNAME=your_username
REDDIT_PASSWORD=your_password
EOL
```

2. Start Kafka and Zookeeper:
```bash
docker-compose up -d
```

3. Initialize the database:
```bash
python reddit_scrapper/setup_database.py
```

## 💾 Database Schema

The SQLite database (`reddit_comments.db`) contains a single table with the following schema:

```sql
CREATE TABLE comments (
    id TEXT PRIMARY KEY,
    body TEXT NOT NULL,
    created_utc INTEGER,
    score INTEGER,
    toxicity_score REAL
)
```

## 🎮 Usage

### Option 1: Running All Components (Production)
```bash
# Terminal 1: Start Kafka Consumer and Comment Scraper
python reddit_scrapper/kafka_consumer.py & python reddit_scrapper/praw_connect.py

# Terminal 2: Run Toxicity Analyzer and Flask Server
python process_comments/toxicity_analyzer.py & python app.py
```

### Option 2: Component-by-Component (Development)
```bash
# Start each in a separate terminal:
python reddit_scrapper/kafka_consumer.py
python reddit_scrapper/praw_connect.py
python process_comments/toxicity_analyzer.py
python app.py
```

### Option 3: Using Docker Compose
```bash
docker-compose up --build  # Start all services
docker-compose down       # Stop all services
```

Access the web interface at `http://localhost:5000`

## 📁 Project Structure
```
is-this-sub-toxic/
├── process_comments/      # ML analysis components
├── reddit_scrapper/      # Data collection components
├── templates/           # Web interface templates
├── app.py              # Flask application
├── docker-compose.yml  # Docker configuration
├── requirements.txt    # Python dependencies
└── README.md
```

## 🔧 Components

### Reddit Scraper
- Fetches comments using PRAW
- Configurable subreddit targeting
- Built-in rate limiting
- Streams to Kafka topic

### Kafka Pipeline
- Producer: Streams Reddit comments
- Consumer: Processes and stores comments
- Ensures reliable data flow

### Toxicity Analysis
- XLNet-based classification
- Asynchronous processing
- Score range: 0 (non-toxic) to 1 (toxic)

### Web Interface
- Real-time visualization
- Interactive Chart.js graphs
- Responsive Tailwind CSS design

## 📊 Monitoring

View real-time logs:
```bash
# Kafka Consumer logs
docker logs -f kafka_consumer

# Flask Application logs
docker logs -f web_app
```

## 🔍 Troubleshooting

1. If Kafka connection fails:
```bash
docker-compose restart kafka
```

2. If database errors occur:
```bash
# Reset database
rm reddit_comments.db
python reddit_scrapper/setup_database.py
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Security Notes

Important security considerations:
- Never commit `.env` file or credentials
- Regenerate Reddit API credentials if exposed
- Use secrets management in production
- Keep the SQLite database secure
