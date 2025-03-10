FROM python:3.9-slim

WORKDIR /app

# Install required packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Expose port for the API
EXPOSE 8000

# Pre-download the model to avoid first-request delay
RUN python -c "from transformers import AutoTokenizer, AutoModelForCausalLM; \
    tokenizer = AutoTokenizer.from_pretrained('gpt2'); \
    model = AutoModelForCausalLM.from_pretrained('gpt2')"

# Run the API server when the container starts
CMD ["python", "app.py"]
