import React, { useState } from "react";
import axios from "axios";
import { BACKEND_URL } from "./constant";

function App() {
  const [resumeFile, setResumeFile] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const [experienceLevel, setExperienceLevel] = useState("auto");
  const [analysisResult, setAnalysisResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      // Validate file size (16MB max)
      const maxSize = 16 * 1024 * 1024;
      if (file.size > maxSize) {
        setError("File size must be less than 16MB");
        e.target.value = null;
        return;
      }
      // Validate file type
      if (file.type !== 'application/pdf') {
        setError("Only PDF files are allowed");
        e.target.value = null;
        return;
      }
      setError("");
      setResumeFile(file);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validation
    if (!resumeFile || !jobDescription) {
      setError("Please provide both a resume and a job description.");
      return;
    }

    if (jobDescription.trim().length < 50) {
      setError("Job description must be at least 50 characters long.");
      return;
    }

    if (jobDescription.length > 10000) {
      setError("Job description must be less than 10,000 characters.");
      return;
    }

    setError("");
    setAnalysisResult(null);
    setIsLoading(true);

    const formData = new FormData();
    formData.append("resume", resumeFile);
    formData.append("jobDescription", jobDescription);
    formData.append("experienceLevel", experienceLevel);

    try {
      const response = await axios.post(`${BACKEND_URL}/analyze`, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
        timeout: 120000, // 2 minutes timeout
      });
      setAnalysisResult(response.data);
      
      // Scroll to results
      setTimeout(() => {
        document.getElementById('results')?.scrollIntoView({ behavior: 'smooth' });
      }, 100);
    } catch (err) {
      console.error('Analysis error:', err);
      if (err.code === 'ECONNABORTED') {
        setError("Request timed out. Please try again.");
      } else if (err.response?.status === 413) {
        setError("File is too large. Maximum size is 16MB.");
      } else if (err.response?.status === 503) {
        setError("Service temporarily unavailable. Please try again in a moment.");
      } else {
        setError(err.response?.data?.error || "An unexpected error occurred. Please try again.");
      }
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
                  accept=".pdf,application/pdf"
                  onChange={handleFileChange}
                  required
                />
                <small className="text-muted">
                  {resumeFile ? (
                    <span className="text-success">✓ {resumeFile.name} ({(resumeFile.size / 1024 / 1024).toFixed(2)} MB)</span>
                  ) : (
                    "PDF only, max 16MB"
                  )}
                </small>
              </div>

              <div className="mb-3">
                <label htmlFor="experience-level" className="form-label">
                  👤 2. Select Experience Level
                </label>
                <select
                  className="form-select"
                  id="experience-level"
                  value={experienceLevel}
                  onChange={(e) => setExperienceLevel(e.target.value)}
                >
                  <option value="auto">Auto Detect</option>
                  <option value="intern">Intern</option>
                  <option value="fresher">Fresher (0-2 years)</option>
                  <option value="experienced">Experienced (3+ years)</option>
                </select>
                <small className="text-muted">Select your experience level or let AI detect it automatically</small>
              </div>

              <div className="mb-3">
                <label htmlFor="job-description" className="form-label">
                  📋 3. Paste Job Description
                </label>
                <textarea
                  className="form-control"
                  id="job-description"
                  rows="10"
                  placeholder="Paste the full job description here..."
                  value={jobDescription}
                  onChange={(e) => setJobDescription(e.target.value)}
                  required
                  maxLength={10000}
                ></textarea>
                <small className="text-muted">
                  {jobDescription.length} / 10,000 characters
                  {jobDescription.length > 0 && jobDescription.length < 50 && (
                    <span className="text-danger"> (minimum 50 characters)</span>
                  )}
                </small>
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
          <div className="mt-5" id="results">
            <h2 className="text-center fw-bold mb-4">Analysis Report</h2>
            {analysisResult.processingTime && (
              <p className="text-center text-muted small">
                Analysis completed in {analysisResult.processingTime}s
              </p>
            )}
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
                      <strong>Experience Level:</strong>{" "}
                      <span className="badge bg-info text-dark">
                        {analysisResult.experienceLevel.charAt(0).toUpperCase() + analysisResult.experienceLevel.slice(1)}
                      </span>
                    </li>
                    <li className="mt-2">
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
