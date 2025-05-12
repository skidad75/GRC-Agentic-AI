
# Dockerfile for Streamlit App
FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir streamlit openai faiss-cpu

EXPOSE 8501

CMD ["streamlit", "run", "app/main.py", "--server.port=8501", "--server.enableCORS=false"]
