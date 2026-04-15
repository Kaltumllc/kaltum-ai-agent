import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import kaltum_agent, clear_session

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    user_input: str
    session_id: str = "default"

class ClearRequest(BaseModel):
    session_id: str = "default"

@app.get("/")
def home():
    return {"message": "Kaltum AI Agent v2 is running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/chat")
def chat_get(user_input: str = "Hello", session_id: str = "default"):
    try:
        response = kaltum_agent(user_input.strip(), session_id)
        return {"response": response, "session_id": session_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
def chat_post(request: ChatRequest):
    try:
        response = kaltum_agent(request.user_input, request.session_id)
        return {"response": response, "session_id": request.session_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/clear")
def clear(request: ClearRequest):
    clear_session(request.session_id)
    return {"message": "Session cleared."}