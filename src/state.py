import json
from datetime import date
from pathlib import Path
from src.models import Job

STATE_FILE = Path("seen_jobs.json")

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