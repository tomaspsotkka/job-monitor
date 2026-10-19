import os
import requests
import time

from src.models import Job
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
MAX_EMBEDS_PER_MESSAGE = 10
MAX_RETRIES = 3

#private helper functions
def _chunks(items: list, size: int) -> list[list]:
    return [items[i:i + size] for i in range(0, len(items), size)]
    
def _post(payload: dict) -> None:
    for attempt in range(MAX_RETRIES):
        response = requests.post(WEBHOOK_URL, json=payload, timeout=10)
        
        if response.status_code == 429:
                wait = response.json().get("retry_after", 1)
                print(f"Rate limited by Discord, waiting {wait}s (attempt {attempt + 1}/{MAX_RETRIES})")
                time.sleep(wait)
                continue
        
        response.raise_for_status()
        return
    
    return RuntimeError(f"Discord still rate limiting after {MAX_RETRIES} attempts")
    
def job_to_embed(job: Job) -> dict:
    embed = {
        "title": job.title,
        "url": job.url,
        "color": 0x008000,
        "fields": [
            {"name": "Company", "value": job.company or "Unknown", "inline": True},
            {"name": "Location", "value": job.location or "Unknown", "inline": True}
        ],
        "footer": {"text": f"Posted {job.posted_date or 'unknown date'}"}
    }
    
    if job.logo_url:
        embed["thumbnail"] = {"url": job.logo_url}
        
    return embed
    
# method for testing
def send_message(text: str) -> None:
    _post({"content": text})
    
def send_jobs(jobs: list[Job], search_name: str) -> None:
    if not jobs:
        return
    
    for index, chunk in enumerate(_chunks(jobs, MAX_EMBEDS_PER_MESSAGE)):
        embeds = [job_to_embed(job) for job in chunk]
        payload = {"embeds": embeds}
    
        if index == 0:
            payload["content"] = f"**{len(jobs)} new jobs** matching your {search_name} search. \nJob run: {datetime.now().strftime('%d-%m-%Y %H:%M')}"
        
        _post(payload)
        
        time.sleep(2)
        