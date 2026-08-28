from fastapi import FastAPI
from pydantic import BaseModel

from retrieval_engine import retrieve
from rag_chatbot import generate_answer

app = FastAPI(title="FastAPI Health API")

sessions = {}

@app.get("/health")
def health():
    return {"status": "ok"}

class ChatRequest(BaseModel):
    session_id: str
    member_id: str
    message: str

@app.post("/chat")
def chat(request: ChatRequest):
    if request.session_id not in sessions:
        sessions[request.session_id] = {
            "member_id": request.member_id,
            "messages": []
        }

    session = sessions[request.session_id]

    session["messages"].append({
        "role": "user",
        "content": request.message
    })

    context = retrieve(request.message)

    try:
        answer = generate_answer(request.message, context)
        
    except Exception:
        return {"error": "Unable to generate an answer."}

    session["messages"].append({
        "role": "assistant",
        "content": answer
    })

    return {
        "session_id": request.session_id,
        "member_id": request.member_id,
        "answer": answer,
        "conversation": session["messages"]
    }

@app.get("/history/{session_id}")
def get_history(session_id: str):
    if session_id not in sessions:
        return {"session_id": session_id, "conversation": []}

    return {
        "session_id": session_id,
        "conversation": sessions[session_id]["messages"]
    }