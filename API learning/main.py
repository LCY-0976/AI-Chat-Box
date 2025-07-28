from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from ai import ai_response
app = FastAPI()

class TextInput(BaseModel):
    user_text: str
    role: str

# API endpoint
@app.post("/api/physicist")
async def get_physicist_response(data: TextInput):
    try:
        ai_result = ai_response(data.user_text, data.role)
        return {
            "original": data.user_text,
            "processed": ai_result
        }
    except Exception as e:
        return {"error": f"Failed to process request: {str(e)}"}

@app.post("/api/psychologist")
async def get_psychologist_response(data: TextInput):
    try:
        ai_result = ai_response(data.user_text, data.role)
        return {
            "original": data.user_text,
            "processed": ai_result
        }
    except Exception as e:
        return {"error": f"Failed to process request: {str(e)}"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)