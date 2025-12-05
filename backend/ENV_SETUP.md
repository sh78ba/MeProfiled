# Environment Configuration for Render

## Setting Environment Variables on Render:

1. Go to your Render dashboard
2. Select your web service (meprofile-backend)
3. Go to **Environment** tab
4. Add/Update these variables:

### Required Variables:

```
FLASK_ENV=production
PYTHON_VERSION=3.11.0
ALLOWED_ORIGINS=http://localhost:5173,https://your-frontend.vercel.app
TRANSFORMERS_CACHE=/tmp/transformers
HF_HOME=/tmp/huggingface
```

### Update ALLOWED_ORIGINS:
Replace `https://your-frontend.vercel.app` with your actual Vercel frontend URL.

You can add multiple origins separated by commas:
```
ALLOWED_ORIGINS=http://localhost:5173,https://app1.vercel.app,https://app2.vercel.app
```

## After Changing Variables:
Render will automatically redeploy your service.
