from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from agent import kaltum_agent

app = FastAPI()

# ✅ CORS FIX
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Kaltum AI Agent is running 🚀"}

@app.post("/chat")
def chat(user_input: str):
    response = kaltum_agent(user_input)
    return {"response": response}