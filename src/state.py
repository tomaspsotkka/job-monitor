import json
import os
from datetime import date, timedelta
from pathlib import Path
from src.models import Job
from dotenv import load_dotenv

load_dotenv()

STATE_FILE = Path(os.getenv("STATE_FILE", "seen_jobs.json"))

def load_state() -> dict:
    if not STATE_FILE.exists():
        return {}
    return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    
    
def save_state(state: dict) -> None:
    text = json.dumps(state, indent=2)
    STATE_FILE.write_text(text)
    

def filter_new(jobs: list[Job], state: dict, search_name: str) -> list[Job]:
    seen = state.get(search_name, {})
    new_jobs = []
    for job in jobs:
        if job.id not in seen:
            new_jobs.append(job)
    return new_jobs

def mark_sent(jobs: list[Job], state: dict, search_name: str) -> None:
    seen = state.setdefault(search_name, {})
    today = date.today().isoformat()
    for job in jobs:
        seen[job.id] = today
        
def prune(state: dict, max_age_days: int = 30) -> None:
    cutoff = (date.today() - timedelta(max_age_days)).isoformat()
    for search_name, seen in state.items():
        recent = {}
        for job_id, day in seen.items():
            if day >= cutoff:
                recent[job_id] = day
            state[search_name] = recent #writing the jobs that are still recdnt
            
            