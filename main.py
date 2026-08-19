import time
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class CodeData(BaseModel):
    code: str

@app.get("/")
def home():
    return {"message": "AI Code Evaluator is running successfully!"}

@app.post("/analyze")
def analyze_code(data: CodeData):
    start_time = time.time()
    try:
        exec(data.code)
        execution_time = time.time() - start_time
        return {
            "status": "Success",
            "execution_time": f"{execution_time:.4f} seconds",
            "message": "Code executed successfully."
        }
    except Exception as e:
        return {
            "status": "Error",
            "message": str(e)
        }

