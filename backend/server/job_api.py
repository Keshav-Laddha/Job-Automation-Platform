# File: backend/server/job_api.py

from flask import Flask, jsonify, Blueprint, request
from backend.scraper.job_scraper import run_all_scrapers
from backend.email.mailer import send_job_email
from flask_cors import CORS

job_api_bp = Blueprint('job_api', __name__)

@job_api_bp.route("/jobs")
def get_jobs():
    jobs = run_all_scrapers()
    return jsonify(jobs)

@job_api_bp.route("/scrape-and-email", methods=["POST"])
def scrape_and_email():
    try:
        jobs = run_all_scrapers()
        send_job_email(jobs)
        return jsonify({"success": True, "message": "Jobs scraped and emailed successfully!"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@job_api_bp.route("/delete-company-data", methods=["POST"])
def delete_company_data():
    data = request.json
    company = data.get("company")
    if not company:
        return jsonify({"success": False, "message": "Missing company name."}), 400
    # Delete from jobs database
    from backend.database.db import get_connection
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM jobs WHERE LOWER(company) = ?", (company.lower(),))
    conn.commit()
    conn.close()
    # Delete from request log
    import os, json
    log_path = "backend/scraper/data/request_log.json"
    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            logs = json.load(f)
        logs = [entry for entry in logs if entry.get("company", "").lower() != company.lower()]
        with open(log_path, "w") as f:
            json.dump(logs, f, indent=2)
    # Log the deletion request
    from backend.scraper.job_scraper import log_request
    import time
    log_request({"type": "delete_request", "company": company, "timestamp": time.time()})
    return jsonify({"success": True, "message": f"All data for company '{company}' has been deleted."})

if __name__ == "__main__":
    job_api_bp.run(debug=True, port=5001)

# from flask import Blueprint, jsonify
# from backend.scraper.job_scraper import run_all_scrapers

# job_api = Blueprint("jobs", __name__)

# @job_api.route("/jobs")
# def get_jobs():
#     jobs = run_all_scrapers()
#     return jsonify(jobs)
