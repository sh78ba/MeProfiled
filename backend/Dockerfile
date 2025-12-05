FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1 \
    TRANSFORMERS_CACHE=/tmp/transformers \
    HF_HOME=/tmp/huggingface \
    PATH=/root/.local/bin:$PATH

EXPOSE 5001

CMD ["gunicorn", "--bind", "0.0.0.0:5001", "--workers", "1", "--threads", "2", "--timeout", "120", "app:app"]
