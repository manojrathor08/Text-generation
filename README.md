# Text Generation Service

A production-ready API service that generates text using a pretrained language model from Hugging Face.

## Overview

This service provides an HTTP API endpoint that accepts text prompts and returns generated text based on those prompts. It uses the GPT-2 model from OpenAI (via Hugging Face) for text generation.


## Getting Started

### Prerequisites

- Docker

### Building and Running

#### Pull the Docker image:

```bash
docker pull manojrathor08/text-generation-service
```

#### Run the container:

```bash
docker run -p 8000:8000 text-generation-service
```

The API will be available at http://localhost:8000.

Access the Swagger UI at: `http://localhost:8000/docs`


## API Usage

### Generate Text

**Endpoint**: `POST /generate`

**Request Body**:
```json
{
  "prompt": "Once upon a time",
  "max_length": 200
}
```

**Response**:
```json
{
  "generated_text": "Once upon a time there was a kingdom far away where dragons and princesses lived in harmony...",
  "prompt_tokens": 4,
  "completion_tokens": 14,
  "generation_time": 0.42
}
```

### Health Check

**Endpoint**: `GET /health`

**Response**:
```json
{
  "status": "healthy",
  "model": "gpt2",
  "max_prompt_length": 1000,
  "max_output_length": 500
}
```

## Configuration

The service uses GPT-2 by default, which is relatively small but capable. For better results but higher resource requirements, you can modify the `MODEL_NAME` in app.py to use other models like:

- `distilgpt2` (smaller, faster)
- `gpt2-medium` (larger, better quality)
- `EleutherAI/gpt-neo-125M` (modern alternative)

Remember to update the pre-download command in the Dockerfile if you change the model.

## Technical Details

- **Web Framework**: FastAPI for the API service
- **Model**: Hugging Face Transformers for text generation
- **Server**: Uvicorn ASGI server for production deployment
- **Containerization**: Docker for easy deployment

## Requirements

The following dependencies are required (see requirements.txt):

```
fastapi==0.103.1
uvicorn==0.23.2
transformers==4.34.0
torch==2.0.1
pydantic==2.4.2
numpy==1.26.3
```

## License

[MIT](LICENSE)
