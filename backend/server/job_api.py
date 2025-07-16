# File: backend/server/job_api.py

from flask import Flask, jsonify, Blueprint
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

if __name__ == "__main__":
    job_api_bp.run(debug=True, port=5001)

# from flask import Blueprint, jsonify
# from backend.scraper.job_scraper import run_all_scrapers

# job_api = Blueprint("jobs", __name__)

# @job_api.route("/jobs")
# def get_jobs():
#     jobs = run_all_scrapers()
#     return jsonify(jobs)
