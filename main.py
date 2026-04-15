from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import kaltum_agent

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    user_input: str

@app.get("/")
def home():
    return {"message": "Kaltum AI Agent is running 🚀"}

@app.get("/health")
def health():
    return {
        "status": "ok",
        "agent_loaded": kaltum_agent is not None
    }

# ✅ GET (browser testing)
@app.get("/chat")
def chat_get(user_input: str = "Hello"):
    response = kaltum_agent(user_input)
    return {"response": response}

# ✅ POST (frontend / production)
@app.post("/chat")
def chat(request: ChatRequest):
    response = kaltum_agent(request.user_input)
    return {"response": response}