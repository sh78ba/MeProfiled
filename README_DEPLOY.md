# Deploy to Render

## Quick Setup

1. Go to [render.com](https://render.com) and sign up with GitHub
2. Click **"New +"** → **"Web Service"**
3. Connect repository: **sh78ba/MeProfiled**
4. Configure:
   - **Name**: `meprofile-backend`
   - **Root Directory**: `backend`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
5. Add Environment Variables:
   ```
   FLASK_ENV=production
   ALLOWED_ORIGINS=http://localhost:5173,https://your-frontend-url.vercel.app
   TRANSFORMERS_CACHE=/tmp/transformers
   HF_HOME=/tmp/huggingface
   ```
6. Click **"Create Web Service"**

First deployment takes ~5-10 minutes (downloads model). Subsequent deployments are faster.

## Update Frontend

After deployment, copy your Render URL (e.g., `https://meprofile-backend.onrender.com`) and update:

**frontend/src/constant.js**:
```javascript
export const BACKEND_URL = 'https://meprofile-backend.onrender.com';
```

Then redeploy frontend on Vercel.

## Local Testing

```bash
cd backend
source venv/bin/activate
gunicorn app:app --bind 0.0.0.0:5001
```

Visit `http://localhost:5001/health`
