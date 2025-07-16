# # backend/scraper/job_scraper.py

import json
import time
import random
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from urllib.parse import urljoin, urlparse
import os
from datetime import datetime, timedelta

from backend.database.models import insert_job
from backend.email.mailer import send_job_email

# --- Configurable constants ---
DAILY_COMPANY_LIMIT = 100
REQUEST_LOG_PATH = "backend/scraper/data/request_log.json"
SCRAPE_LOG_PATH = "backend/scraper/data/scrape_log.json"
SCRAPE_PAUSE_PATH = "backend/scraper/data/scrape_pause.json"
CAPTCHA_KEYWORDS = ["captcha", "are you human", "verify you are", "robot check", "recaptcha"]
DEFAULT_COMPANY_DELAY = (8, 15)  # seconds between companies
DEFAULT_JOB_DELAY = (3, 5)       # seconds between job listings/pages
PAUSE_ON_ERROR_HOURS = 6
USER_AGENT = "AI-Job-Assistant-Bot/1.0 (Contact: youremail@example.com)"

# --- Utility functions for logging and state ---
def log_request(entry):
    try:
        if os.path.exists(REQUEST_LOG_PATH):
            with open(REQUEST_LOG_PATH, "r") as f:
                logs = json.load(f)
        else:
            logs = []
        logs.append(entry)
        with open(REQUEST_LOG_PATH, "w") as f:
            json.dump(logs, f, indent=2)
    except Exception as e:
        print(f"[LOGGING ERROR] {e}")

def get_scrape_log():
    if os.path.exists(SCRAPE_LOG_PATH):
        with open(SCRAPE_LOG_PATH, "r") as f:
            return json.load(f)
    return []

def update_scrape_log(company, timestamp):
    log = get_scrape_log()
    log.append({"company": company, "timestamp": timestamp})
    # Keep only last 7 days for safety
    cutoff = time.time() - 7*24*3600
    log = [entry for entry in log if entry["timestamp"] >= cutoff]
    with open(SCRAPE_LOG_PATH, "w") as f:
        json.dump(log, f, indent=2)

def get_pause_until():
    if os.path.exists(SCRAPE_PAUSE_PATH):
        with open(SCRAPE_PAUSE_PATH, "r") as f:
            return float(f.read().strip())
    return 0

def set_pause_until(ts):
    with open(SCRAPE_PAUSE_PATH, "w") as f:
        f.write(str(ts))

def is_captcha(page_source):
    text = page_source.lower()
    return any(kw in text for kw in CAPTCHA_KEYWORDS)

# --- robots.txt parsing ---
def parse_robots_txt(url):
    parsed = urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    crawl_delay = None
    allowed = True
    try:
        resp = requests.get(robots_url, timeout=5, headers={"User-Agent": USER_AGENT})
        log_request({"type": "robots.txt", "url": robots_url, "timestamp": time.time(), "status": resp.status_code})
        if resp.status_code != 200:
            return allowed, crawl_delay
        lines = resp.text.splitlines()
        user_agent = None
        for line in lines:
            line = line.strip()
            if line.lower().startswith("user-agent:"):
                user_agent = line.split(":", 1)[1].strip()
            if user_agent in ("*", USER_AGENT):
                if line.lower().startswith("disallow:"):
                    path = line.split(":", 1)[1].strip()
                    if path == "/":
                        allowed = False
                if line.lower().startswith("crawl-delay:"):
                    try:
                        crawl_delay = float(line.split(":", 1)[1].strip())
                    except Exception:
                        pass
        return allowed, crawl_delay
    except Exception as e:
        log_request({"type": "robots.txt", "url": robots_url, "timestamp": time.time(), "status": "error", "error": str(e)})
        return allowed, crawl_delay

def setup_driver():
    options = uc.ChromeOptions()
    options.headless = True
    options.add_argument(f"--user-agent={USER_AGENT}")
    driver = uc.Chrome(options=options)
    return driver

def scrape_company_jobs(company_name, company_info, job_delay=DEFAULT_JOB_DELAY):
    url = company_info["url"]
    keywords = company_info["keywords"]
    print(f"[INFO] Scraping {company_name} at {url}")
    allowed, crawl_delay = parse_robots_txt(url)
    if not allowed:
        print(f"[ETHICS] Skipping {company_name}: robots.txt disallows scraping.")
        log_request({"type": "skip", "company": company_name, "url": url, "timestamp": time.time(), "reason": "robots.txt disallow"})
        return []
    driver = setup_driver()
    try:
        # Exponential backoff for page load
        for attempt in range(4):
            try:
                driver.get(url)
                time.sleep(5)
                break
            except Exception as e:
                wait = 2 ** attempt
                print(f"[WARN] Error loading {url}, retrying in {wait}s: {e}")
                time.sleep(wait)
        page_source = driver.page_source
        if is_captcha(page_source):
            print(f"[CAPTCHA] Detected on {company_name}, skipping.")
            log_request({"type": "captcha", "company": company_name, "url": url, "timestamp": time.time()})
            return []
        soup = BeautifulSoup(page_source, "html.parser")
        job_listings = []
        seen_links = set()
        for tag in soup.find_all("a", href=True):
            raw_title = tag.get_text(strip=True)
            href = tag["href"].strip()
            if not raw_title or not href:
                continue
            for keyword in keywords:
                if keyword.lower() in raw_title.lower():
                    full_link = urljoin(url, href)
                    if full_link in seen_links:
                        continue
                    seen_links.add(full_link)
                    title = raw_title.title()
                    job_dict = {
                        "company": company_name,
                        "title": title,
                        "link": full_link,
                        "matched_keyword": keyword,
                        "location": company_info.get("location", "Unknown")
                    }
                    job_listings.append(job_dict)
                    insert_job(
                        company=job_dict["company"],
                        title=job_dict["title"],
                        link=job_dict["link"],
                        matched_keyword=job_dict["matched_keyword"]
                    )
                    # Log each job listing request
                    log_request({
                        "type": "job_listing",
                        "company": company_name,
                        "url": full_link,
                        "timestamp": time.time(),
                        "status": "success"
                    })
                    # Delay between job listings/pages
                    delay = random.uniform(*job_delay)
                    print(f"[ETHICS] Waiting {delay:.1f}s before next job listing...")
                    time.sleep(delay)
                    break
        return job_listings
    finally:
        try:
            driver.quit()
        except:
            pass

def run_all_scrapers():
    # --- Check for pause ---
    now = time.time()
    pause_until = get_pause_until()
    if now < pause_until:
        mins = int((pause_until - now) // 60) + 1
        print(f"[ETHICS] Scraping paused for {mins} more minutes due to previous errors.")
        return []
    # --- Enforce daily company cap ---
    log = get_scrape_log()
    last_24h = [entry for entry in log if entry["timestamp"] >= now - 24*3600]
    if len(last_24h) >= DAILY_COMPANY_LIMIT:
        print(f"[ETHICS] Daily company scrape cap ({DAILY_COMPANY_LIMIT}) reached. Try again later.")
        return []
    config = load_config()
    all_jobs = []
    companies = list(config.items())
    companies_scraped = 0
    for idx, (company, info) in enumerate(companies):
        # --- Check daily cap again in loop ---
        log = get_scrape_log()
        last_24h = [entry for entry in log if entry["timestamp"] >= time.time() - 24*3600]
        if len(last_24h) >= DAILY_COMPANY_LIMIT:
            print(f"[ETHICS] Daily company scrape cap reached during run.")
            break
        try:
            jobs = scrape_company_jobs(company, info)
            all_jobs.extend(jobs)
            update_scrape_log(company, time.time())
            companies_scraped += 1
        except Exception as e:
            print(f"[ERROR] Failed to scrape {company}: {e}")
            log_request({"type": "error", "company": company, "url": info.get("url"), "timestamp": time.time(), "error": str(e)})
            # If HTTP error code 429/403/503, pause scraping for 6 hours
            if any(code in str(e) for code in ["429", "403", "503"]):
                pause_until = time.time() + PAUSE_ON_ERROR_HOURS * 3600
                set_pause_until(pause_until)
                print(f"[ETHICS] Pausing all scraping for {PAUSE_ON_ERROR_HOURS} hours due to error: {e}")
                break
        # --- Delay between companies (respect crawl-delay if present) ---
        if idx < len(companies) - 1:
            delay = None
            # Use crawl-delay if present, else default
            allowed, crawl_delay = parse_robots_txt(info["url"])
            if crawl_delay:
                delay = crawl_delay
            else:
                delay = random.randint(*DEFAULT_COMPANY_DELAY)
            print(f"[ETHICS] Waiting {delay:.1f}s before next company...")
            time.sleep(delay)
    return all_jobs

def monitor_logs_for_issues():
    """Scan the request log for errors or complaints and print a summary."""
    if not os.path.exists(REQUEST_LOG_PATH):
        print("[LOG MONITOR] No request log found.")
        return
    with open(REQUEST_LOG_PATH, "r") as f:
        logs = json.load(f)
    issues = [entry for entry in logs if entry.get("type") in ("error", "complaint") or any(str(code) in str(entry.get("error", "")) for code in [429, 403, 503])]
    if not issues:
        print("[LOG MONITOR] No issues or complaints found in logs.")
        return
    print(f"[LOG MONITOR] Found {len(issues)} issues/complaints:")
    for entry in issues:
        print(f"- {entry}")

# CLI for testing
if __name__ == "__main__":
    from backend.database.db import init_db
    init_db()  # ensure DB is initialized
    results = run_all_scrapers()
    print(f"\n[✓] Found {len(results)} matching jobs:\n")
    for job in results:
        print(f"- {job['company'].title()} | {job['title']} | {job['link']}")
    if results:
        send_job_email(results)