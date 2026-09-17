# Automation

## What runs here

| Job | Schedule | Purpose |
|-----|----------|---------|
| `sync_all` | 02:00 daily | Pull FDA + EMA + EDA, emit change_events |

## Adding a job

1. Define an async function in `scheduler.py`
2. Register with `scheduler.add_job(...)` using `CronTrigger.from_crontab()`
3. Rebuild: `docker-compose up -d --build scheduler`

## Monitoring

- `docker-compose logs -f scheduler`
- In production: send failures to Sentry / Slack webhook