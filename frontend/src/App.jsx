import React, { useState } from "react";
import axios from "axios";
import { BACKEND_URL } from "./constant";

function App() {
  const [resumeFile, setResumeFile] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const [analysisResult, setAnalysisResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  const handleFileChange = (e) => {
    setResumeFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!resumeFile || !jobDescription) {
      setError("Please provide both a resume and a job description.");
      return;
    }

    setError("");
    setAnalysisResult(null);
    setIsLoading(true);

    const formData = new FormData();
    formData.append("resume", resumeFile);
    formData.append("jobDescription", jobDescription);

    try {
      const response = await axios.post(`${BACKEND_URL}/analyze`, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      setAnalysisResult(response.data);
    } catch (err) {
      setError(err.response?.data?.error || "An unexpected error occurred.");
    } finally {
      setIsLoading(false);
    }
  };

  const getScoreColor = (score) => {
    if (score >= 85) return "text-success";
    if (score >= 70) return "text-warning";
    return "text-danger";
  };

  return (
    <div className="container py-5">
      <div className="card shadow p-4">
        <div className="text-center mb-4">
          <h1 className="display-5 fw-bold">MeProfiled</h1>
          <p className="text-muted">
            Get an intelligent, in-depth analysis of your resume against any job
            description.
          </p>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="row g-4">
            <div className="col-md-6">
              <div className="mb-3">
                <label htmlFor="resume" className="form-label">
                  📄 1. Upload Resume (PDF)
                </label>
                <input
                  type="file"
                  className="form-control"
                  id="resume"
                  accept=".pdf"
                  onChange={handleFileChange}
                  required
                />
              </div>

              <div className="mb-3">
                <label htmlFor="job-description" className="form-label">
                  📋 2. Paste Job Description
                </label>
                <textarea
                  className="form-control"
                  id="job-description"
                  rows="10"
                  placeholder="Paste the full job description here..."
                  value={jobDescription}
                  onChange={(e) => setJobDescription(e.target.value)}
                  required
                ></textarea>
              </div>
            </div>

            <div className="col-md-6 d-flex flex-column justify-content-center align-items-center bg-light rounded p-4">
              <h4>Ready for Analysis?</h4>
              <p className="text-muted text-center">
                Our AI agent will provide a detailed breakdown.
              </p>
              <button
                type="submit"
                className="btn btn-primary btn-lg w-100 mt-3"
                disabled={isLoading || !resumeFile || !jobDescription}
              >
                {isLoading ? "🤖 Agent is thinking..." : "Analyze Now"}
              </button>
            </div>
          </div>
        </form>

        {error && (
          <div className="alert alert-danger mt-4" role="alert">
            {error}
          </div>
        )}

        {isLoading && (
          <div className="text-center my-5">
            <div className="spinner-border text-primary" role="status"></div>
            <p className="mt-3 text-muted">
              Analyzing... This may take up to 30 seconds.
            </p>
          </div>
        )}

        {analysisResult && (
          <div className="mt-5">
            <h2 className="text-center fw-bold mb-4">Analysis Report</h2>
            <div className="row g-4">
              <div className="col-lg-4">
                <div className="bg-light p-4 rounded shadow-sm h-100">
                  <h5 className="fw-bold">Match Score</h5>
                  <p
                    className={`display-4 fw-bold my-2 ${getScoreColor(
                      analysisResult.matchScore
                    )}`}
                  >
                    {analysisResult.matchScore}
                    <span className="fs-4 text-secondary">%</span>
                  </p>
                  <ul className="list-unstyled mt-3">
                    <li>
                      <strong>Skills Match:</strong>{" "}
                      {analysisResult.skillsMatchPercent}%
                    </li>
                    <li>
                      <strong>Experience Match:</strong>{" "}
                      {analysisResult.experienceMatchPercent}%
                    </li>
                    <li>
                      <strong>Keyword Match:</strong>{" "}
                      {analysisResult.keywordMatchPercent}%
                    </li>
                  </ul>
                  <h6 className="mt-4">Summary</h6>
                  <p className="text-muted">{analysisResult.summary}</p>
                </div>
              </div>

              <div className="col-lg-8">
                <div className="mb-4 p-4 border border-success rounded bg-white">
                  <h5 className="text-success fw-bold mb-3">✅ Strengths</h5>
                  <ul className="list-group list-group-flush">
                    {analysisResult.strengths.map((item, i) => (
                      <li key={i} className="list-group-item">
                        {item}
                      </li>
                    ))}
                  </ul>
                </div>
                <div className="p-4 border border-danger rounded bg-white">
                  <h5 className="text-danger fw-bold mb-3">🔍 Areas for Improvement</h5>
                  <ul className="list-group list-group-flush">
                    {analysisResult.areasForImprovement.map((item, i) => (
                      <li key={i} className="list-group-item">
                        {item}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
      {/* Footer */}
<footer className=" text-center py-4 mt-5 rounded shadow-sm">
  <div className="container">
    <p className="mb-1 fs-5">Made with ❤️ by <strong>Shantanu</strong></p>
    <p className="mb-0 text-secondary">Empowering your job hunt with AI insights</p>
  </div>
</footer>

    </div>
  );
}

export default App;
