from src.sources.linkedin import build_search_url, fetch_page, parse_jobs
from pathlib import Path
from src.notifier import send_jobs
from src.config import load_config

CACHE = Path("page_raw.html")

if __name__ == "__main__":
    config = load_config()
    print(config)
    
    for search in config["searches"]:
        print(build_search_url(search))
    
    if CACHE.exists():
        html = CACHE.read_text(encoding="utf-8")
        print("Loaded HTML from cache")
    else:
        html = fetch_page(build_search_url())
        CACHE.write_text(html, encoding="utf-8")
        print("Fetched HTML from LinkedIn and saved to cache")
    
    jobs = parse_jobs(html)
    print(f"Found {len(jobs)} jobs")
    for job in jobs:
        print(job)
        
    send_jobs(jobs[:10])
    