import os
import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI(title="AI Code Reviewer API")

class CodeData(BaseModel):
    code: str
    language: str = "python"

@app.get("/")
def home():
    return {"message": "AI Code Evaluator is running successfully!"}

@app.post("/analyze")
def analyze_code(data: CodeData):
    start_time = time.time()
    
    api_key = os.environ.get("GROQ_API_KEY", "YOUR_GROQ_API_KEY")
    
    prompt = f"Review the following {data.language} code, find any bugs, and suggest improvements:\n\n{data.code}"
    
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
          "model": "gemma2-9b-it",

                "messages": [
                    {"role": "system", "content": "You are an expert code reviewer."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.2
            }
        )
        
        result = response.json()
        
        if "choices" in result:
            review_text = result["choices"][0]["message"]["content"]
            execution_time = time.time() - start_time
            return {
                "status": "Success",
                "execution_time": f"{execution_time:.4f} seconds",
                "review": review_text
            }
        else:
            return {
                "status": "Error",
                "message": result.get("error", {}).get("message", "Unknown API error")
            }
            
    except Exception as e:
        return {
            "status": "Error",
            "message": str(e)
        }
