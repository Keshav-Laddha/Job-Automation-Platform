import React, { useEffect, useState } from "react";
import JobCard from "../components/JobCard";
import axios from "axios";

const Dashboard = () => {
  const [jobs, setJobs] = useState([]);
  const [scraping, setScraping] = useState(false);

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

  return (
    <div className="min-h-screen bg-gray-100 py-10 px-4">
      <h1 className="text-4xl font-bold text-center text-blue-700 mb-10">🚀 AI Job Assistant</h1>
      <div className="flex justify-center mb-6">
        <button
          onClick={handleScrapeAndEmail}
          className={`bg-green-600 text-white px-6 py-2 rounded shadow hover:bg-green-700 transition font-semibold ${scraping ? 'opacity-50 cursor-not-allowed' : ''}`}
          disabled={scraping}
        >
          {scraping ? "Scraping & Emailing..." : "🔄 Scrape Jobs & Email Me"}
        </button>
      </div>
      {jobs.map((job, idx) => (
        <JobCard key={idx} job={job} />
      ))}
    </div>
  );
};

export default Dashboard;