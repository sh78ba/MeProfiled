# MeProfiled - AI Resume Analyzer 🚀

An advanced AI-powered resume analysis tool that intelligently matches resumes with job descriptions using state-of-the-art NLP models, providing detailed insights and actionable feedback.

## 🌟 Live Demo

- **Frontend**: [https://me-profiled-frontend.vercel.app](https://me-profiled-frontend.vercel.app)
- **Backend API**: [https://sh78ba-meprofiled-backend.hf.space](https://sh78ba-meprofiled-backend.hf.space)

## ✨ Features

- **📄 PDF Resume Upload** - Supports PDF files up to 16MB
- **🤖 Advanced NLP Analysis** - Semantic matching using all-mpnet-base-v2 (420MB model)
- **📊 Comprehensive Scoring** - Skills, Experience, and Keyword analysis with weighted scoring
- **👥 Experience Level Detection** - Auto-detects intern/fresher/experienced profiles
- **💡 Personalized Feedback** - Detailed strengths and improvement suggestions
- **⚡ High Performance** - 2 workers, 4 threads, optimized for 16GB RAM
- **🎯 Production-Grade** - Deployed on Hugging Face Spaces with 16GB RAM

## 🛠 Tech Stack

### Frontend
- **React 18** with Vite for blazing-fast development
- **Bootstrap 5** for responsive UI
- **Axios** for API communication
- **Environment-based** configuration
- **Deployed on**: Vercel

### Backend
- **Flask 3.0.0** - Python web framework
- **Sentence Transformers** - all-mpnet-base-v2 (state-of-the-art)
- **PyTorch 2.0.1** - Deep learning framework
- **scikit-learn 1.3.2** - ML utilities
- **PyPDF2** - PDF text extraction
- **Gunicorn** - Production WSGI server
- **Deployed on**: Hugging Face Spaces (Docker)

### NLP/AI Model
- **Model**: `sentence-transformers/all-mpnet-base-v2`
- **Size**: 420MB (production-grade)
- **Embedding Dimension**: 768
- **Max Sequence Length**: 512 tokens
- **Max Text Length**: 5000 characters
- **Capabilities**: 
  - Advanced semantic similarity
  - Enhanced keyword extraction with bigrams
  - Context-aware scoring
  - Multi-lingual support

## 📁 Project Structure

```
MeProfiled/
├── backend/
│   ├── app.py              # Flask application entry point
│   ├── config.py           # Configuration with model settings
│   ├── models.py           # NLP model management & caching
│   ├── routes.py           # API endpoints (/analyze, /health)
│   ├── requirements.txt    # Python dependencies
│   ├── Dockerfile          # Docker configuration for HF Spaces
│   ├── README.md           # HF Spaces metadata
│   ├── .env.example        # Environment variables template
│   ├── services/
│   │   └── analyzer.py     # Resume analysis logic & scoring
│   └── utils/
│       ├── pdf_utils.py    # PDF processing & text extraction
│       └── text_utils.py   # Keyword extraction & NLP utils
└── frontend/
    ├── src/
    │   ├── App.jsx         # Main React component
    │   ├── config.js       # Backend URL & model config
    │   └── constant.js     # Constants
    ├── package.json        # Node dependencies
    ├── vercel.json         # Vercel deployment config
    └── .env.example        # Environment template
```

## 🚀 Deployment

### Backend (Hugging Face Spaces)
**Deployed at**: https://sh78ba-meprofiled-backend.hf.space

**Configuration**:
- SDK: Docker
- RAM: 16GB (free tier)
- Workers: 2
- Threads per worker: 4
- Timeout: 300 seconds
- Max requests per worker: 100

**Key Files**:
- `Dockerfile` - Container configuration
- `README.md` - HF Spaces metadata (sdk: docker, app_port: 7860)
- Environment: Production-optimized with model caching

### Frontend (Vercel)
**Deployed at**: https://me-profiled-frontend.vercel.app

**Configuration**:
- Framework: Vite
- Auto-deploy: Enabled on push to main
- Environment: `VITE_BACKEND_URL` set to HF Spaces URL

## 🛠 Local Development Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- 4GB+ RAM (for model loading)

### Backend Setup

```bash
cd backend

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env:
# ALLOWED_ORIGINS=http://localhost:5173,https://your-frontend.vercel.app
# PORT=5001

# Run development server
python app.py
```

**First run**: Model download (~420MB) takes 1-2 minutes

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
echo "VITE_BACKEND_URL=http://localhost:5001" > .env

# Run development server
npm run dev
```

Frontend will be available at http://localhost:5173

## 🔌 API Endpoints

### Base URL
- **Production**: https://sh78ba-meprofiled-backend.hf.space
- **Local**: http://localhost:5001

### Endpoints

#### `GET /`
Welcome message and API info
```json
{
  "message": "Hello from Backend"
}
```

#### `GET /health`
Health check with model status
```json
{
  "status": "healthy",
  "model_loaded": true,
  "timestamp": "2025-12-06T00:00:00.000000"
}
```

#### `POST /analyze`
Analyze resume against job description

**Request** (multipart/form-data):
```
resume: PDF file (max 16MB)
jobDescription: string (50-10000 chars)
experienceLevel: 'auto' | 'intern' | 'fresher' | 'experienced'
```

**Response**:
```json
{
  "success": true,
  "matchScore": 85.5,
  "experienceLevel": "fresher",
  "skillsMatchPercent": 88,
  "experienceMatchPercent": 82,
  "keywordMatchPercent": 86,
  "summary": "Strong match...",
  "strengths": ["..."],
  "areasForImprovement": ["..."],
  "matchedKeywords": ["..."],
  "missingKeywords": ["..."],
  "timestamp": "...",
  "processingTime": 1.23
}
```

## 🧠 How It Works

1. **📤 Upload Resume** - User uploads PDF resume (max 16MB) and enters job description (50-10,000 chars)
2. **📝 Text Extraction** - PyPDF2 extracts and cleans text from PDF
3. **🔤 Tokenization** - Text preprocessed and chunked (max 5000 chars, 512 tokens)
4. **🎯 Embeddings** - all-mpnet-base-v2 generates 768-dimensional semantic embeddings
5. **📐 Similarity** - Cosine similarity calculates semantic match between resume and JD
6. **🔑 Keywords** - Enhanced extraction with bigrams, tech terms, and partial matching
7. **⚖️ Weighted Scoring** - Multi-factor algorithm:
   - Semantic similarity (50%)
   - Keyword matching (30%)
   - Experience alignment (20%)
8. **📊 Score Normalization** - Sigmoid function for realistic ranges (30-95%)
9. **💬 Analysis Generation** - AI generates personalized feedback and recommendations
10. **✅ Response** - Detailed JSON response with scores, insights, and suggestions

## 🎯 Key Features Implementation

### Experience Detection
Pattern matching for career level identification:
- **Intern**: Keywords like "intern", "student", no experience years
- **Fresher**: 0-2 years experience, entry-level terms
- **Experienced**: 3+ years, senior/lead titles, management experience

### Adaptive Scoring
Different weight distributions per experience level:
- **Intern**: Skills (40%), Projects (30%), Keywords (30%)
- **Fresher**: Skills (50%), Experience (20%), Keywords (30%)
- **Experienced**: Experience (40%), Skills (30%), Leadership (30%)

### Score Boosting
Sigmoid function for realistic score ranges:
- Prevents extreme scores (0% or 100%)
- Typical range: 30-95%
- Balanced distribution around 60-80%

### Advanced Keyword Matching
- **Bigrams**: Two-word phrases (e.g., "machine learning")
- **Partial matching**: Fuzzy matching for similar terms
- **Tech term detection**: Programming languages, frameworks, tools
- **Synonym handling**: Alternative terms (e.g., "JS" vs "JavaScript")

### Model Optimization
- **LRU Cache**: Embeddings cached (32 entries) for performance
- **Lazy Loading**: Model loaded on first request
- **Memory Management**: `gc.collect()` after analysis
- **Multi-threading**: 2 workers × 4 threads = 8 concurrent requests

## 📊 Performance Metrics

- **Analysis Time**: 30-60 seconds per resume (with cold start)
- **Subsequent Requests**: 5-15 seconds (model cached)
- **Model Size**: 420MB (all-mpnet-base-v2)
- **Accuracy**: State-of-the-art semantic similarity
- **Concurrency**: 8 simultaneous requests (2 workers × 4 threads)
- **Max File Size**: 16MB PDF
- **Max Job Description**: 10,000 characters

## 🔐 Environment Variables

### Backend (.env)
```env
FLASK_ENV=production
PORT=7860
ALLOWED_ORIGINS=https://me-profiled-frontend.vercel.app,http://localhost:5173
MODEL_NAME=sentence-transformers/all-mpnet-base-v2
LOG_LEVEL=INFO
```

### Frontend (.env)
```env
VITE_BACKEND_URL=https://sh78ba-meprofiled-backend.hf.space
```

## 🐛 Troubleshooting

### Backend Issues

**Model loading slow on first request**
- First request takes 30-45 seconds to download model
- Subsequent requests are much faster (model cached)

**Memory errors**
- Ensure 4GB+ RAM available
- Model requires ~1.5GB loaded in memory

**CORS errors**
- Add frontend URL to `ALLOWED_ORIGINS` in backend `.env`
- Check Hugging Face Spaces environment variables

### Frontend Issues

**Connection errors**
- Verify `VITE_BACKEND_URL` is correct
- Check if backend is running (visit `/health` endpoint)
- First request may timeout (backend starting up)

**File upload fails**
- Ensure PDF is under 16MB
- Check file is valid PDF format

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

MIT License - see LICENSE file for details

## 👨‍💻 Author

**Shantanu Basumatary**
- GitHub: [@sh78ba](https://github.com/sh78ba)
- Project: [MeProfiled](https://github.com/sh78ba/MeProfiled)

## 🙏 Acknowledgments

- **Hugging Face** for free Spaces hosting
- **Sentence Transformers** for the all-mpnet-base-v2 model
- **Vercel** for frontend hosting
- Open source community for amazing tools and libraries

---

Made with ❤️ by Shantanu • Empowering your job hunt with AI insights
