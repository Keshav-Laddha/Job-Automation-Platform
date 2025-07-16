import React, { useEffect, useState, useMemo } from "react";
import axios from "axios";
import InterviewQuestions from "../components/InterviewQuestions"; // (to be created)
import { useToast } from "../components/Toast";

// Utility to normalize strings for search (case, dot, and space insensitive)
function normalizeString(str) {
  return (str || "").toLowerCase().replace(/\s+/g, "").replace(/\./g, "");
}

const AppliedJobs = () => {
  const [appliedJobs, setAppliedJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState("");
  const [reminderFilter, setReminderFilter] = useState("");
  const [sortBy, setSortBy] = useState("applied_at");
  const toast = useToast();

  useEffect(() => {
    fetchAppliedJobs();
  }, []);

  const fetchAppliedJobs = async () => {
    try {
      const res = await axios.get(`${process.env.REACT_APP_API_URL}/applied`);
      if (typeof res.data === 'string' && res.data.startsWith('<!DOCTYPE html>')) {
        toast.showToast('Ngrok error or rate limit. Please restart ngrok or try again later.', 'error');
        setAppliedJobs([]);
        return;
      }
      console.log("✅ Applied jobs API raw response:", res.data);
      // Defensive check
      if (Array.isArray(res.data)) {
        setAppliedJobs(res.data);
      } else {
        console.warn("❌ API did not return an array:", res.data);
        setAppliedJobs([]);
        toast.showToast('API did not return an array. Check backend.', 'error');
      }
    } catch (err) {
      console.error("Error fetching applied jobs:", err);
      setAppliedJobs([]);
      toast.showToast('Error fetching applied jobs.', 'error');
    } finally {
      setLoading(false);
    }
  };

  const updateJobStatus = async (jobId, field, value) => {
    try {
      await axios.patch(`${process.env.REACT_APP_API_URL}/applied/${jobId}`, {
        [field]: value
      });
      fetchAppliedJobs(); // Refresh the list
      toast.showToast("Job updated!", "success");
    } catch (err) {
      toast.showToast("Error updating job", "error");
    }
  };

  const deleteJob = async (jobId) => {
    try {
      await axios.delete(`${process.env.REACT_APP_API_URL}/applied/${jobId}`);
      fetchAppliedJobs(); // Refresh the list
      toast.showToast("Job deleted!", "success");
    } catch (err) {
      toast.showToast("Error deleting job", "error");
    }
  };

  const uploadResume = async (jobId, file) => {
    const formData = new FormData();
    formData.append("resume", file);
    try {
      await axios.post(`${process.env.REACT_APP_API_URL}/applied/${jobId}/upload_resume`, formData);
      fetchAppliedJobs();
      toast.showToast("Resume uploaded!", "success");
    } catch (err) {
      toast.showToast("Error uploading resume", "error");
    }
  };

  // Filtering and sorting logic
  const filteredJobs = useMemo(() => {
    let jobs = [...appliedJobs];
    // Filter out known dummy jobs
    const dummyCompanies = [
      "Tech Corp", "Web Solutions", "Analytics Inc", "Cloud Systems", "Startup XYZ", "AI Company"
    ];
    jobs = jobs.filter(j => !dummyCompanies.includes(j.company));
    if (search) {
      const s = normalizeString(search);
      jobs = jobs.filter(j =>
        (j.company && normalizeString(j.company).includes(s)) ||
        (j.title && normalizeString(j.title).includes(s)) ||
        (j.notes && normalizeString(j.notes).includes(s))
      );
    }
    if (statusFilter) {
      jobs = jobs.filter(j => j.status === statusFilter);
    }
    if (reminderFilter === "yes") {
      jobs = jobs.filter(j => !!j.reminder);
    } else if (reminderFilter === "no") {
      jobs = jobs.filter(j => !j.reminder);
    }
    // Always show newest jobs at the top
    jobs.sort((a, b) => new Date(b.applied_at) - new Date(a.applied_at));
    return jobs;
  }, [appliedJobs, search, statusFilter, reminderFilter, sortBy]);

  if (loading) return <div className="text-center py-8">Loading...</div>;

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">📋 Applied Jobs Tracker</h1>

      {/* Filters and Search */}
      <div className="flex flex-wrap gap-4 mb-6 items-end">
        <div>
          <label className="block text-gray-700 text-sm mb-1">Search</label>
          <input
            type="text"
            placeholder="Search company, title, or notes..."
            value={search}
            onChange={e => setSearch(e.target.value)}
            className="border rounded px-3 py-1 w-56"
          />
        </div>
        <div>
          <label className="block text-gray-700 text-sm mb-1">Status</label>
          <select
            value={statusFilter}
            onChange={e => setStatusFilter(e.target.value)}
            className="border rounded px-3 py-1"
          >
            <option value="">All</option>
            <option value="Applied">Applied</option>
            <option value="Interview">Interview</option>
            <option value="Rejected">Rejected</option>
            <option value="Accepted">Accepted</option>
          </select>
        </div>
        <div>
          <label className="block text-gray-700 text-sm mb-1">Reminder</label>
          <select
            value={reminderFilter}
            onChange={e => setReminderFilter(e.target.value)}
            className="border rounded px-3 py-1"
          >
            <option value="">All</option>
            <option value="yes">With Reminder</option>
            <option value="no">No Reminder</option>
          </select>
        </div>
        <div>
          <label className="block text-gray-700 text-sm mb-1">Sort By</label>
          <select
            value={sortBy}
            onChange={e => setSortBy(e.target.value)}
            className="border rounded px-3 py-1"
          >
            <option value="applied_at">Applied Date</option>
            <option value="deadline">Deadline</option>
            <option value="follow_up_date">Follow Up Date</option>
          </select>
        </div>
      </div>

      {filteredJobs.length === 0 ? (
        <div className="text-center py-8 text-gray-500">
          No applied jobs match your filters.
        </div>
      ) : (
        <div className="space-y-4">
          {filteredJobs.map((job) => {
              // Reminder highlight logic
              const followUpSoon = job.follow_up_date && new Date(job.follow_up_date) - new Date() < 3 * 24 * 60 * 60 * 1000;
              return (
                <div key={job.id} className={`bg-white rounded-lg shadow-md p-6 border ${followUpSoon ? "border-yellow-400" : ""}`}>
                  <div className="flex justify-between items-start mb-4">
                    <div>
                      <h2 className="text-xl font-semibold">{job.company}</h2>
                      <p className="text-gray-600">{job.title}</p>
                      <a
                        href={job.link}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-blue-600 hover:underline text-sm"
                      >
                        🔗 View Job Posting
                      </a>
                    </div>
                    <div className="text-right space-y-2">
                      <select
                        value={job.status}
                        onChange={(e) => updateJobStatus(job.id, "status", e.target.value)}
                        className="border rounded px-3 py-1 mb-2"
                      >
                        <option value="Applied">Applied</option>
                        <option value="Interview">Interview</option>
                        <option value="Rejected">Rejected</option>
                        <option value="Accepted">Accepted</option>
                      </select>
                      <input
                        type="text"
                        placeholder="CTC Offered"
                        value={job.ctc || ""}
                        onChange={(e) => updateJobStatus(job.id, "ctc", e.target.value)}
                        className="w-full border rounded px-2 py-1 mt-1"
                      />
                      <button
                        onClick={() => deleteJob(job.id)}
                        className="block text-red-600 hover:text-red-800 text-sm"
                      >
                        🗑️ Delete
                      </button>
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                    <div>
                      <label className="block text-gray-600">Notes:</label>
                      <textarea
                        value={job.notes || ""}
                        onChange={(e) => updateJobStatus(job.id, "notes", e.target.value)}
                        className="w-full border rounded px-2 py-1 mt-1"
                        rows="2"
                      />
                    </div>
                    <div>
                      <label className="block text-gray-600">HR Contact:</label>
                      <input
                        type="text"
                        value={job.hr_contact || ""}
                        onChange={(e) => updateJobStatus(job.id, "hr_contact", e.target.value)}
                        className="w-full border rounded px-2 py-1 mt-1"
                      />
                    </div>
                    <div>
                      <label className="block text-gray-600">Follow Up Date:</label>
                      <input
                        type="date"
                        value={job.follow_up_date ? job.follow_up_date.split("T")[0] : ""}
                        onChange={(e) => updateJobStatus(job.id, "follow_up_date", e.target.value)}
                        className="w-full border rounded px-2 py-1 mt-1"
                      />
                    </div>
                    <div>
                      <label className="block text-gray-600">Last Date to Apply:</label>
                      <input
                        type="date"
                        value={job.deadline ? job.deadline.split("T")[0] : ""}
                        onChange={(e) => updateJobStatus(job.id, "deadline", e.target.value)}
                        className="w-full border rounded px-2 py-1 mt-1"
                      />
                    </div>
                  </div>

                  <div className="mt-4 flex flex-col md:flex-row gap-4 items-center">
                    <div>
                      <label className="block text-gray-600">Resume:</label>
                      <input
                        type="file"
                        accept=".pdf,.doc,.docx"
                        onChange={e => e.target.files[0] && uploadResume(job.id, e.target.files[0])}
                        className="block mt-1"
                      />
                      {job.resume_path && (
                        <a
                          href={`${process.env.REACT_APP_API_URL}/applied/resume/${job.resume_path}`}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-blue-600 hover:underline text-sm ml-2"
                        >
                          📄 View Resume
                        </a>
                      )}
                    </div>
                    <div>
                      <label className="block text-gray-600">Reminder:</label>
                      <input
                        type="checkbox"
                        checked={!!job.reminder}
                        onChange={e => updateJobStatus(job.id, "reminder", e.target.checked ? 1 : 0)}
                        className="ml-2"
                      />
                      {followUpSoon && <span className="ml-2 text-yellow-600 font-semibold">⏰ Upcoming Follow Up!</span>}
                    </div>
                    <div>
                      <label className="block text-gray-600">Applied On:</label>
                      <div>{job.applied_at ? new Date(job.applied_at).toLocaleDateString() : "-"}</div>
                    </div>
                  </div>

                  {/* Interview Questions Section */}
                  <div className="mt-6">
                    <InterviewQuestions jobId={job.id} company={job.company} />
                  </div>
                </div>
              );
            })}
        </div>
      )}
    </div>
  );
};

export default AppliedJobs;