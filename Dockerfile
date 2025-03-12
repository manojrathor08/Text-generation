# Use a lightweight Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TRANSFORMERS_CACHE=/app/model_cache

# Create model cache directory (but do NOT store inside the image)
RUN mkdir -p /app/model_cache

# Copy requirements first (to use Docker cache properly)
COPY requirements.txt .

# Install dependencies without caching to reduce size
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose port for the API
EXPOSE 8000

# Preload the model dynamically (instead of storing it in the image)
CMD ["sh", "-c", "python -c 'from transformers import pipeline; pipeline(\"text-generation\", model=\"gpt2\")' && uvicorn app:app --host 0.0.0.0 --port 8000"]
