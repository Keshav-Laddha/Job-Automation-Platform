import React, { useEffect, useState } from "react";
import axios from "axios";

const InterviewQuestions = () => {
  const [questions, setQuestions] = useState([]);
  const [search, setSearch] = useState("");
  const [openIndex, setOpenIndex] = useState(null);

  useEffect(() => {
    const fetchQuestions = async () => {
      try {
        const res = await axios.get(`${process.env.REACT_APP_API_URL}/interview_questions`);
        setQuestions(res.data);
      } catch (err) {
        setQuestions([]);
      }
    };
    fetchQuestions();
  }, []);

  const filtered = questions.filter(q =>
    q.question.toLowerCase().includes(search.toLowerCase()) ||
    q.companies.some(c => c.toLowerCase().includes(search.toLowerCase()))
  );

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
      {filtered.length === 0 ? (
        <div className="text-center text-gray-500">No interview questions found.</div>
      ) : (
        <div className="space-y-4">
          {filtered.map((q, idx) => (
            <div key={idx} className="bg-white rounded-lg shadow border p-4">
              <div
                className="flex justify-between items-center cursor-pointer"
                onClick={() => setOpenIndex(openIndex === idx ? null : idx)}
              >
                <span className="font-semibold text-lg text-blue-800">{q.question}</span>
                <span className="text-gray-400 text-xl">{openIndex === idx ? "▲" : "▼"}</span>
              </div>
              {openIndex === idx && (
                <div className="mt-3">
                  <div className="mb-2 text-gray-700">
                    <span className="font-semibold">Description: </span>
                    {q.description}
                  </div>
                  <div className="flex flex-wrap gap-2 mb-2">
                    {q.companies.map((company, i) => (
                      <span key={i} className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-xs font-semibold">
                        {company}
                      </span>
                    ))}
                  </div>
                  {q.ctc_offered && q.ctc_offered.length > 0 && (
                    <div className="text-sm text-gray-500 mb-1">
                      <span className="font-semibold">CTC Offered: </span>
                      {q.ctc_offered.join(", ")}
                    </div>
                  )}
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