# Job Monitor

A Python bot that checks job sites for new postings that match my searches, and posts them to my Discord server. Each search gets its own channel, so new jobs show up as clean cards with the title, company, location, posted date and company logo.
 
Right now it supports LinkedIn. More job sites are planned.
 
## How it works
 
```
config.yaml → fetch jobs → parse → filter → post to Discord
```
 
1. **Searches** are defined in `config.yaml` (keywords, location, experience level, job type, workplace)
2. **Fetch:** each search is turned into a LinkedIn guest search URL and downloaded with `requests`
3. **Parse:** the HTML job cards are turned into `Job` objects with BeautifulSoup
4. **Filter:** titles with unwanted words (like "senior" or "lead") and blocked companies are dropped
5. **Post:** jobs are sent to the search's Discord channel through a webhook, max 10 cards per message, with retries if Discord rate limits