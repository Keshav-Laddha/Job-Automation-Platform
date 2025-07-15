# # backend/scraper/job_scraper.py

# import json
# import time
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from bs4 import BeautifulSoup
# import undetected_chromedriver as uc

# def load_config():
#     with open("backend/scraper/company_config.json") as f:
#         return json.load(f)


# # def setup_driver():
# #     options = Options()
# #     options.headless = True
# #     options.add_argument("--no-sandbox")
# #     options.add_argument("--disable-dev-shm-usage")
# #     driver = webdriver.Chrome(options=options)
# #     return driver
# def setup_driver():
#     options = uc.ChromeOptions()
#     options.headless = True
#     driver = uc.Chrome(options=options)
#     return driver

# def scrape_company_jobs(company_name, company_info):
#     url = company_info["url"]
#     keywords = company_info["keywords"]
#     print(f"[INFO] Scraping {company_name} at {url}")
#     driver = setup_driver()

#     try:
#         driver.get(url)
#         time.sleep(5)  # Let page load (tune for each site)

#         soup = BeautifulSoup(driver.page_source, "html.parser")

#         job_listings = []
#         seen = set()  # to avoid duplicates

#         # Example: find all job entries by <a> or <div>
#         for link in soup.find_all(["a", "div"]):
#             text = link.get_text().strip().lower()
#             href = link.get("href")

#             for keyword in keywords:
#                 if keyword.lower() in text:
#                     job_data = (
#                         company_name,
#                         text,
#                         href if href and href.startswith("http") else url,
#                         keyword,
#                     )
#                     if job_data not in seen:
#                         seen.add(job_data)
#                         job_listings.append({
#                             "company": company_name,
#                             "title": text,
#                             "link": job_data[2],
#                             "matched_keyword": keyword,
#                         })
#                     break

#         return job_listings
#     finally:
#         driver.quit()
#         driver=None


# def run_all_scrapers():
#     config = load_config()
#     all_jobs = []
#     for company, info in config.items():
#         try:
#             jobs = scrape_company_jobs(company, info)
#             all_jobs.extend(jobs)
#         except Exception as e:
#             print(f"[ERROR] Failed to scrape {company}: {e}")
#     return all_jobs


# # CLI for testing
# if __name__ == "__main__":
#     results = run_all_scrapers()
#     print(f"\n[✓] Found {len(results)} matching jobs:\n")
#     for job in results:
#         print(f"- {job['company'].title()} | {job['title']} | {job['link']}")


# File: backend/scraper/job_scraper.py

import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from urllib.parse import urljoin

from backend.database.models import insert_job  # NEW IMPORT
from backend.email.mailer import send_job_email

def load_config():
    with open("backend/scraper/company_config.json") as f:
        return json.load(f)

def setup_driver():
    options = uc.ChromeOptions()
    options.headless = True
    driver = uc.Chrome(options=options)
    return driver

def scrape_company_jobs(company_name, company_info):
    url = company_info["url"]
    keywords = company_info["keywords"]
    print(f"[INFO] Scraping {company_name} at {url}")
    driver = setup_driver()

    try:
        driver.get(url)
        time.sleep(5)  # Wait for page load

        soup = BeautifulSoup(driver.page_source, "html.parser")

        job_listings = []
        seen_links = set()

        # Scan for anchor tags with links
        for tag in soup.find_all("a", href=True):
            raw_title = tag.get_text(strip=True)
            href = tag["href"].strip()

            if not raw_title or not href:
                continue

            for keyword in keywords:
                if keyword.lower() in raw_title.lower():
                    full_link = urljoin(url, href)  # Fix relative URLs

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

                    # Save to DB
                    insert_job(
                        company=job_dict["company"],
                        title=job_dict["title"],
                        link=job_dict["link"],
                        matched_keyword=job_dict["matched_keyword"]
                    )
                    break

        return job_listings
    finally:
        try:
            driver.quit()
        except:
            pass


def run_all_scrapers():
    config = load_config()
    all_jobs = []
    for company, info in config.items():
        try:
            jobs = scrape_company_jobs(company, info)
            all_jobs.extend(jobs)
        except Exception as e:
            print(f"[ERROR] Failed to scrape {company}: {e}")
    return all_jobs


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