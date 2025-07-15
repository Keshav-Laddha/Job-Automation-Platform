# File: backend/database/models.py
# Description: Interfaces for querying and updating the job/feedback database

from backend.database.db import get_connection


def insert_job(company, title, link, matched_keyword):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO jobs (company, title, link, matched_keyword)
        VALUES (?, ?, ?, ?)
    """, (company, title, link, matched_keyword))
    conn.commit()
    conn.close()


def get_all_jobs():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jobs ORDER BY timestamp DESC")
    jobs = cursor.fetchall()
    conn.close()
    return jobs


def get_jobs_by_keyword(keyword):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jobs WHERE matched_keyword = ? ORDER BY timestamp DESC", (keyword,))
    jobs = cursor.fetchall()
    conn.close()
    return jobs


def insert_resume_feedback(job_id, selected_points, feedback):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO resume_feedback (job_id, selected_points, feedback)
        VALUES (?, ?, ?)
    """, (job_id, selected_points, feedback))
    conn.commit()
    conn.close()


def get_feedback_for_job(job_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM resume_feedback WHERE job_id = ?", (job_id,))
    feedbacks = cursor.fetchall()
    conn.close()
    return feedbacks

def insert_applied_job(job_id, company, title, status="Applied", notes="", hr_contact="", deadline=""):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO applied_jobs (job_id, company, title, status, notes, hr_contact, deadline)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (job_id, company, title, status, notes, hr_contact, deadline))
    conn.commit()
    conn.close()


def get_all_applied_jobs():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM applied_jobs ORDER BY applied_at DESC")
    jobs = cursor.fetchall()
    conn.close()
    return jobs


def update_applied_job(applied_id, field, value):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"UPDATE applied_jobs SET {field} = ? WHERE id = ?", (value, applied_id))
    conn.commit()
    conn.close()


def delete_applied_job(applied_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM applied_jobs WHERE id = ?", (applied_id,))
    conn.commit()
    conn.close()

def update_resume_file(job_id, filename):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE applied_jobs SET resume_path = ? WHERE id = ?", (filename, job_id))
    conn.commit()
    conn.close()