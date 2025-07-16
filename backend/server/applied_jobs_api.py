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
    # Accept all possible fields from query params
    company = request.args.get("company")
    title = request.args.get("title")
    link = request.args.get("link")
    status = request.args.get("status", "Applied")
    hr_contact = request.args.get("hr_contact", "")
    follow_up_date = request.args.get("follow_up_date", "")
    reminder = int(request.args.get("reminder", 0))
    applied_at = request.args.get("applied_at", "")
    deadline = request.args.get("deadline", "")
    resume_path = request.args.get("resume_path", "")
    notes = request.args.get("notes", "")
    ctc = request.args.get("ctc", "")

    print("[DEBUG] /applied/new params:", {
        "company": company, "title": title, "link": link, "status": status, "hr_contact": hr_contact,
        "follow_up_date": follow_up_date, "reminder": reminder, "applied_at": applied_at, "deadline": deadline,
        "resume_path": resume_path, "notes": notes, "ctc": ctc
    })

    # Check required fields
    if not company or not title or not link:
        print("[ERROR] Missing required fields for applied job.")
        return "Missing required fields (company, title, link)", 400

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO applied_jobs (company, title, link, status, hr_contact, follow_up_date, reminder, applied_at, deadline, resume_path, notes, ctc)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (company, title, link, status, hr_contact, follow_up_date, reminder, applied_at, deadline, resume_path, notes, ctc))
        conn.commit()
        print("[DEBUG] Inserted applied job for:", company, title)
    except Exception as e:
        print("[ERROR] Failed to insert applied job:", e)
        return f"Database error: {e}", 500
    finally:
        conn.close()

    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
    return redirect(f"{frontend_url}/applied")

@applied_jobs_bp.route("/applied/uploads/<path:filename>")
def serve_uploaded_file(filename):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)

# --- Interview Questions Endpoints ---
@applied_jobs_bp.route("/interview_questions", methods=["GET"])
def get_interview_questions():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, question, company, ctc_offered, asked_at FROM interview_questions ORDER BY asked_at DESC")
    rows = cursor.fetchall()
    conn.close()

    # Group by question (case-insensitive, trimmed)
    questions_dict = {}
    for row in rows:
        q_text = row[1].strip().lower()
        if q_text not in questions_dict:
            questions_dict[q_text] = {
                "id": row[0],
                "question": row[1].strip(),
                "description": row[1].strip(),  # For now, use question as description
                "companies": [row[2]],
                "ctc_offered": [row[3]] if row[3] else [],
                "asked_at": [row[4]]
            }
        else:
            if row[2] not in questions_dict[q_text]["companies"]:
                questions_dict[q_text]["companies"].append(row[2])
            if row[3] and row[3] not in questions_dict[q_text]["ctc_offered"]:
                questions_dict[q_text]["ctc_offered"].append(row[3])
            questions_dict[q_text]["asked_at"].append(row[4])
    # Return as a list
    return jsonify(list(questions_dict.values()))

@applied_jobs_bp.route("/interview_questions", methods=["POST"])
def add_interview_question():
    data = request.json
    job_id = data.get("job_id")
    company = data.get("company")
    question = data.get("question")
    ctc_offered = data.get("ctc_offered", "")
    description = data.get("description", question)  # For future extensibility
    if not question or not company:
        return jsonify({"success": False, "message": "Missing question or company."}), 400
    conn = get_connection()
    cursor = conn.cursor()
    # Check if question exists for any company (case-insensitive, trimmed)
    cursor.execute("SELECT id, company FROM interview_questions WHERE LOWER(TRIM(question)) = ?", (question.strip().lower(),))
    existing = cursor.fetchall()
    companies = [row[1] for row in existing]
    if company in companies:
        conn.close()
        return jsonify({"success": False, "message": "Question already exists for this company."}), 200
    # Otherwise, insert new row
    cursor.execute(
        "INSERT INTO interview_questions (job_id, company, question, ctc_offered) VALUES (?, ?, ?, ?)",
        (job_id, company, question.strip(), ctc_offered)
    )
    conn.commit()
    conn.close()
    return jsonify(success=True)

@applied_jobs_bp.route("/interview_questions/<int:question_id>", methods=["DELETE"])
def delete_interview_question(question_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM interview_questions WHERE id = ?", (question_id,))
    conn.commit()
    conn.close()
    return jsonify(success=True)

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