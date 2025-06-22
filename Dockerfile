FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY app/ .

# Expose port
EXPOSE 8501

# Default command (can be overridden in docker-compose)
CMD ["streamlit", "run", "main.py", "--server.runOnSave", "true", "--server.port", "8501", "--server.address", "0.0.0.0"] 