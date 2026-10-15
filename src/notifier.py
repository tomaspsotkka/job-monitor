import os
import requests
from dotenv import load_dotenv

load_dotenv()
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

def send_message(text: str) -> None:
    response = requests.post(WEBHOOK_URL, json={"content": text}, timeout = 10)
    response.raise_for_status()
    