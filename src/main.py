from src.sources.linkedin import build_search_url, fetch_page, parse_jobs
from pathlib import Path
from src.notifier import send_jobs
from src.config import load_config
from src.filters import apply_filters
import time

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
    
    for search in config["searches"]:
        print(build_search_url(search))
        html = get_html(search)
        jobs = parse_jobs(html)
        relevant = apply_filters(jobs, config["filters"])
        print(f"\n[{search['name']}] {len(jobs)} found, {len(relevant)} after filters")
    
        all_jobs.extend(relevant)
        send_jobs(relevant[:10], search["name"])  
        
    print(f"\nTotal: {len(all_jobs)} jobs")
    