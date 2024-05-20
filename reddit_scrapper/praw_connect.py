"""Module providingFunction printing python version."""

import json
import praw
from kafka import KafkaProducer
from colorama import Fore, Style, init

# Setup Reddit connection using PRAW with credentials from praw.ini
reddit = praw.Reddit(site_name="DEFAULT")  # The section name in praw.ini

# Choose the subreddit
subreddit = reddit.subreddit("EASportsFC")

# Setup Kafka producer
producer = KafkaProducer(
    bootstrap_servers=["localhost:9092"],
    value_serializer=lambda m: json.dumps(m).encode("ascii"),
)

init(autoreset=True)

# Fetch and send a limited number of comments to Kafka
COMMENT_LIMIT = 10  # Set the number of comments you want to fetch
for comment in subreddit.stream.comments(pause_after=-1):
    if comment is None:
        break
    message = {"id": comment.id, "body": comment.body}
    producer.send("reddit_comments", value=message)
    producer.flush()
    print(
        f"{Fore.GREEN}Sent {Style.RESET_ALL}{comment.body}{Style.RESET_ALL}{Fore.GREEN} "
        f"to Kafka{Style.RESET_ALL}\n"
    )

    COMMENT_LIMIT -= 1
    if COMMENT_LIMIT <= 0:
        break

print(
    f"{Fore.YELLOW}Remaining requests: "
    f"{Style.RESET_ALL}{reddit.auth.limits['remaining']}{Fore.YELLOW} "
    f"out of {Style.RESET_ALL}{reddit.auth.limits['used']}{Fore.YELLOW} "
    f"used{Style.RESET_ALL}\n"
)

# Close the producer
producer.close()
