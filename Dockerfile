# Dockerfile for Streamlit App
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies for PyAudio
RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    python3-pyaudio \
    && rm -rf /var/lib/apt/lists/*

COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "app/main.py", "--server.port=8501", "--server.enableCORS=false"]
