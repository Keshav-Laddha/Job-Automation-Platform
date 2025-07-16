# File: backend/database/db.py
# Description: Sets up the SQLite database connection and initializes tables

import sqlite3
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "jobs.db"

DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def get_connection():
    conn = sqlite3.connect(str(DB_PATH))
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS applied_jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id INTEGER,
            company TEXT NOT NULL,
            title TEXT NOT NULL,
            status TEXT DEFAULT 'applied',
            link TEXT,
            resume_path TEXT,
            notes TEXT,
            hr_contact TEXT,
            deadline TEXT,
            applied_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            follow_up_date TEXT,
            reminder INTEGER DEFAULT 0,
            ctc TEXT,
            FOREIGN KEY(job_id) REFERENCES jobs(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interview_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id INTEGER,
            company TEXT,
            question TEXT,
            asked_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            ctc_offered TEXT,
            FOREIGN KEY(job_id) REFERENCES applied_jobs(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            title TEXT NOT NULL,
            link TEXT NOT NULL,
            matched_keyword TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resume_feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id INTEGER,
            selected_points TEXT,
            feedback TEXT,
            FOREIGN KEY(job_id) REFERENCES jobs(id)
        )
    """)

    # --- MIGRATION: Add 'link' column to interview_questions if not exists ---
    cursor.execute("PRAGMA table_info(interview_questions)")
    columns = [row[1] for row in cursor.fetchall()]
    if 'link' not in columns:
        cursor.execute("ALTER TABLE interview_questions ADD COLUMN link TEXT")
        print("✅ Added 'link' column to interview_questions table")
    # --- MIGRATION: Add 'description' column to interview_questions if not exists ---
    cursor.execute("PRAGMA table_info(interview_questions)")
    columns = [row[1] for row in cursor.fetchall()]
    if 'description' not in columns:
        cursor.execute("ALTER TABLE interview_questions ADD COLUMN description TEXT")
        print("✅ Added 'description' column to interview_questions table")

    # Insert sample data if applied_jobs table is empty
    
    # Also add some sample jobs data
    cursor.execute("SELECT COUNT(*) FROM jobs")
    if cursor.fetchone()[0] == 0:
        jobs_data = [
            ("Tech Corp", "Software Engineer", "https://example.com/job1", "python"),
            ("Web Solutions", "Frontend Developer", "https://example.com/job2", "react"),
            ("Analytics Inc", "Data Scientist", "https://example.com/job3", "machine learning"),
            ("Cloud Systems", "Backend Developer", "https://example.com/job4", "aws"),
            ("Startup XYZ", "Full Stack Developer", "https://example.com/job5", "javascript"),
            ("AI Company", "Machine Learning Engineer", "https://example.com/job6", "tensorflow")
        ]
        cursor.executemany(
            "INSERT INTO jobs (company, title, link, matched_keyword) VALUES (?, ?, ?, ?)",
            jobs_data
        )
        print("✅ Added sample data to jobs table")

    conn.commit()
    conn.close()
    print("✅ Database initialized successfully")

if __name__ == "__main__":
    init_db()