# MeProfiled - Project Documentation

Quick reference guide for all project files with essential information only.

---

## Backend Files

### README.md
Project documentation with overview, features, tech stack (React, Flask, OpenAI API), and live deployment link.

---

### backend/app.py
**Purpose:** Flask REST API that analyzes resume-job description matches using OpenAI GPT-3.5-turbo via LangChain.

**Key Functions:**
- `extract_text_from_pdf(pdf_file)` - Extracts text from PDF using PyPDF2
- `analyze_resume()` - POST endpoint that processes analysis requests

**How It Works:**
1. Receives resume PDF + job description text
2. Extracts text from PDF
3. Sends to OpenAI GPT-3.5-turbo with weighted prompt (Skills 50%, Experience 40%, Keywords 10%)
4. Returns JSON with match score (0-100), strengths, and improvement areas

**Libraries:** Flask, flask-cors, PyPDF2, langchain, langchain-openai, python-dotenv

**Environment:** Requires `OPENAI_API_KEY`

**Limitations:** Image-based PDFs fail (no OCR), serverless timeout limits apply

---

### backend/requirements.txt
Python packages: Flask, Flask-Cors, PyPDF2, langchain, langchain-openai, python-dotenv

**Note:** No version pinning - should pin versions for production

---

### backend/vercel.json
Vercel serverless deployment config - routes all requests to app.py using @vercel/python runtime.

---

## Frontend Files

### frontend/package.json
NPM config with React 19, Vite 7, Tailwind CSS 4, Bootstrap 5, Axios, ESLint.

**Scripts:** `dev`, `build`, `lint`, `preview`

---

### frontend/vite.config.js
Minimal Vite config with React plugin for JSX transformation and HMR (Hot Module Replacement).

---

### frontend/eslint.config.js
ESLint config with React Hooks rules, Fast Refresh compliance, and ES2020 support.

**Custom rule:** Allows unused uppercase variables (e.g., `BACKEND_URL`).

---

### frontend/index.html
HTML entry point - loads favicons, PWA manifest, and mounts React app to `#root` div.

---

### frontend/vercel.json
SPA deployment config - rewrites all routes to `/` for client-side routing.

---

### frontend/src/main.jsx
React entry point - renders `<App />` with StrictMode and imports Bootstrap CSS globally.

---

### frontend/src/App.jsx
**Purpose:** Main React component for resume analysis UI.

**Key Features:**
- File upload for resume PDF
- Textarea for job description
- API call to backend `/analyze` endpoint
- Displays match score with color coding (Green ≥85%, Yellow 70-84%, Red <70%)
- Shows strengths and improvement areas

**State:** resumeFile, jobDescription, analysisResult, isLoading, error

**Libraries:** React (useState), Axios, Bootstrap

**Limitations:** No file size validation, no result caching, loading blocks UI

---

### frontend/src/App.css
Empty file (can be removed).

---

### frontend/src/constant.js
Exports `BACKEND_URL` from environment variable `VITE_BACKEND_URL`.

---

### frontend/src/index.css
Imports Tailwind CSS v4 utilities globally.

**Note:** Bootstrap also imported - potential class conflicts

---

### frontend/public/about.txt
Attribution for "Cookie" font used in favicon.

---

### frontend/public/site.webmanifest
PWA manifest with app icons and standalone display mode.

**Note:** Missing name/description fields

---

## 📊 Project Architecture

**Stack:**
- **Frontend:** React 19 + Vite 7 + Tailwind/Bootstrap + Axios
- **Backend:** Flask + LangChain + OpenAI GPT-3.5-turbo + PyPDF2
- **Deployment:** Vercel serverless (both frontend and backend)

**Data Flow:**
```
User uploads PDF + JD text → Frontend (App.jsx)
    ↓ Axios POST
Backend (app.py) extracts PDF text → LangChain prompt → OpenAI API
    ↓ JSON response
Frontend displays: match score (0-100) + strengths + improvements
```

**Critical Config:**
- `OPENAI_API_KEY` - Backend environment variable
- `VITE_BACKEND_URL` - Frontend environment variable

**Key Improvements Needed:**
1. Pin dependency versions (requirements.txt)
2. Add OCR support for image PDFs
3. Remove duplicate CSS frameworks (Tailwind vs Bootstrap)
4. Add result caching
5. Complete PWA manifest
6. Add file validation

---

*MeProfiled - AI Resume Analyzer by Shantanu*
