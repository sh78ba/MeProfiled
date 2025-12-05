# MeProfiled - AI Resume Analyzer

An AI-powered resume analysis tool that matches resumes with job descriptions using NLP and provides detailed insights.

## Features

- **PDF Resume Upload** - Supports PDF files up to 16MB
- **Job Description Analysis** - Semantic matching using BERT embeddings
- **Match Scoring** - Skills, Experience, and Keyword analysis
- **Experience Level Detection** - Auto-detects intern/fresher/experienced
- **Personalized Feedback** - Strengths and improvement suggestions

## Tech Stack

### Frontend
- React 18 + Vite
- Bootstrap 5
- Axios
- Environment-based config

### Backend
- Flask 3.0.0
- Sentence Transformers (all-MiniLM-L6-v2)
- PyTorch
- scikit-learn
- PyPDF2

### NLP/AI
- BERT-based sentence embeddings
- Cosine similarity matching
- Enhanced keyword extraction with bigrams
- Sigmoid score boosting

## Project Structure

```
MeProfiled/
├── backend/
│   ├── app.py              # Flask application
│   ├── config.py           # Configuration
│   ├── models.py           # BERT model management
│   ├── routes.py           # API endpoints
│   ├── requirements.txt    # Python dependencies
│   ├── services/
│   │   └── analyzer.py     # Resume analysis logic
│   └── utils/
│       ├── pdf_utils.py    # PDF processing
│       └── text_utils.py   # Text extraction & keywords
└── frontend/
    ├── src/
    │   ├── App.jsx         # Main React component
    │   └── constant.js     # Backend URL config
    └── package.json        # Node dependencies
```

## Setup & Installation

### Backend

```bash
cd backend
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env and set ALLOWED_ORIGINS

# Run
python app.py
```

### Frontend

```bash
cd frontend
npm install

# Create .env file
echo "VITE_BACKEND_URL=http://localhost:5001" > .env

# Run
npm run dev
```

## Environment Variables

### Backend (.env)
```
FLASK_ENV=production
PORT=5001
ALLOWED_ORIGINS=http://localhost:5173,https://your-frontend.vercel.app
```

### Frontend (.env)
```
VITE_BACKEND_URL=http://localhost:5001
```

## API Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check
- `POST /analyze` - Analyze resume against job description

## How It Works

1. **Upload Resume** - User uploads PDF resume and enters job description
2. **Text Extraction** - PyPDF2 extracts text from PDF
3. **Embeddings** - BERT model generates embeddings for resume and JD
4. **Similarity** - Cosine similarity calculates semantic match
5. **Keywords** - Enhanced extraction identifies technical terms and phrases
6. **Scoring** - Weighted algorithm computes match scores
7. **Analysis** - Generates personalized feedback and recommendations

## Key Features Implementation

- **Experience Detection**: Pattern matching for intern/fresher/experienced keywords
- **Adaptive Scoring**: Different weight distributions per experience level
- **Score Boosting**: Sigmoid function for realistic score ranges (30-95%)
- **Keyword Matching**: Bigrams, partial matching, tech term detection
- **Model Caching**: LRU cache for embeddings, lazy model loading

## License

MIT
