from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

try:
    from agent import kaltum_agent
except Exception as e:
    print("Agent import error:", e)
    kaltum_agent = None

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
    return {"status": "ok", "agent_loaded": kaltum_agent is not None}

@app.post("/chat")
def chat(request: ChatRequest):
    if not kaltum_agent:
        return {"response": "⚠️ AI not available"}

    try:
        response = kaltum_agent(request.user_input)
        return {"response": response}
    except Exception as e:
        return {"response": f"❌ Error: {str(e)}"}