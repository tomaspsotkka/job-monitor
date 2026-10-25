import os
import time
from pathlib import Path

from dotenv import load_dotenv

from src.config import load_config
from src.filters import apply_filters
from src.notifier import send_jobs
from src.sources.linkedin import build_search_url, fetch_page, parse_jobs
from src.state import load_state, save_state, mark_sent, filter_new, prune

load_dotenv()

CACHE_DIR = Path("cache")

def get_html(search: dict) -> str:
    cache_file = CACHE_DIR / f"{search['name']}.html"
    
    if cache_file.exists():
        print(f"[{search['name']}] loaded from cache")
        return cache_file.read_text(encoding="utf-8")
    
    html = fetch_page(build_search_url(search))
    cache_file.write_text(html, encoding="utf-8")
    print(f"[{search['name']}] fetched from LinkedIn")
    time.sleep(2)
    return html
    

if __name__ == "__main__":
    config = load_config()
    all_jobs = []
    state = load_state()
    prune(state)
    
    for search in config["searches"]:
        webhook_url = os.getenv(search["webhook"])
        if not webhook_url:
            print(f"[{search['name']}] no webhook found for {search['webhook']}, skipping")
            continue
        
        print(build_search_url(search))
        html = get_html(search)
        jobs = parse_jobs(html)
        relevant = apply_filters(jobs, config["filters"])
        new_jobs = filter_new(relevant, state, search["name"])
        print(f"\n[{search['name']}] {len(jobs)} found, {len(relevant)} after filters, {len(new_jobs)} new")
    
        send_jobs(new_jobs, search["name"], webhook_url)
        mark_sent(new_jobs, state, search["name"])
        save_state(state)
        
        all_jobs.extend(new_jobs) 
        
    print(f"\nTotal: {len(all_jobs)} new jobs")
    