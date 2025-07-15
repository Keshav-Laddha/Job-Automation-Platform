import pandas as pd
import json
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

INPUT_EXCEL = "data/Imp1.xlsx"  # <- put your Excel here
OUTPUT_JSON = "backend/scraper/company_config.json"
DEFAULT_KEYWORDS = ["intern", "software", "developer", "analyst"]

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9",
}

def bing_search(company_name):
    query = f"{company_name} careers site:.com"
    search_url = f"https://www.bing.com/search?q={quote(query)}"
    response = requests.get(search_url, headers=HEADERS)

    if response.status_code != 200:
        print(f"[ERROR] Failed search for {company_name}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    for a in soup.find_all("a", href=True):
        href = a["href"]
        text = a.get_text().lower()

        if "career" in href or "jobs" in href or "careers" in text:
            return href

    return None

def generate_config_from_excel():
    df = pd.read_excel(INPUT_EXCEL, header=None, names=["company"])
    companies = df["company"].dropna().unique()

    config = {}

    for company in companies:
        name = str(company).strip()
        if not name:
            continue

        print(f"🔍 Searching: {name}")
        url = bing_search(name)
        time.sleep(2)  # be gentle to avoid rate limiting

        if url:
            config[name] = {
                "url": url,
                "keywords": DEFAULT_KEYWORDS,
                "location": "India"
            }
        else:
            print(f"[WARNING] No URL found for {name}")

    # Save config to JSON
    with open(OUTPUT_JSON, "w") as f:
        json.dump(config, f, indent=2)

    print(f"\n✅ Config saved to: {OUTPUT_JSON}")
    print(f"Total companies processed: {len(config)}")

if __name__ == "__main__":
    generate_config_from_excel()