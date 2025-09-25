# Simple Docker build for DevOps Automation Hub
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy Python requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Python source code
COPY src/ ./src/

# Copy the demo HTML as a simple frontend
COPY demo.html ./static/index.html

# Create logs directory
RUN mkdir -p logs

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash devops
RUN chown -R devops:devops /app
USER devops

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/api/health || exit 1

# Set environment variables
ENV PYTHONPATH=/app/src
ENV FLASK_ENV=development

# Start the application
CMD ["python", "src/main.py"]
