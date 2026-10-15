from urllib.parse import urlencode
from src.models import Job
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"

def build_search_url() -> str:
    params = {
        "keywords": "data engineer",
        "location": "Denmark",
        "f_TPR": "r604800",
        "f_E": "1,2",
        "sortBy": "DD",
        "start": 0,
        "geoId": "104514075",
        
    }
    return f"{BASE_URL}?{urlencode(params)}"

HEADERS = {"User-Agent": "Mozilla/5.0"}

def fetch_page(url: str) -> str:
    response = requests.get(url, headers=HEADERS, timeout = 15)
    response.raise_for_status()
    return response.text

def parse_jobs(html: str) -> list[Job]:
    soup = BeautifulSoup(html, "html.parser")
    jobs = []
    
    job_cards = soup.find_all("li")
    
    for card in job_cards:
        id_tag = card.find("div", attrs={"data-entity-urn": True})
        if id_tag is None:
            continue
        job_id = id_tag["data-entity-urn"].split(":")[-1]
        
        title_tag = card.find("h3", class_="base-search-card__title")
        if title_tag is None:
            continue
        title = title_tag.get_text(strip=True)
        
        company_tag = card.find("h4", class_="base-search-card__subtitle")
        company = company_tag.get_text(strip=True) if company_tag else ""
        
        location_tag = card.find("span", class_="job-search-card__location")
        location = location_tag.get_text(strip=True) if location_tag else ""
        
        url_tag = card.find("a", class_="base-card__full-link")
        if url_tag is None:
            continue
        url = url_tag["href"].split("?")[0]
        
        posted_date_tag = card.find("time")
        posted_date = posted_date_tag["datetime"] if posted_date_tag else ""
        
        jobs.append(Job(id=job_id, 
                        title=title, 
                        company=company, 
                        location=location, 
                        url=url,
                        posted_date=posted_date))
    return jobs
        
    
