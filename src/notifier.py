import os
import requests
from dotenv import load_dotenv
from src.models import Job

load_dotenv()
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

def send_message(text: str) -> None:
    response = requests.post(WEBHOOK_URL, json={"content": text}, timeout = 10)
    response.raise_for_status()
    
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
    
def send_jobs(jobs: list[Job], search_name: str) -> None:
    if not jobs:
        return
    
    embeds = []
    
    for job in jobs:
        embeds.append(job_to_embed(job))
        
    payload = {
        "content": f"**{len(jobs)} new jobs** matching your {search_name} search",
        "embeds": embeds
    }
    response = requests.post(WEBHOOK_URL, json=payload, timeout=10)
    response.raise_for_status()
    