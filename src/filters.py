from src.models import Job

def is_relevant(job: Job, filters: dict) -> bool:
    title = job.title.lower()
    company = job.company.lower()
    
    for word in filters.get("title_exclude", []):
        if word.lower() in title:
            return False
        
    for word in filters.get("company_exclude", []):
        if word.lower() in company:
            return False
        
    include = filters.get("title_include", [])
    if include and not any(word.lower() in title for word in include):
        return False
    
    return True

def apply_filters(jobs: list[Job], filters: dict) -> list[Job]:
    filtered_jobs = []
    
    for job in jobs:
        if is_relevant(job, filters):
            filtered_jobs.append(job)
    
    return filtered_jobs
    