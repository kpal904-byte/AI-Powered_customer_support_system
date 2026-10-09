FROM python:3.12-slim

# ---------------------------------------------------------
# Python configuration
# ---------------------------------------------------------

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Hugging Face cache location
ENV HF_HOME=/root/.cache/huggingface


# ---------------------------------------------------------
# Working directory
# ---------------------------------------------------------

WORKDIR /app


# ---------------------------------------------------------
# Install system dependencies
# ---------------------------------------------------------

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*


# ---------------------------------------------------------
# Install Python dependencies
# ---------------------------------------------------------

COPY requirements.txt .

RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


# ---------------------------------------------------------
# Pre-download embedding model
# ---------------------------------------------------------

RUN python -c "\
from sentence_transformers import SentenceTransformer; \
SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')"


# ---------------------------------------------------------
# Copy project
# ---------------------------------------------------------

COPY src ./src
COPY data ./data
COPY models ./models
COPY vector_db ./vector_db


# ---------------------------------------------------------
# Create required directories
# ---------------------------------------------------------

RUN mkdir -p /app/mlruns


# ---------------------------------------------------------
# Expose API port
# ---------------------------------------------------------

EXPOSE 8000


# ---------------------------------------------------------
# Health check
# ---------------------------------------------------------

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health')" || exit 1


# ---------------------------------------------------------
# Start FastAPI
# ---------------------------------------------------------

CMD ["python", "-m", "uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]