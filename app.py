# app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline
import uvicorn

app = FastAPI(title="Text Generation API")

# Select a small but capable text generation model
model_name = "gpt2"
generator = pipeline('text-generation', model=model_name)

@app.get("/")
async def root():
    return {"message": "Welcome to the Text Generation API! Use /generate to generate text."}


class PromptRequest(BaseModel):
    prompt: str
    max_length: int = 200  # Default max length for generated text

class GenerationResponse(BaseModel):
    generated_text: str

@app.post("/generate", response_model=GenerationResponse)
async def generate_text(request: PromptRequest):
    try:
        # Ensure the prompt isn't empty
        if not request.prompt.strip():
            raise HTTPException(status_code=400, detail="Prompt cannot be empty")
        
        # Generate text based on the prompt
        result = generator(
            request.prompt, 
            max_length=request.max_length, 
            num_return_sequences=1
        )
        
        # Extract the generated text from the result
        generated_text = result[0]['generated_text']
        
        return GenerationResponse(generated_text=generated_text)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Text generation failed: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model": model_name}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)