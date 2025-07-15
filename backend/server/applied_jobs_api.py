from flask import Flask, jsonify, request, redirect, Blueprint, current_app
from backend.database.db import get_connection
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from flask import send_from_directory
from urllib.parse import quote_plus

applied_jobs_bp = Blueprint('applied_jobs', __name__)

ALLOWED_EXTENSIONS = {"pdf", "docx"}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@applied_jobs_bp.route("/applied/<int:job_id>/upload_resume", methods=["POST"])
def upload_resume(job_id):
    if "resume" not in request.files:
        return jsonify(error="No file uploaded"), 400

    file = request.files["resume"]
    if file.filename == "":
        return jsonify(error="Empty filename"), 400

    if not allowed_file(file.filename):
        return jsonify(error="Only PDF/DOCX allowed"), 400

    filename = secure_filename(f"job_{job_id}_{file.filename}")
    save_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    file.save(save_path)

    # 🔁 Save full path or just filename (frontend will build URL)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE applied_jobs SET resume_path = ? WHERE id = ?", (filename, job_id))
    conn.commit()
    conn.close()

    return jsonify(success=True, filename=filename)

@applied_jobs_bp.route("/applied/resume/<path:filename>")
def serve_resume(filename):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)

@applied_jobs_bp.route("/applied")
def get_applied():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM applied_jobs ORDER BY applied_at DESC")
    jobs = [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]
    conn.close()
    return jsonify(jobs)

@applied_jobs_bp.route("/applied/<int:job_id>", methods=["PATCH"])
def update_applied(job_id):
    updates = request.json
    fields = ', '.join([f"{key} = ?" for key in updates])
    values = list(updates.values()) + [job_id]

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"UPDATE applied_jobs SET {fields} WHERE id = ?", values)
    conn.commit()
    conn.close()
    return jsonify(success=True)

@applied_jobs_bp.route("/applied/<int:job_id>", methods=["DELETE"])
def delete_applied(job_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM applied_jobs WHERE id = ?", (job_id,))
    conn.commit()
    conn.close()
    return jsonify(success=True)

# 🌟 NEW: One-click job tracker addition from email or anywhere
@applied_jobs_bp.route("/applied/new")
def quick_add_applied():
    company = request.args.get("company")
    title = request.args.get("title")
    link = request.args.get("link")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO applied_jobs (company, title, link, status)
        VALUES (?, ?, ?, 'Applied')
    """, (company, title, link))
    conn.commit()
    conn.close()

    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
    return redirect(f"{frontend_url}/optimize?job_title={quote_plus(title)}&job_description={quote_plus(link)}")

@applied_jobs_bp.route("/applied/uploads/<path:filename>")
def serve_uploaded_file(filename):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)

# from flask import Blueprint, request, jsonify, redirect, send_from_directory
# from backend.database.db import get_connection
# from werkzeug.utils import secure_filename
# from urllib.parse import quote_plus
# import os
# from dotenv import load_dotenv

# load_dotenv()

# applied_api = Blueprint("applied", __name__, url_prefix="/applied")
# UPLOAD_FOLDER = "backend/uploads"
# ALLOWED_EXTENSIONS = {"pdf", "docx"}

# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @applied_api.route("/<int:job_id>/upload_resume", methods=["POST"])
# def upload_resume(job_id):
#     if "resume" not in request.files:
#         return jsonify(error="No file uploaded"), 400
#     file = request.files["resume"]
#     if file.filename == "":
#         return jsonify(error="Empty filename"), 400
#     if not allowed_file(file.filename):
#         return jsonify(error="Only PDF/DOCX allowed"), 400

#     filename = secure_filename(f"job_{job_id}_{file.filename}")
#     save_path = os.path.join(UPLOAD_FOLDER, filename)
#     file.save(save_path)

#     conn = get_connection()
#     cursor = conn.cursor()
#     cursor.execute("UPDATE applied_jobs SET resume_path = ? WHERE id = ?", (filename, job_id))
#     conn.commit()
#     conn.close()

#     return jsonify(success=True, filename=filename)

# @applied_api.route("/resume/<path:filename>")
# def serve_resume(filename):
#     return send_from_directory(UPLOAD_FOLDER, filename)

# @applied_api.route("/uploads/<path:filename>")
# def serve_uploaded_file(filename):
#     return send_from_directory(UPLOAD_FOLDER, filename)

# @applied_api.route("/")
# def get_applied():
#     conn = get_connection()
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM applied_jobs ORDER BY applied_at DESC")
#     jobs = [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]
#     conn.close()
#     return jsonify(jobs)

# @applied_api.route("/<int:job_id>", methods=["PATCH"])
# def update_applied(job_id):
#     updates = request.json
#     fields = ', '.join([f"{key} = ?" for key in updates])
#     values = list(updates.values()) + [job_id]
#     conn = get_connection()
#     cursor = conn.cursor()
#     cursor.execute(f"UPDATE applied_jobs SET {fields} WHERE id = ?", values)
#     conn.commit()
#     conn.close()
#     return jsonify(success=True)

# @applied_api.route("/<int:job_id>", methods=["DELETE"])
# def delete_applied(job_id):
#     conn = get_connection()
#     cursor = conn.cursor()
#     cursor.execute("DELETE FROM applied_jobs WHERE id = ?", (job_id,))
#     conn.commit()
#     conn.close()
#     return jsonify(success=True)

# @applied_api.route("/new")
# def quick_add_applied():
#     company = request.args.get("company")
#     title = request.args.get("title")
#     link = request.args.get("link")
#     conn = get_connection()
#     cursor = conn.cursor()
#     cursor.execute("""
#         INSERT INTO applied_jobs (company, title, link, status)
#         VALUES (?, ?, ?, 'Applied')
#     """, (company, title, link))
#     conn.commit()
#     conn.close()

#     frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
#     return redirect(f"{frontend_url}/optimize?job_title={quote_plus(title)}&job_description={quote_plus(link)}")