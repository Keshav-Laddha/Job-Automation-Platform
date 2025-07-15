## 📌 Job Application Automation Platform

> Automate your internship/job hunt with real-time scraping, email alerts, and AI-powered resume optimization using BART!

---

### 🛠️ Tech Stack

| Layer          | Technologies                                                                |
| -------------- | --------------------------------------------------------------------------- |
| **Frontend**   | React, Tailwind CSS (Coming Next)                                           |
| **Backend**    | Python, Flask, HuggingFace Transformers (BART), FastAPI (optional), Uvicorn |
| **AI Models**  | `facebook/bart-large-cnn` (via HuggingFace)                                 |
| **Email**      | Gmail SMTP (via `smtplib`)                                                  |
| **Deployment** | Ngrok (for local tunneling)                                                 |

---

### 🚀 Features

* 🔍 **Job Scraper**: Crawls major career sites (Google, Microsoft, etc.) using keywords and locations.
* 📬 **Automated Email Alerts**: Sends you tailored jobs daily/periodically with ATS-tailored prompt.
* 🤖 **AI Resume Tailoring**: Suggests resume bullet points using BART or routes you to ChatGPT.
* 💡 **Copyable Prompts**: Easy copy-paste prompts for ChatGPT to get your resume tailored fast.
* 🎨 **Web Form Interface**: Use a simple UI to get real-time BART suggestions for any job description (via Flask).

---

### 📁 Project Structure

```
job-automation/
├── backend/
│   ├── scraper/             # Job scrapers for different companies
│   │   └── job_scraper.py
│   ├── resume/
│   │   └── ats_optimizer.py  # AI-based ATS optimizer using BART
│   ├── server/
│   │   ├── bart_server.py    # Flask server with form + /optimize API
│   │   └── templates/
│   │       └── form.html     # Web UI for resume optimization
│   ├── email/
│   │   └── mailer.py         # Sends job matches via email
├── frontend/                # (Coming Soon)
├── .env                     # SMTP creds, etc.
└── README.md
```

---

### 🔧 .env Configuration

Create a `.env` file in the root:

```
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASS=your_app_password
TO_EMAIL=recipient_email@gmail.com
```

---

### 🧪 How to Run Locally

#### ✅ 1. Clone & Set Up Environment

```bash
git clone https://github.com/yourusername/job-automation
cd job-automation
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### ✅ 2. Run the Job Scraper + Emailer

```bash
python backend/scraper/job_scraper.py
```

You'll receive an email with job listings + ChatGPT/BART links.

#### ✅ 3. Start the Resume Optimizer Server (BART)

```bash
python backend/server/bart_server.py
```

#### ✅ 4. Start a Local Tunnel (Optional)

```bash
ngrok http 5002
```

#### ✅ 5. Access Web Form

Open in browser:

```
http://localhost:5002/form
```

---

### 🌐 API Usage

#### `POST /optimize`

**Request:**

```json
{
  "resume_point": "Built a full-stack web app",
  "job_title": "Frontend Developer at Google"
}
```

**Response:**

```json
{
  "optimized_points": [
    "Developed responsive web application using modern JS frameworks aligned with Google's frontend stack.",
    ...
  ]
}
```

---

### ✨ Example Email Preview

You’ll receive an email with:

* ✅ Job Title & Company
* 📌 Link to Job Posting
* 📋 Prompt for ChatGPT
* 💬 Button to Open ChatGPT
* ⚡️ Optional: BART Optimizer Link (`http://localhost:5002/form?job_title=...`)

---

### 🧠 Possible Future Enhancements

* 🔭 Add filtering by location, stipend, tech stack
* 🌍 Deploy Flask server publicly
* 🤝 Google Calendar Integration for job deadlines/interviews
* 📄 Auto-tailor & attach updated resume PDF
* 👨‍💻 Add Open Source contribution tracker

---

### 🧑‍💻 Author

**Keshav Laddha**
B.Tech CSE | LNMIIT
Competitive Programmer • AI/ML & Web Dev Enthusiast
[GitHub](https://github.com/keshavladdha) • [LinkedIn](https://linkedin.com/in/keshavladdha)

---

### 📜 License

MIT License

---