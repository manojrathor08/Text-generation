# Text Generation Service

A simple API service that generates text using a pretrained language model from Hugging Face.

## Overview

This service provides an HTTP API endpoint that accepts text prompts and returns generated text based on those prompts. It uses the GPT-2 model from OpenAI (via Hugging Face) for text generation.

## Getting Started

### Prerequisites
- Docker

### Building and Running

1. Build the Docker image:
   ```bash
   docker build -t text-generation-service .
   ```

2. Run the container:
   ```bash
   docker run -p 8000:8000 text-generation-service
   ```

The API will be available at `http://localhost:8000`.

## API Usage

### Generate Text

**Endpoint:** `POST /generate`

**Request Body:**
```json
{
  "prompt": "Once upon a time",
  "max_length": 200
}
```

**Response:**
```json
{
  "generated_text": "Once upon a time there was a kingdom far away where dragons and princesses lived in harmony..."
}
```

### Health Check

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "model": "gpt2"
}
```

## Configuration

The service uses GPT-2, which is relatively small but capable. For better results but higher resource requirements, you can modify the `model_name` in `app.py` to use other models like:
- `distilgpt2` (smaller, faster)
- `gpt2-medium` (larger, better quality)
- `EleutherAI/gpt-neo-125M` (modern alternative)

Remember to update the pre-download command in the Dockerfile if you change the model.

## Technical Details

- Built with FastAPI for the web service
- Uses Hugging Face Transformers for the text generation model
- Containerized with Docker for easy deployment
