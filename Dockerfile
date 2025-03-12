FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TRANSFORMERS_CACHE=/app/model_cache

# Create model cache directory
RUN mkdir -p /app/model_cache

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download the model to avoid first-request delay
RUN python -c "from transformers import AutoTokenizer, AutoModelForCausalLM; \
    tokenizer = AutoTokenizer.from_pretrained('gpt2'); \
    model = AutoModelForCausalLM.from_pretrained('gpt2')"

# Copy application code
COPY app.py .

# Expose port for the API
EXPOSE 8000

# Run the API server with Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]