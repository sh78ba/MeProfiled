FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1 \
    HF_HOME=/tmp/huggingface \
    MALLOC_TRIM_THRESHOLD_=100000 \
    MALLOC_MMAP_THRESHOLD_=100000

CMD gunicorn --bind 0.0.0.0:${PORT:-5001} --workers 1 --threads 1 --timeout 180 --worker-class sync --max-requests 10 --max-requests-jitter 5 app:app
