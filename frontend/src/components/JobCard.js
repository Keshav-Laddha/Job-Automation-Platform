//File: frontend/src/components/JobCard.jsx
import React, { useState } from "react";


const JobCard = ({ job }) => {
  const prompt = `Act as an AI assistant for resume tailoring.\n\nHere is a job description:\nTitle: ${job.title}\nCompany: ${job.company}\nLink: ${job.link}\n\nHere is my resume:\n[Paste Resume Text Here]\n\nGive me resume bullet points that improve my ATS score for this job and ask me to select which ones to include.`;

  const chatgptLink = "https://chat.openai.com/";
  const bartLink = `/form?job_title=${encodeURIComponent(job.title)}`;

  const copyToClipboard = () => {
    navigator.clipboard.writeText(prompt).then(
      () => alert("✅ Prompt copied to clipboard!"),
      () => alert("❌ Failed to copy prompt.")
    );
  };

  const addToTracker = () => {
    // Build query string with all job info
    const params = new URLSearchParams({
      company: job.company,
      title: job.title,
      link: job.link,
      // Add more fields as needed (status, hr_contact, etc.)
    });
    // Redirect to backend /applied/new endpoint
    window.location.href = `${process.env.REACT_APP_API_URL}/applied/new?${params.toString()}`;
  };

  return (
    <div className="bg-white rounded-lg shadow-md border p-6 mb-8 hover:shadow-lg transition-all max-w-3xl mx-auto">
      {/* Title */}
      <h2 className="text-xl font-semibold text-gray-800 mb-1">
        {job.company} <span className="text-gray-500">—</span> {job.title}
      </h2>

      {/* Link */}
      <a
        href={job.link}
        target="_blank"
        rel="noopener noreferrer"
        className="text-blue-600 hover:underline text-sm mb-4 inline-block"
      >
        🔗 View Job Posting
      </a>

      {/* Prompt */}
      <textarea
        readOnly
        className="w-full h-40 p-3 border border-gray-300 rounded-md bg-gray-50 font-mono text-sm mb-4 resize-none"
        value={prompt}
      ></textarea>

      {/* Actions */}
      <div className="flex flex-wrap gap-2 mt-2">
        <button
          onClick={copyToClipboard}
          className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 transition"
        >
          ✅ Copy Prompt
        </button>
        <a
          href={chatgptLink}
          target="_blank"
          rel="noopener noreferrer"
          className="bg-purple-600 text-white px-4 py-2 rounded hover:bg-purple-700 transition"
        >
          💬 Open in ChatGPT
        </a>
        <a
          href={bartLink}
          target="_blank"
          rel="noopener noreferrer"
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
        >
          🤖 Optimize with BART
        </a>
        <button
          onClick={addToTracker}
          className="bg-orange-600 text-white px-4 py-2 rounded hover:bg-orange-700 transition"
        >
          📋 Add to Tracker
        </button>
      </div>
    </div>
  );
};

export default JobCard;