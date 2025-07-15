# File: backend/utils/convert_excel_to_config.py
import pandas as pd
import json

def excel_to_config(excel_path, output_path="backend/scraper/company_config.json"):
    df = pd.read_excel(excel_path)

    config = {}
    for _, row in df.iterrows():
        company = row['Company Name'].strip()
        url = row['URL'].strip()
        keywords = [k.strip() for k in row['Keywords'].split(",")]

        config[company.lower()] = {
            "url": url,
            "keywords": keywords
        }

    with open(output_path, "w") as f:
        json.dump(config, f, indent=2)

    print(f"[✓] Config saved to {output_path}")

# Usage:
# excel_to_config("companies.xlsx")