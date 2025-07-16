import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import JobCard from "./components/JobCard";
import BartForm from "./pages/BartForm";
import Analytics from "./pages/Analytics";
import Layout from "./components/Layout";
import AppliedJobs from "./pages/AppliedJobs";
import Dashboard from "./pages/Dashboard";
import InterviewQuestions from "./pages/InterviewQuestions";

const dummyJobs = [
  {
    title: "Software Engineer Intern",
    company: "Google",
    link: "https://careers.google.com/jobs/results/123"
  },
  {
    title: "Backend Developer Intern",
    company: "Microsoft",
    link: "https://careers.microsoft.com/jobs/results/456"
  },
  {
    title: "Full Stack Intern",
    company: "Amazon",
    link: "https://amazon.jobs/en/jobs/789"
  }
];

// Home component is no longer used as default

console.log("API URL:", process.env.REACT_APP_API_URL);

const App = () => (
  <Router>
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Dashboard />} />
        <Route path="form" element={<BartForm />} />
        <Route path="/optimize" element={<BartForm />} />
        <Route path="analytics" element={<Analytics />} />
        <Route path="applied" element={<AppliedJobs />} />
        <Route path="interview-questions" element={<InterviewQuestions />} />
      </Route>
    </Routes>
  </Router>
);

export default App;