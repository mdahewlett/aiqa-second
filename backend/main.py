import os
import openai
from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

load_dotenv()
PASSWORD = os.getenv("SITE_PASSWORD")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

openai.api_key = os.getenv("OPENAI_API_KEY")

class ChatRequest(BaseModel):
    query: str

@app.post("/chat")
def chat(request: ChatRequest, x_api_key: str = Header(None)):
    if x_api_key != PASSWORD:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    completion = openai.chat.completions.create(
        model="gpt-4.1-nano-2025-04-14",
        messages=[
            {
                "role":"user",
                "content": request.query
            }
        ]
    )
    message = completion.choices[0].message.content
    return {"response": message}

app.mount("/", StaticFiles(directory="dist", html=True), name="static")
