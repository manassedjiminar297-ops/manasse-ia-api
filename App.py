import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai

app = FastAPI()

openai.api_key = os.getenv("OPENAI_API_KEY")

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def home():
    return {"status": "API Manassé IA en ligne !"}

@app.post("/chat")
def chat(request: ChatRequest):
    if not openai.api_key:
        raise HTTPException(status_code=500, detail="Clé API OpenAI non configurée sur le serveur.")
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": request.message}]
        )
        return {"response": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
