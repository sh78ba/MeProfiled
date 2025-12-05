# 🤖 MeProfiled – AI-Powered Resume Analyzer

An intelligent, production-ready resume analysis tool that uses BERT NLP to evaluate how well your resume matches a job description. Get detailed insights, personalized recommendations, and experience-level specific analysis.

🔗 **Live App**: [https://me-profiled-frontend.vercel.app](https://me-profiled-frontend.vercel.app)

---

## ✨ Features

### 🎯 Smart Analysis
- 📄 **PDF Resume Upload** with validation (max 16MB)
- 📝 **Job Description Matching** using BERT embeddings
- 🤖 **AI-Powered Insights** with semantic similarity analysis
- 📊 **Detailed Match Scores** (Skills, Experience, Keywords)
- 💼 **Experience Level Detection** (Intern, Fresher, Experienced)

### 🚀 Production Ready
- ⚡ **Fast Processing** with model caching (3-8 seconds)
- 🔒 **Secure** with file validation and input sanitization
- 📈 **Scalable** with optimized BERT inference
- 🎨 **Responsive UI** with real-time validation
- 🔍 **Comprehensive Logging** and health monitoring

### 📊 Analysis Breakdown
- **Match Score**: Overall compatibility (0-100%)
- **Skills Match**: Technical and soft skills alignment
- **Experience Match**: Work history relevance
- **Keyword Match**: Job-specific terminology coverage
- **Strengths**: What you're doing well
- **Areas for Improvement**: Actionable recommendations

---

## 📸 Demo

![MeProfiled Demo](/images/s.png)

> *Smart resume analysis with experience-level specific recommendations*

---

## 🛠️ Tech Stack

### Frontend
- ⚛️ **React 18** with Vite
- 🎨 **Bootstrap 5** for UI components
- 📡 **Axios** for API communication
- ✅ **Real-time Validation** and error handling
- 🌐 **Environment-based Configuration**

### Backend
- 🐍 **Python 3.11** with Flask
- 🤗 **Transformers** (BERT base-uncased)
- 🧠 **PyTorch** for model inference
- 📄 **PyPDF2** for PDF text extraction
- 🔧 **Scikit-learn** for cosine similarity
- 📊 **Structured Logging** with monitoring
- 🔒 **Security** with CORS and validation

### Infrastructure
- 🚀 **Vercel** (Frontend)
- 🚂 **Railway/Render** (Backend - recommended)
- 🐳 **Docker** support included
- ⚙️ **Gunicorn** for production server
- 📦 **LRU Caching** for performance

---

## 📦 Installation & Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- pip & npm

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Run development server
python app.py

# Or run with gunicorn (production)
gunicorn app:app --workers 2 --timeout 120
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
cp .env.local.example .env.local

# Run development server
npm run dev

# Build for production
npm run build
```

---

## 🚀 Production Deployment

See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed deployment instructions including:
- Railway deployment (recommended for ML models)
- Render deployment
- Docker deployment
- Vercel deployment
- Environment configuration
- Performance optimization tips

### Quick Deploy

**Backend (Railway):**
```bash
railway login
railway init
railway up
```

**Frontend (Vercel):**
```bash
vercel --prod
```

---

## 📡 API Endpoints

### `POST /analyze`
Analyze resume against job description

**Request:**
```bash
curl -X POST http://localhost:5001/analyze \
  -F "resume=@resume.pdf" \
  -F "jobDescription=Your job description here..." \
  -F "experienceLevel=auto"
```

**Response:**
```json
{
  "matchScore": 78,
  "skillsMatchPercent": 82,
  "experienceMatchPercent": 75,
  "keywordMatchPercent": 70,
  "experienceLevel": "fresher",
  "summary": "Moderate match with 78% overall compatibility...",
  "strengths": ["Strong technical skills alignment..."],
  "areasForImprovement": ["Enhance experience section..."],
  "processingTime": 4.23
}
```

### `GET /health`
Health check endpoint

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-12-05T10:30:00",
  "model_loaded": true
}
```

---

## 🎯 Key Features Explained

### Experience-Level Adaptive Scoring

The system automatically detects and adjusts scoring based on candidate level:

| Level | Skills Weight | Experience Weight | Keywords Weight |
|-------|---------------|-------------------|-----------------|
| Intern | 60% | 20% | 20% |
| Fresher | 55% | 30% | 15% |
| Experienced | 50% | 40% | 10% |

### BERT-Based Semantic Analysis

- Uses `bert-base-uncased` for text embeddings
- Cosine similarity for semantic matching
- Keyword extraction with stop word filtering
- Combines semantic understanding with keyword matching

### Production Optimizations

- **Lazy Loading**: Model loads on first request
- **Caching**: LRU cache for embeddings (128 items)
- **Validation**: Comprehensive input validation
- **Error Handling**: Graceful error messages
- **Monitoring**: Structured logging with timestamps
- **Security**: File size limits, type validation, CORS

---

## 🔧 Configuration

### Backend Environment Variables

```bash
FLASK_ENV=production
PORT=5001
ALLOWED_ORIGINS=https://your-frontend.vercel.app
LOG_LEVEL=INFO
```

### Frontend Environment Variables

```bash
VITE_BACKEND_URL=https://your-backend.railway.app
```

---

## 📊 Performance Metrics

- **Cold Start**: ~10-15 seconds (model loading)
- **Warm Requests**: 3-8 seconds per analysis
- **Memory Usage**: ~500MB (BERT model)
- **Max File Size**: 16MB
- **Concurrent Requests**: 2-4 workers

---

## 🐛 Troubleshooting

**Model Loading Issues:**
```bash
python -c "from transformers import AutoTokenizer, AutoModel; \
    AutoTokenizer.from_pretrained('bert-base-uncased'); \
    AutoModel.from_pretrained('bert-base-uncased')"
```

**Timeout Issues:**
- Increase timeout in `gunicorn` or frontend axios config
- Check network connectivity
- Monitor server resources

**PDF Extraction Issues:**
- Ensure PDF contains selectable text (not scanned images)
- Check file is not encrypted
- Verify file size is under 16MB

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📄 License

MIT License - feel free to use this project for personal or commercial purposes.

---

## 👨‍💻 Author

**Shantanu Basumatary**
- GitHub: [@sh78ba](https://github.com/sh78ba)
- Project: [MeProfiled](https://github.com/sh78ba/MeProfiled)

---

## 🙏 Acknowledgments

- Built with [BERT](https://huggingface.co/bert-base-uncased) from Hugging Face
- UI components from [Bootstrap](https://getbootstrap.com/)
- Deployed on [Vercel](https://vercel.com/) and [Railway](https://railway.app/)

---

Made with ❤️ for job seekers worldwide

