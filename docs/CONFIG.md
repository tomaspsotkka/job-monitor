# Configuration

Everything the bot searches for and filters on lives in `config.yaml` in the project root. Changing what you get in Discord never needs a code change, only an edit to this file.

The file has two sections:

```yaml
searches:   # what to look for, one entry per search
  - ...

filters:    # rules that drop jobs you don't want, applied to every search
  ...
```

## searches

A list of searches. Each one is fetched separately and posted to its own Discord channel.

| Field | Required | Type | What it does |
| --- | --- | --- | --- |
| `name` | yes | text | Unique name for the search. Used in logs, in the Discord message header and as the cache file name (`cache/<name>.html`). Use lowercase with dashes, like `data-engineer-dk` |
| `source` | yes | text | Which job site to search. Only `linkedin` for now |
| `webhook` | yes | text | **Name** of the env var that holds the Discord webhook URL for this search's channel. Never put the URL itself here |
| `keywords` | yes | text | What you'd type in the LinkedIn search box, like `data engineer` |
| `location` | yes | text | Location as text, like `Denmark` |
| `geo_id` | yes | text | LinkedIn's internal ID for the location. More precise than `location`. Always in quotes |
| `time_posted` | yes | text | How recent the jobs must be (see values below) |
| `experience` | yes | list | Experience levels to include (see values below) |
| `job_type` | no | list | Job types to include. Leave it out to get all types |
| `workplace` | no | list | On-site, remote or hybrid. Leave it out to get all |

### time_posted

The format is `r` followed by a number of seconds.

| Value | Meaning |
| --- | --- |
| `r86400` | last 24 hours (best for a daily run) |
| `r604800` | last 7 days |
| `r2592000` | last 30 days |
| `r3600` | last hour (any number of seconds works) |

### experience

| Value | Level |
| --- | --- |
| `1` | Internship |
| `2` | Entry level |
| `3` | Associate |
| `4` | Mid-Senior level |
| `5` | Director |
| `6` | Executive |

Companies pick the level themselves and often get it wrong, so expect some senior roles even with `[1, 2]`. Use `title_exclude` to catch those.

### job_type

| Value | Type |
| --- | --- |
| `F` | Full-time |
| `P` | Part-time |
| `C` | Contract |
| `T` | Temporary |
| `I` | Internship |
| `V` | Volunteer |
| `O` | Other |

### workplace

| Value | Type |
| --- | --- |
| `1` | On-site |
| `2` | Remote |
| `3` | Hybrid |

### Finding a geo_id

1. Go to linkedin.com/jobs and search for any job in the location you want
2. Look at the URL in your browser, it contains `geoId=` followed by a number
3. Copy that number into `geo_id`, in quotes

Known IDs:

| Location | geo_id |
| --- | --- |
| Denmark | `"104514075"` |

## filters

Applied to every search, after the jobs are fetched. All matching ignores upper and lower case.

| Field | Type | What it does |
| --- | --- | --- |
| `title_exclude` | list | Drop a job if its title contains **any** of these words |
| `title_include` | list | If not empty, keep a job only if its title contains **at least one** of these words. Empty list = keep everything |
| `company_exclude` | list | Drop a job if the company name contains any of these words |

Matching checks if the word appears **anywhere** in the text, even inside other words. So `lead` also matches "Leading", and `intern` would match "International". Keep that in mind if a job disappears and you don't know why.

## Environment variables

Webhook URLs are secrets, so they live in a `.env` file in the project root (gitignored), and in GitHub Secrets when running in GitHub Actions. Each search's `webhook` field points to one of these by name.

```
DISCORD_WEBHOOK_BOT_ALERTS=https://discord.com/api/webhooks/...                         # alerts channel
DISCORD_WEBHOOK_LINKEDIN_DATA_ENGINEER=https://discord.com/api/webhooks/...
DISCORD_WEBHOOK_LINKEDIN_ANALYTICS_ENGINEER=https://discord.com/api/webhooks/...
```

If a search's `webhook` name isn't found, that search is skipped with a warning, and the other searches still run.

## Full example

```yaml
searches:
  - name: data-engineer-dk
    source: linkedin
    webhook: DISCORD_WEBHOOK_LINKEDIN_DATA_ENGINEER
    keywords: data engineer
    location: Denmark
    geo_id: "104514075"
    time_posted: r86400
    experience: [1, 2]
    job_type: [F, I]
    workplace: [2, 3]

  - name: analytics-engineer-dk
    source: linkedin
    webhook: DISCORD_WEBHOOK_LINKEDIN_ANALYTICS_ENGINEER
    keywords: analytics engineer
    location: Denmark
    geo_id: "104514075"
    time_posted: r86400
    experience: [1, 2]

filters:
  title_exclude: [senior, lead, principal, manager, head of, architect]
  title_include: []
  company_exclude: []
```

## YAML tips

- Indentation matters, use spaces, never tabs
- Each search starts with `- ` at the same indentation level
- Put numbers that are really IDs in quotes (like `geo_id`), so they stay text
- If the bot crashes with `yaml.scanner.ScannerError`, the error message shows the line number of the problem