<<<<<<< HEAD
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
=======
# 💼 Job Automation Platform

A powerful, AI-enhanced job application manager that **automates job scraping**, **tracks applications**, **sends email reminders**, and **optimizes your resume with BART/ChatGPT**.
All with a clean and modern UI, built for efficiency.

---

## 🚀 Features at a Glance

### 🧠 AI Resume Optimization

* Tailored bullet points using **BART/ChatGPT**
* One-click prompts for editing in ChatGPT

### 🔍 Job Scraping & Alerts

* Manual and automated scraping from company sites & job boards
* Scheduled scraping (twice daily: 11:00 AM & 4:00 PM)
* Email delivery of job results

### 📋 Job Tracker

* Track application status: Applied, Interview, Rejected, Offer
* Upload resumes, add notes, HR contacts, and deadlines
* Follow-up reminders

### 📧 Email Notifications

* Curated job match alerts
* Deadline and follow-up email reminders

### 🎤 Interview Questions Manager

* Add, group, and manage unique interview questions
* Company badges and collapsible UI for better UX

### 📊 Analytics Dashboard

* Visual charts and stats using Chart.js
* Overview of application progress

### 💻 Modern UI/UX

* Responsive React + Tailwind CSS frontend
* Search, filter, and navigate effortlessly

---

## 🛠️ Tech Stack

| Area       | Tech Used                           |
| ---------- | ----------------------------------- |
| Frontend   | React, Tailwind CSS                 |
| Backend    | Flask (Python)                      |
| Database   | SQLite                              |
| Automation | Python scripts (scraping & email)   |
| Analytics  | Chart.js                            |
| Email      | SMTP (Gmail integration)            |
| Config     | dotenv for secure environment setup |

---

## 🚦 Local Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/job-automation.git
cd job-automation
```

### 2. Backend Setup

```bash
cd backend
python -m venv venv

# On Windows
venv\\Scripts\\activate

# On Mac/Linux
source venv/bin/activate

pip install -r ../requirements.txt

# Ensure backend/.env is configured
python server/bart_server.py
```

### 3. Frontend Setup

```bash
cd ../frontend
npm install

# Ensure frontend/.env is configured
npm start
>>>>>>> 8403121a4a208b4e3c5092ea0b6485f6ba3322b4
```

---

<<<<<<< HEAD
### 🔧 .env Configuration

Create a `.env` file in the root:

```
=======
## 🔐 Environment Variables

### backend/.env

```
FRONTEND_URL=http://localhost:3000
BART_PUBLIC_URL=http://localhost:5002
CLEARBIT_LOGO_API=https://logo.clearbit.com
>>>>>>> 8403121a4a208b4e3c5092ea0b6485f6ba3322b4
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASS=your_app_password
<<<<<<< HEAD
TO_EMAIL=recipient_email@gmail.com
=======
TO_EMAIL=your_email@gmail.com
```

### frontend/.env

```
REACT_APP_API_URL=http://localhost:5002
CLEARBIT_LOGO_API=https://logo.clearbit.com
```

📌 **Note:** Use a Gmail App Password if 2FA is enabled.

---

## 🧩 Project Structure

```
Job Automation/
├── backend/
│   ├── database/
│   ├── email/
│   ├── resume/
│   ├── scraper/
│   ├── server/
│   ├── uploads/
│   └── utils/
└── frontend/
    ├── public/
    └── src/
        ├── components/
        └── pages/
>>>>>>> 8403121a4a208b4e3c5092ea0b6485f6ba3322b4
```

---

<<<<<<< HEAD
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
=======
## 📸 Screenshots

> Add screenshots of your Dashboard, Tracker, and Resume Optimizer here
> Example:

```
📊 Dashboard | 📁 Tracker | 📄 Resume Optimizer
>>>>>>> 8403121a4a208b4e3c5092ea0b6485f6ba3322b4
```

---

<<<<<<< HEAD
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
=======
## 🤝 Contributing

Pull requests are welcome!
For major changes, please open an issue first to discuss what you would like to change.

---

## 🛡️ License

This project is licensed under the [MIT License](LICENSE).

---

## ⭐ Credits

* [OpenAI](https://openai.com/) – for AI resume suggestions
* [Clearbit](https://clearbit.com) – for company logos
* [BART](https://huggingface.co/facebook/bart-large)

---

## 🌟 Show Your Support

If you found this project helpful, please ⭐ star the repository and share it with others!

>>>>>>> 8403121a4a208b4e3c5092ea0b6485f6ba3322b4
