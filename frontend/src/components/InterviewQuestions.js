import React, { useEffect, useState } from "react";
import axios from "axios";
import { useToast } from "./Toast";

const InterviewQuestions = ({ jobId, company }) => {
  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [newQuestion, setNewQuestion] = useState("");
  const [newDescription, setNewDescription] = useState("");
  const [showModal, setShowModal] = useState(false);
  const toast = useToast();

  useEffect(() => {
    fetchQuestions();
    // eslint-disable-next-line
  }, [jobId]);

  const fetchQuestions = async () => {
    setLoading(true);
    try {
      const res = await axios.get(`${process.env.REACT_APP_API_URL}/interview_questions?job_id=${jobId}`);
      setQuestions(res.data);
    } catch (err) {
      setQuestions([]);
    } finally {
      setLoading(false);
    }
  };

  const addQuestion = async (e) => {
    e.preventDefault();
    if (!newQuestion.trim()) return;
    try {
      await axios.post(`${process.env.REACT_APP_API_URL}/interview_questions`, {
        job_id: jobId,
        company,
        question: newQuestion,
        description: newDescription
      });
      setNewQuestion("");
      setNewDescription("");
      setShowModal(false);
      fetchQuestions();
      toast.showToast("Question added!", "success");
    } catch (err) {
      toast.showToast("Error adding question", "error");
    }
  };

  const deleteQuestion = async (id) => {
    try {
      await axios.delete(`${process.env.REACT_APP_API_URL}/interview_questions/${id}`);
      fetchQuestions();
      toast.showToast("Question deleted!", "success");
    } catch (err) {
      toast.showToast("Error deleting question", "error");
    }
  };

  return (
    <div className="bg-gray-50 rounded p-4 border mt-2">
      <div className="flex justify-between items-center mb-2">
        <h3 className="font-semibold text-blue-700">Interview Questions</h3>
        <button
          onClick={() => setShowModal(true)}
          className="bg-blue-600 text-white px-3 py-1 rounded hover:bg-blue-700 text-sm"
        >
          + Add
        </button>
      </div>
      {loading ? (
        <div className="text-gray-400 text-sm">Loading...</div>
      ) : questions.length === 0 ? (
        <div className="text-gray-400 text-sm">No questions yet.</div>
      ) : (
        <ul className="divide-y divide-gray-200">
          {questions.map(q => (
            <li key={q.id} className="py-2 flex justify-between items-center">
              <div>
                <span className="font-medium text-gray-800">{q.question}</span>
                {q.description && (
                  <span className="ml-2 text-xs bg-yellow-100 text-yellow-700 px-2 py-0.5 rounded">Desc: {q.description}</span>
                )}
                <span className="ml-2 text-xs text-gray-500">{q.asked_at ? new Date(q.asked_at).toLocaleDateString() : ""}</span>
              </div>
              <button
                onClick={() => deleteQuestion(q.id)}
                className="text-red-500 hover:text-red-700 text-xs"
              >
                Delete
              </button>
            </li>
          ))}
        </ul>
      )}
      {/* Modal for adding question */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-30 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg shadow-lg p-6 w-full max-w-md">
            <h4 className="font-semibold mb-3 text-blue-700">Add Interview Question</h4>
            <form onSubmit={addQuestion} className="flex flex-col gap-3">
              <input
                type="text"
                placeholder="Interview question..."
                value={newQuestion}
                onChange={e => setNewQuestion(e.target.value)}
                className="border rounded px-2 py-1"
                required
              />
              <input
                type="text"
                placeholder="Description (optional)"
                value={newDescription}
                onChange={e => setNewDescription(e.target.value)}
                className="border rounded px-2 py-1"
              />
              <div className="flex gap-2 mt-2">
                <button
                  type="submit"
                  className="bg-blue-600 text-white px-4 py-1 rounded hover:bg-blue-700"
                >
                  Add
                </button>
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="bg-gray-300 text-gray-800 px-4 py-1 rounded hover:bg-gray-400"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default InterviewQuestions; 