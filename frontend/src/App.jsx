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
      const response = await axios.post(
        BACKEND_URL+"/analyze",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
      setAnalysisResult(response.data);
    } catch (err) {
      setError(err.response?.data?.error || "An unexpected error occurred.");
    } finally {
      setIsLoading(false);
    }
  };

  // Helper to determine score color
  const getScoreColor = (score) => {
    if (score >= 85) return "text-green-600";
    if (score >= 70) return "text-yellow-600";
    return "text-red-600";
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col justify-center items-center p-4">
      <div className="w-full max-w-5xl bg-white rounded-xl shadow-lg p-8 space-y-8">
        {/* Header */}
        <div className="text-center">
          <h1 className="text-4xl font-bold text-gray-800">
            AI Agent Resume Analyzer
          </h1>
          <p className="text-gray-600 mt-2">
            Get an intelligent, in-depth analysis of your resume against any job
            description.
          </p>
        </div>

        {/* Form */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className="space-y-4">
            <div>
              <label
                htmlFor="resume"
                className="block text-sm font-medium text-gray-700 mb-1"
              >
                📄 1. Upload Resume (PDF)
              </label>
              <input
                id="resume"
                type="file"
                accept=".pdf"
                onChange={handleFileChange}
                className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100"
                required
              />
            </div>
            <div>
              <label
                htmlFor="job-description"
                className="block text-sm font-medium text-gray-700 mb-1"
              >
                📋 2. Paste Job Description
              </label>
              <textarea
                id="job-description"
                rows="10"
                className="mt-1 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
                placeholder="Paste the full job description here..."
                value={jobDescription}
                // --- THIS IS THE FIX ---
                onChange={(e) => setJobDescription(e.target.value)}
                required
              />
            </div>
          </div>
          <div className="flex flex-col items-center justify-center bg-indigo-50 rounded-lg p-8">
            <h2 className="text-xl font-semibold text-gray-800">
              Ready for Analysis?
            </h2>
            <p className="text-gray-600 mt-2 mb-4 text-center">
              Our AI agent will provide a detailed breakdown.
            </p>
            <button
              onClick={handleSubmit}
              disabled={isLoading || !resumeFile || !jobDescription}
              className="w-full inline-flex justify-center py-3 px-6 border border-transparent shadow-sm text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:bg-gray-400 disabled:cursor-not-allowed"
            >
              {isLoading ? "🤖 Agent is thinking..." : "Analyze Now"}
            </button>
          </div>
        </div>

        {/* Error Message */}
        {error && (
          <div className="mt-6 p-4 bg-red-100 border-l-4 border-red-500 text-red-700">
            <p>{error}</p>
          </div>
        )}

        {/* Loading Spinner */}
        {isLoading && (
          <div className="text-center p-8">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">
              Analyzing... This may take up to 30 seconds.
            </p>
          </div>
        )}

        {/* Results */}
        {analysisResult && (
          <div className="pt-8 border-t border-gray-200">
            <h2 className="text-3xl font-bold text-gray-800 text-center mb-6">
              Analysis Report
            </h2>
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Score & Summary */}
              {/* Score & Summary */}
              <div className="lg:col-span-1 bg-gray-50 p-6 rounded-lg">
                <h3 className="text-lg font-semibold text-gray-700">
                  Match Score
                </h3>
                <p
                  className={`text-7xl font-bold my-2 ${getScoreColor(
                    analysisResult.matchScore
                  )}`}
                >
                  {analysisResult.matchScore}
                  <span className="text-3xl text-gray-500">%</span>
                </p>

                <div className="mt-4 space-y-1 text-sm text-gray-600">
                  <p>
                    <span className="font-medium text-gray-700">
                      Skills Match:
                    </span>{" "}
                    {analysisResult.skillsMatchPercent}%
                  </p>
                  <p>
                    <span className="font-medium text-gray-700">
                      Experience Match:
                    </span>{" "}
                    {analysisResult.experienceMatchPercent}%
                  </p>
                  <p>
                    <span className="font-medium text-gray-700">
                      Keyword Match:
                    </span>{" "}
                    {analysisResult.keywordMatchPercent}%
                  </p>
                </div>

                <h3 className="text-lg font-semibold text-gray-700 mt-6">
                  Summary
                </h3>
                <p className="text-gray-600 text-sm mt-1">
                  {analysisResult.summary}
                </p>
              </div>

              {/* Strengths & Improvements */}
              <div className="lg:col-span-2 space-y-6">
                <div className="bg-green-50 p-6 rounded-lg border border-green-200">
                  <h3 className="text-xl font-semibold text-green-800 mb-3">
                    ✅ Strengths
                  </h3>
                  <ul className="list-disc list-inside space-y-2 text-green-700">
                    {analysisResult.strengths.map((item, index) => (
                      <li key={index}>{item}</li>
                    ))}
                  </ul>
                </div>
                <div className="bg-red-50 p-6 rounded-lg border border-red-200">
                  <h3 className="text-xl font-semibold text-red-800 mb-3">
                    🔍 Areas for Improvement
                  </h3>
                  <ul className="list-disc list-inside space-y-2 text-red-700">
                    {analysisResult.areasForImprovement.map((item, index) => (
                      <li key={index}>{item}</li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
