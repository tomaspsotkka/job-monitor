from src.notifier import send_message
from src.sources.linkedin import build_search_url, fetch_linkedin

if __name__ == "__main__":
    #send_message("Hello from Job Bot!")
    url = build_search_url()
    html = fetch_linkedin(url)
    
    with open("page.html", "w", encoding="utf-8") as f:
        f.write(html)
        
    print(f"Saved {len(html)} characters to page.html")