from dataclasses import dataclass

@dataclass
class Job:
    id: str
    title: str
    company: str
    location: str
    url: str
    posted_date: str