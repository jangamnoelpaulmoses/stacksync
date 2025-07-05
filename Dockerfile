# Dockerfile (for Cloud Run, without nsjail)
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Disable nsjail in this build
ENV USE_NSJAIL=false

EXPOSE 8080
CMD ["python3", "app.py"]
