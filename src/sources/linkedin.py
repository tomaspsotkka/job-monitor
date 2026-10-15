from urllib.parse import urlencode
import requests

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


def fetch_linkedin(url: str) -> str:
    response = requests.get(url, headers=HEADERS, timeout = 15)
    response.raise_for_status()
    return response.text
