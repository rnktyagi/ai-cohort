from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from retrieval_engine import retrieve
from rag_chatbot import generate_answer
from memory.memory import save_message, get_history
from memory.token_count import count_tokens

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

    save_message(
        request.session_id,
        "user",
        request.message
    )

    session["messages"].append({
        "role": "user",
        "content": request.message
    })

    try:
        history = get_history(request.session_id, 10)

        history_text = "\n".join(
            f"{role}: {content}"
            for role, content in history
        )

        if count_tokens(history_text) > 2000:
            half = len(history) // 2
            oldest = history[:half]

            summary_prompt = f"""
Summarize this conversation briefly.
Keep important facts, especially the member's selected plan.

Conversation:
{oldest}
"""

            summary = ""

            for token in generate_answer("", summary_prompt):
                summary += token

            history_text = (
                f"Conversation summary:\n{summary}\n\n"
                + "\n".join(
                    f"{role}: {content}"
                    for role, content in history[half:]
                )
            )

        context = retrieve(request.message)

        def stream():
            answer = ""

            for token in generate_answer(
                request.message,
                f"Conversation history:\n{history_text}\n\nContext:\n{context}"
            ):
                answer += token
                yield f"data: {token}\n\n"

            save_message(
                request.session_id,
                "assistant",
                answer
            )

            session["messages"].append({
                "role": "assistant",
                "content": answer
            })

        return StreamingResponse(
            stream(),
            media_type="text/event-stream"
        )

    except Exception:
        return {
            "error": "Unable to generate an answer."
        }

@app.get("/history/{session_id}")
def get_session_history(session_id: str):
    history = get_history(session_id)

    return {
        "session_id": session_id,
        "conversation": [
            {
                "role": role,
                "content": content
            }
            for role, content in history
        ]
    }