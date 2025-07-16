from apscheduler.schedulers.background import BlockingScheduler
from backend.scraper.job_scraper import run_all_scrapers
from datetime import datetime

def scheduled_scrape():
    print(f"[INFO] Running scheduled job scraping at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    run_all_scrapers()

sched = BlockingScheduler()
sched.add_job(scheduled_scrape, 'cron', hour=11, minute=0)
sched.add_job(scheduled_scrape, 'cron', hour=16, minute=0)

if __name__ == "__main__":
    sched.start() 