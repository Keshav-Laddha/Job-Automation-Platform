# File: backend/server/reminder_service.py

from apscheduler.schedulers.background import BlockingScheduler
from backend.database.db import get_connection
import smtplib, os
from email.mime.text import MIMEText
from datetime import datetime, timedelta

def send_deadline_reminders():
    conn = get_connection()
    cursor = conn.cursor()

    upcoming = (datetime.today() + timedelta(days=2)).strftime("%Y-%m-%d")
    cursor.execute("SELECT * FROM applied_jobs WHERE deadline = ?", (upcoming,))
    rows = cursor.fetchall()

    if rows:
        body = "\n".join(f"{r[1]} - {r[2]} (Due: {r[7]})" for r in rows)
        msg = MIMEText(body)
        msg["Subject"] = "📅 Job Application Deadline Reminder"
        msg["From"] = os.getenv("SMTP_USER")
        msg["To"] = os.getenv("TO_EMAIL")

        with smtplib.SMTP(os.getenv("SMTP_HOST"), int(os.getenv("SMTP_PORT", "587"))) as server:
            server.starttls()
            server.login(os.getenv("SMTP_USER"), os.getenv("SMTP_PASS"))
            server.send_message(msg)

    conn.close()

def send_followup_reminders():
    conn = get_connection()
    cursor = conn.cursor()

    today = datetime.today().strftime("%Y-%m-%d")
    cursor.execute("SELECT * FROM applied_jobs WHERE follow_up_date = ? AND reminder = 1", (today,))
    rows = cursor.fetchall()

    if rows:
        body = "\n\n".join(
            f"Follow up for: {r[2]} at {r[1]}\nHR Contact: {r[5] or 'N/A'}\nNotes: {r[10] or 'N/A'}" for r in rows
        )
        msg = MIMEText(body)
        msg["Subject"] = "🔔 Follow-Up Reminder for Today"
        msg["From"] = os.getenv("SMTP_USER")
        msg["To"] = os.getenv("TO_EMAIL")

        with smtplib.SMTP(os.getenv("SMTP_HOST"), int(os.getenv("SMTP_PORT", "587"))) as server:
            server.starttls()
            server.login(os.getenv("SMTP_USER"), os.getenv("SMTP_PASS"))
            server.send_message(msg)

    conn.close()

sched = BlockingScheduler()
sched.add_job(send_deadline_reminders, "cron", hour=9)  # runs every day at 9 AM
sched.add_job(send_followup_reminders, "cron", hour=8)  # runs every day at 8 AM

if __name__ == "__main__":
    sched.start()