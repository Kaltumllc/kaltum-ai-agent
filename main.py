from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import kaltum_agent

app = FastAPI()

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Request schema (THIS IS THE KEY)
class ChatRequest(BaseModel):
    user_input: str

@app.get("/")
def home():
    return {"message": "Kaltum AI Agent is running 🚀"}

# ✅ FIXED ENDPOINT (JSON BODY)
@app.post("/chat")
def chat(request: ChatRequest):
    response = kaltum_agent(request.user_input)
    return {"response": response}
