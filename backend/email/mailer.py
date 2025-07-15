# File: backend/email/mailer.py
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
TO_EMAIL = os.getenv("TO_EMAIL")


def generate_prompt(job):
    return f"""You are an AI resume assistant.

**Job Title**: {job['title'].title()}
**Company**: {job['company']}
**Job Link**: {job['link']}

Using the job title and company above, and considering my resume below:

[PASTE RESUME TEXT HERE]

Write 3–5 tailored bullet points that will improve my chances of passing ATS filters for this role.
"""

def get_company_logo_url(company_name):
    return f"{os.getenv('CLEARBIT_LOGO_API', 'https://logo.clearbit.com')}/{company_name.lower()}.com"

def generate_email_html(jobs):
    job_html = ""
    bart_base_url = os.getenv("BART_PUBLIC_URL")

    for job in jobs:
        prompt = generate_prompt(job)
        chatgpt_link = "https://chat.openai.com/"
        bart_link = f"{bart_base_url}/optimize?job_title={quote_plus(job['title'])}&job_description={quote_plus(job['link'])}"
        apply_link = f"{bart_base_url}/applied/new?company={quote_plus(job['company'])}&title={quote_plus(job['title'])}&link={quote_plus(job['link'])}"

        job_html += f"""
        <div style="margin-bottom: 20px; padding: 10px; border: 1px solid #ddd; font-family: Arial, sans-serif;">
            <h3 style="margin-bottom: 5px;">{job['company']} - {job['title'].title()}</h3>
            <p style="margin: 5px 0;"><b>Location(s):</b> {job.get('location', 'N/A')}</p>
            <p style="margin: 5px 0;"><a href="{job['link']}" target="_blank">🔗 View Job Posting</a></p>
            <p style="margin: 5px 0;">
                <b>Prompt:</b><br>
                <textarea rows="6" style="width:100%; font-family: monospace; background:#f9f9f9; border:1px solid #ccc; padding: 8px;">{prompt}</textarea>
            </p>
            <div style="margin-top: 10px;">
                <a href="{chatgpt_link}" style="padding: 8px 12px; background-color: #10a37f; color: white; text-decoration: none; border-radius: 5px;">💬 Open in ChatGPT</a>
                &nbsp;
                <a href="{bart_link}" style="padding: 8px 12px; background-color: #0056d2; color: white; text-decoration: none; border-radius: 5px;">🤖 Ask BART AI</a>
                <a href="{apply_link}" style="padding: 8px 12px; background-color: #28a745; color: white; text-decoration: none; border-radius: 5px;">📥 Add to Tracker</a>
            </div>
        </div>
        """

    html = f"""
    <html>
    <body>
        <h2 style="font-family: Arial, sans-serif;">🎯 New Job Matches</h2>
        {job_html}
        <p style="font-family: Arial, sans-serif;">Good luck! 🚀</p>
    </body>
    </html>
    """
    return html


def send_job_email(jobs):
    if not jobs:
        print("[INFO] No jobs to send.")
        return

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "🔔 New Internship Opportunities Found!"
    msg["From"] = SMTP_USER
    msg["To"] = TO_EMAIL

    html_content = generate_email_html(jobs)
    part2 = MIMEText(html_content, "html")

    msg.attach(part2)

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_USER, TO_EMAIL, msg.as_string())
            print("[✓] Email sent successfully!")
    except Exception as e:
        print(f"[ERROR] Failed to send email: {e}")