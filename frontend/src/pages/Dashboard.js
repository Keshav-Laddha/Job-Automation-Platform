import React, { useEffect, useState } from "react";
import JobCard from "../components/JobCard";
import axios from "axios";
import Modal from "../components/Modal";

const Dashboard = () => {
  const [jobs, setJobs] = useState([]);
  const [scraping, setScraping] = useState(false);
  const [excelFile, setExcelFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadError, setUploadError] = useState("");
  const [cooldownMsg, setCooldownMsg] = useState("");
  const [showAddJobModal, setShowAddJobModal] = useState(false);
  const [manualJob, setManualJob] = useState({
    company: "",
    title: "",
    link: "",
    status: "Applied",
    ctc: "",
    notes: "",
    hr_contact: "",
    follow_up_date: "",
    deadline: "",
    reminder: false,
    resume: null,
    applied_at: new Date().toISOString().split("T")[0],
  });
  const [savingJob, setSavingJob] = useState(false);

  useEffect(() => {
    const fetchJobs = async () => {
      try {
        const res = await axios.get(`${process.env.REACT_APP_API_URL}/jobs`);
        setJobs(res.data);
      } catch (err) {
        console.error("Error fetching jobs:", err);
      }
    };

    fetchJobs();
  }, []);

  const handleScrapeAndEmail = async () => {
    setScraping(true);
    try {
      const res = await axios.post(`${process.env.REACT_APP_API_URL}/scrape-and-email`);
      alert(res.data.message || "Jobs scraped and emailed!");
    } catch (err) {
      alert(err.response?.data?.message || "Failed to scrape and email jobs.");
    }
    setScraping(false);
  };

  const handleExcelChange = (e) => {
    setExcelFile(e.target.files[0]);
  };

  const handleExcelUpload = async () => {
    if (!excelFile) {
      alert("Please select an Excel file to upload.");
      return;
    }
    setUploading(true);
    setUploadError("");
    setCooldownMsg("");
    const formData = new FormData();
    formData.append("excel", excelFile);
    try {
      const res = await axios.post(`${process.env.REACT_APP_API_URL}/upload-company-excel`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      alert(res.data.message || "Config generated successfully!");
    } catch (err) {
      const msg = err.response?.data?.message || "Failed to generate config.";
      setUploadError(msg);
      if (err.response?.status === 429) setCooldownMsg(msg);
      else alert(msg);
    }
    setUploading(false);
  };

  const handleManualJobChange = (e) => {
    const { name, value, type, checked, files } = e.target;
    if (type === "checkbox") {
      setManualJob((prev) => ({ ...prev, [name]: checked }));
    } else if (type === "file") {
      setManualJob((prev) => ({ ...prev, resume: files[0] }));
    } else {
      setManualJob((prev) => ({ ...prev, [name]: value }));
    }
  };

  const handleManualJobSubmit = async (e) => {
    e.preventDefault();
    setSavingJob(true);
    try {
      const formData = new FormData();
      Object.entries(manualJob).forEach(([key, value]) => {
        if (key === "resume" && value) {
          formData.append("resume", value);
        } else if (key !== "resume") {
          formData.append(key, value);
        }
      });
      await axios.post(`${process.env.REACT_APP_API_URL}/applied`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setShowAddJobModal(false);
      setManualJob({
        company: "",
        title: "",
        link: "",
        status: "Applied",
        ctc: "",
        notes: "",
        hr_contact: "",
        follow_up_date: "",
        deadline: "",
        reminder: false,
        resume: null,
        applied_at: new Date().toISOString().split("T")[0],
      });
      alert("Saved successfully! See Applied Jobs.");
    } catch (err) {
      console.error("Failed to save job:", err, err?.response?.data);
      alert(err?.response?.data?.error || "Failed to save job. Please try again.");
    }
    setSavingJob(false);
  };

  return (
    <div className="min-h-screen bg-gray-100 py-10 px-4">
      <h1 className="text-4xl font-bold text-center text-blue-700 mb-10">🚀 AI Job Assistant</h1>
      {/* Excel Upload Section */}
      <div className="max-w-xl mx-auto bg-white rounded-lg shadow p-6 mb-8 border-2 border-blue-200">
        <h2 className="text-2xl font-semibold mb-2 text-blue-800 flex items-center gap-2">
          <span role="img" aria-label="upload">📤</span> Upload Company Excel
        </h2>
        <div className="bg-blue-50 border-l-4 border-blue-400 p-4 mb-4 rounded">
          <div className="font-semibold text-blue-700 mb-1 flex items-center gap-2">
            <span role="img" aria-label="info">ℹ️</span> Please read before uploading:
          </div>
          <ul className="list-disc list-inside text-sm text-blue-900 space-y-1">
            <li>Max <b>20 companies per upload</b>. Only <b>one upload per hour</b> is allowed.</li>
            <li>Max <b>100 companies scraped per 24 hours</b> (across all uploads).</li>
            <li>Scraping strictly <b>respects robots.txt</b> and site rules, including <b>Crawl-delay</b>.</li>
            <li>There are <b>delays between all requests</b> to avoid overloading servers.</li>
            <li>If a site shows a captcha or blocks scraping, it is skipped and scraping is paused if needed.</li>
            <li>All scraping activity is <b>logged for transparency</b>.</li>
            <li>Any company can <b>request data deletion</b> at any time (see below).</li>
            <li>See the <a href="/README.md#ethical-use-policy" target="_blank" rel="noopener noreferrer" className="underline text-blue-700">Ethical Use Policy</a> for full details.</li>
          </ul>
        </div>
        <p className="text-gray-700 text-sm mb-3">
          <b>Excel Format Guide:</b> The file should have the following columns (in order):<br />
          <span className="font-mono">Company Name</span>, <span className="font-mono">URL</span>, <span className="font-mono">Keywords</span> (comma-separated), <span className="font-mono">Location</span>.<br />
          Example row: <span className="font-mono">Acme Corp | https://acme.com/careers | python, data, ai | New York</span>
        </p>
        {uploadError && <div className="text-red-600 mb-2">{uploadError}</div>}
        {cooldownMsg && <div className="text-yellow-700 mb-2">{cooldownMsg}</div>}
        <div className="flex items-center gap-3 mb-2">
          <input
            type="file"
            accept=".xlsx,.xls"
            onChange={handleExcelChange}
            className="border rounded px-3 py-2"
            disabled={uploading || !!cooldownMsg}
          />
          <button
            onClick={handleExcelUpload}
            className={`bg-blue-600 text-white px-4 py-2 rounded shadow hover:bg-blue-700 transition font-semibold ${uploading || cooldownMsg ? 'opacity-50 cursor-not-allowed' : ''}`}
            disabled={uploading || !!cooldownMsg}
          >
            {uploading ? "Uploading..." : "Upload & Generate Config"}
          </button>
        </div>
        <div className="text-xs text-gray-600 mt-2">
          <span role="img" aria-label="check">✅</span> After upload: Your Excel will be checked for format and limits. If valid, a config is generated and you can start scraping jobs.<br />
          <span role="img" aria-label="delete">🗑️</span> <b>Data Deletion:</b> If a company requests data removal, contact the maintainer and all related data will be deleted promptly.
        </div>
      </div>
      <div className="flex justify-center mb-6 gap-4">
        <button
          onClick={handleScrapeAndEmail}
          className={`bg-green-600 text-white px-6 py-2 rounded shadow hover:bg-green-700 transition font-semibold ${scraping ? 'opacity-50 cursor-not-allowed' : ''}`}
          disabled={scraping}
        >
          {scraping ? "Scraping & Emailing..." : "🔄 Scrape Jobs & Email Me"}
        </button>
        <button
          onClick={() => setShowAddJobModal(true)}
          className="bg-orange-600 text-white px-6 py-2 rounded shadow hover:bg-orange-700 transition font-semibold"
        >
          ➕ Add Job to Job Tracker
        </button>
      </div>
      {showAddJobModal && (
        <Modal onClose={() => setShowAddJobModal(false)}>
          <h2 className="text-xl font-bold mb-4">Add Job to Job Tracker</h2>
          <form onSubmit={handleManualJobSubmit} className="space-y-3">
            <div>
              <label className="block text-gray-700">Company</label>
              <input type="text" name="company" value={manualJob.company} onChange={handleManualJobChange} className="border rounded px-3 py-1 w-full" required />
            </div>
            <div>
              <label className="block text-gray-700">Title</label>
              <input type="text" name="title" value={manualJob.title} onChange={handleManualJobChange} className="border rounded px-3 py-1 w-full" required />
            </div>
            <div>
              <label className="block text-gray-700">Link</label>
              <input type="url" name="link" value={manualJob.link} onChange={handleManualJobChange} className="border rounded px-3 py-1 w-full" />
            </div>
            <div>
              <label className="block text-gray-700">Status</label>
              <select name="status" value={manualJob.status} onChange={handleManualJobChange} className="border rounded px-3 py-1 w-full">
                <option value="Applied">Applied</option>
                <option value="Interview">Interview</option>
                <option value="Rejected">Rejected</option>
                <option value="Accepted">Accepted</option>
              </select>
            </div>
            <div>
              <label className="block text-gray-700">CTC Offered</label>
              <input type="text" name="ctc" value={manualJob.ctc} onChange={handleManualJobChange} className="border rounded px-3 py-1 w-full" />
            </div>
            <div>
              <label className="block text-gray-700">Notes</label>
              <textarea name="notes" value={manualJob.notes} onChange={handleManualJobChange} className="border rounded px-3 py-1 w-full" rows="2" />
            </div>
            <div>
              <label className="block text-gray-700">HR Contact</label>
              <input type="text" name="hr_contact" value={manualJob.hr_contact} onChange={handleManualJobChange} className="border rounded px-3 py-1 w-full" />
            </div>
            <div>
              <label className="block text-gray-700">Follow Up Date</label>
              <input type="date" name="follow_up_date" value={manualJob.follow_up_date} onChange={handleManualJobChange} className="border rounded px-3 py-1 w-full" />
            </div>
            <div>
              <label className="block text-gray-700">Last Date to Apply</label>
              <input type="date" name="deadline" value={manualJob.deadline} onChange={handleManualJobChange} className="border rounded px-3 py-1 w-full" />
            </div>
            <div className="flex items-center gap-2">
              <input type="checkbox" name="reminder" checked={manualJob.reminder} onChange={handleManualJobChange} />
              <label className="text-gray-700">Reminder</label>
            </div>
            <div>
              <label className="block text-gray-700">Resume (optional)</label>
              <input type="file" name="resume" accept=".pdf,.doc,.docx" onChange={handleManualJobChange} className="border rounded px-3 py-1 w-full" />
            </div>
            <div>
              <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition" disabled={savingJob}>
                {savingJob ? "Saving..." : "Save Job"}
              </button>
            </div>
          </form>
        </Modal>
      )}
      {jobs.map((job, idx) => (
        <JobCard key={idx} job={job} />
      ))}
    </div>
  );
};

export default Dashboard;