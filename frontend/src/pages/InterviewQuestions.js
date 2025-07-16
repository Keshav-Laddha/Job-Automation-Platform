import React, { useEffect, useState } from "react";
import axios from "axios";

// Utility to normalize strings for search (case, dot, and space insensitive)
function normalizeString(str) {
  return (str || "").toLowerCase().replace(/\s+/g, "").replace(/\./g, "");
}

const InterviewQuestions = () => {
  const [questions, setQuestions] = useState([]);
  const [search, setSearch] = useState("");
  const [openIndex, setOpenIndex] = useState(null);

  useEffect(() => {
    const fetchQuestions = async () => {
      try {
        const res = await axios.get(`${process.env.REACT_APP_API_URL}/interview_questions`);
        setQuestions(Array.isArray(res.data) ? res.data : []);
      } catch (err) {
        setQuestions([]);
      }
    };
    fetchQuestions();
  }, []);

  const filtered = questions.filter(q =>
    normalizeString(q.question).includes(normalizeString(search)) ||
    (Array.isArray(q.companies) && q.companies.some(c => normalizeString(c).includes(normalizeString(search))))
  );

  // Sort filtered questions by number of companies (descending)
  const sorted = [...filtered].sort((a, b) => {
    const aCount = Array.isArray(a.companies) ? a.companies.length : 0;
    const bCount = Array.isArray(b.companies) ? b.companies.length : 0;
    return bCount - aCount;
  });

  return (
    <div className="max-w-3xl mx-auto py-8 px-4">
      <h1 className="text-3xl font-bold text-center mb-6 text-blue-700">📝 Interview Questions</h1>
      <div className="mb-6 flex justify-center">
        <input
          type="text"
          placeholder="Search questions or companies..."
          value={search}
          onChange={e => setSearch(e.target.value)}
          className="border rounded px-3 py-2 w-full max-w-md"
        />
      </div>
      {sorted.length === 0 ? (
        <div className="text-center text-gray-500">No interview questions found.</div>
      ) : (
        <div className="space-y-4">
          {sorted.map((q, idx) => (
            <div key={q.id} className="bg-white rounded-lg shadow border p-4">
              <div
                className="flex justify-between items-center cursor-pointer"
                onClick={() => setOpenIndex(openIndex === idx ? null : idx)}
              >
                <span className="font-semibold text-lg text-blue-800">{q.question}</span>
                <div className="flex items-center gap-2">
                  {/* Always show link button on right if present */}
                  {q.link && (
                    <a
                      href={q.link}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="ml-2 flex items-center gap-1 px-3 py-1 bg-blue-600 text-white rounded-full shadow-sm font-semibold text-xs transition hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-offset-2"
                      onClick={e => e.stopPropagation()} // Prevent row expand on link click
                      title="Open question link"
                    >
                      <span role="img" aria-label="link">🔗</span> Link
                    </a>
                  )}
                  <span className="text-gray-400 text-xl">{openIndex === idx ? "▲" : "▼"}</span>
                </div>
              </div>
              {openIndex === idx && (
                <div className="mt-3">
                  {q.description && (
                    <div className="mb-2 text-gray-700">
                      <span className="font-semibold">Description: </span>
                      {q.description}
                    </div>
                  )}
                  {Array.isArray(q.companies) && q.companies.length > 0 && (
                    <div className="flex flex-wrap gap-2 mb-2">
                      {q.companies.map((company, i) => (
                        <span key={i} className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-xs font-semibold">
                          {company}
                        </span>
                      ))}
                    </div>
                  )}
                  {/* Link button removed from expanded section */}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default InterviewQuestions; 