# app.py
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field, validator
from transformers import pipeline, AutoTokenizer
import uvicorn
import logging
import time
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Text Generation API",
    description="API for generating text using Hugging Face models",
    version="1.0.0"
)

# Configuration
MAX_PROMPT_LENGTH = 1000
MAX_OUTPUT_LENGTH = 500
DEFAULT_MAX_LENGTH = 200
MODEL_NAME = "gpt2"

# Initialize model and tokenizer
try:
    logger.info(f"Loading model {MODEL_NAME}...")
    start_time = time.time()
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    generator = pipeline('text-generation', model=MODEL_NAME)
    logger.info(f"Model loaded successfully in {time.time() - start_time:.2f} seconds")
except Exception as e:
    logger.error(f"Failed to load model: {str(e)}")
    raise RuntimeError(f"Model initialization failed: {str(e)}")

class PromptRequest(BaseModel):
    prompt: str
    max_length: int = Field(
        default=DEFAULT_MAX_LENGTH,
        ge=10,
        le=MAX_OUTPUT_LENGTH,
        description="Maximum length of generated text"
    )
    
    @validator('prompt')
    def validate_prompt(cls, v):
        if not v.strip():
            raise ValueError("Prompt cannot be empty")
        if len(v) > MAX_PROMPT_LENGTH:
            raise ValueError(f"Prompt too long. Maximum is {MAX_PROMPT_LENGTH} characters")
        return v

class GenerationResponse(BaseModel):
    generated_text: str
    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None
    generation_time: Optional[float] = None

@app.get("/")
async def root():
    return {
        "message": "Welcome to the Text Generation API!",
        "docs": "/docs",
        "generate_endpoint": "/generate"
    }

@app.post("/generate", response_model=GenerationResponse)
async def generate_text(request: PromptRequest, background_tasks: BackgroundTasks):
    try:
        # Log request
        logger.info(f"Received generation request with prompt length: {len(request.prompt)}")
        
        # Tokenize to count tokens
        input_tokens = tokenizer.encode(request.prompt)
        if len(input_tokens) > MAX_PROMPT_LENGTH:
            raise HTTPException(
                status_code=400,
                detail=f"Prompt too long. Maximum is {MAX_PROMPT_LENGTH} tokens"
            )
        
        # Generate text with timing
        start_time = time.time()
        try:
            result = generator(
                request.prompt,
                max_length=min(request.max_length, MAX_OUTPUT_LENGTH),
                num_return_sequences=1,
                do_sample=True,
                temperature=0.7
            )
        except Exception as gen_error:
            logger.error(f"Generation error: {str(gen_error)}")
            raise HTTPException(
                status_code=500,
                detail=f"Text generation failed: {str(gen_error)}"
            )
        
        # Calculate time taken
        generation_time = time.time() - start_time
        
        # Extract result
        if isinstance(result[0], dict) and 'generated_text' in result[0]:
            generated_text = result[0]['generated_text']
        else:
            generated_text = result[0]
        
        # Calculate tokens
        output_tokens = len(tokenizer.encode(generated_text))
        prompt_tokens = len(input_tokens)
        completion_tokens = output_tokens - prompt_tokens
        
        # Log completion (asynchronously)
        background_tasks.add_task(
            logger.info,
            f"Generated {completion_tokens} tokens in {generation_time:.2f} seconds"
        )
        
        return GenerationResponse(
            generated_text=generated_text,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            generation_time=round(generation_time, 2)
        )
    
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except ValueError as ve:
        # Handle validation errors
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # Log unexpected errors
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred during text generation"
        )

@app.get("/health")
async def health_check():
    # Basic health check that verifies model is loaded
    return {
        "status": "healthy",
        "model": MODEL_NAME,
        "max_prompt_length": MAX_PROMPT_LENGTH,
        "max_output_length": MAX_OUTPUT_LENGTH
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)