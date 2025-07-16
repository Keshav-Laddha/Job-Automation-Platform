// File: frontend/src/components/BartForm.jsx

import React, { useState, useEffect } from "react";
import axios from "axios";
import { useSearchParams } from "react-router-dom";

const BartForm = () => {
  const [jobTitle, setJobTitle] = useState("");
  const [jobDescription, setJobDescription] = useState(""); // ✅ NEW
  const [resumePoints, setResumePoints] = useState("");
  const [suggestions, setSuggestions] = useState([]);
  const [loading, setLoading] = useState(false);

  const [searchParams] = useSearchParams();

  useEffect(() => {
  const prefillTitle = searchParams.get("job_title");
  const prefillDescription = searchParams.get("job_description");

  if (prefillTitle) setJobTitle(prefillTitle);
  if (prefillDescription) setJobDescription(prefillDescription);
}, [searchParams]);


  const handleSubmit = async (e) => {
    e.preventDefault();
    setSuggestions([]);
    setLoading(true);

    const payload = {
      resume_points: resumePoints,
      job_title: jobTitle,
      job_description: jobDescription
    };

    console.log("🟢 API URL:", process.env.REACT_APP_API_URL);
    console.log('🟢 All env vars:', process.env);
    console.log('Environment:', process.env.NODE_ENV);
    console.log('API URL:', process.env.REACT_APP_API_URL);

    try {
      const res = await axios.post(`${process.env.REACT_APP_API_URL}/optimize`, payload, {
        headers: {
          'ngrok-skip-browser-warning': 'true'
        },
        resume_points: resumePoints.split('\n').join('\n'),
        job_title: jobTitle,
        job_description: jobDescription,
      });
      setSuggestions(res.data.optimized_points || []);
    } catch (err) {
      alert("⚠️ Error contacting the optimization server.");
      console.error(err);
    }

    setLoading(false);
  };

  return (
    <div className="min-h-screen px-4 py-8 bg-gray-50 text-gray-800">
      <div className="max-w-2xl mx-auto bg-white rounded-lg shadow-md p-6">
        <h1 className="text-3xl font-bold mb-6 text-center text-blue-700">
          🤖 BART Resume Optimizer
        </h1>

        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Job Title</label>
            <input
              type="text"
              className="w-full border border-gray-300 rounded px-3 py-2"
              value={jobTitle}
              onChange={(e) => setJobTitle(e.target.value)}
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Job Description (Optional)</label>
            <textarea
              className="w-full border border-gray-300 rounded px-3 py-2"
              rows="4"
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              placeholder="Paste the job description here..."
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Resume Bullet Points</label>
            <textarea
              className="w-full border border-gray-300 rounded px-3 py-2"
              rows="6"
              value={resumePoints}
              onChange={(e) => setResumePoints(e.target.value)}
              placeholder="Paste multiple points separated by new lines"
              required
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className={`w-full text-white font-semibold py-2 px-4 rounded transition duration-200 ${
              loading ? "bg-blue-300 cursor-not-allowed" : "bg-blue-600 hover:bg-blue-700"
            }`}
          >
            {loading ? "Optimizing..." : "🚀 Optimize Resume"}
          </button>
        </form>

        {suggestions.length > 0 && (
          <div className="mt-8">
            <h2 className="text-lg font-semibold mb-4 text-green-700">
              ✅ Optimized Suggestions
            </h2>
            <div className="space-y-4">
              {suggestions.map((group, idx) => (
                <div key={idx} className="border p-3 bg-gray-50 rounded shadow-sm">
                  <p className="font-semibold mb-2 text-blue-700">🔹 Original:</p>
                  <p className="mb-2 text-sm">{group.original}</p>
                  <p className="font-semibold text-green-700 mb-1">✨ Suggestions:</p>
                  <ul className="list-disc list-inside text-sm text-gray-700 space-y-1">
                    {group.suggestions.map((opt, i) => (
                      <li key={i}>{opt}</li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default BartForm;