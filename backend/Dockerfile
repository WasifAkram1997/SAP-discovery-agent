FROM python:3.11-slim

WORKDIR /app

# Install system dependencies including build tools for Python packages
RUN apt-get update && apt-get install -y \
    postgresql-client \
    build-essential \
    libpq-dev \
    python3-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create logs directory
RUN mkdir -p /app/logs

# Expose port
EXPOSE 8001

# Run application with uvicorn
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8001"]
