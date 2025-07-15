# File: backend/scraper/generate_company_config.py

import pandas as pd
import json
import os

EXCEL_PATH = os.path.join(os.path.dirname(__file__), "data", "Imp1.xlsx")
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "company_config.json")

def excel_to_company_config():
    df = pd.read_excel(EXCEL_PATH)

    config = {}
    for _, row in df.iterrows():
        company = str(row['company']).strip().lower()
        url = str(row['url']).strip()
        keywords = str(row['keywords']).split(',') if 'keywords' in row and pd.notna(row['keywords']) else []
        location_str = str(row.get('location', '')).strip() if pd.notna(row.get('location')) else "Unknown"
        locations = [loc.strip() for loc in location_str.split(',') if loc.strip()]

        if url:
            config[company] = {
                "url": url,
                "keywords": [k.strip() for k in keywords if k.strip()],
                "location": locations
            }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(config, f, indent=2)

    print(f"[✓] company_config.json created at {OUTPUT_PATH}")

if __name__ == "__main__":
    excel_to_company_config()