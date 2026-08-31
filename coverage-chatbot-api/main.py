from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from retrieval_engine import retrieve
from rag_chatbot import generate_answer
from memory.memory import save_message, get_history
from guardrails_config import check_input
from token_utils import count_tokens

from langfuse import get_client, propagate_attributes

import csv
from datetime import datetime
import hashlib
import re
import time

app = FastAPI(title="FastAPI Health API")

langfuse = get_client()

sessions = {}
cache = {}
rate_limits = {}

MAX_REQUESTS = 10
WINDOW_SECONDS = 60


@app.get("/health")
def health():
    return {"status": "ok"}


class ChatRequest(BaseModel):
    session_id: str
    member_id: str
    message: str


def normalize_question(question):
    return re.sub(r"\s+", " ", question.strip().lower())


def get_cache_key(question):
    normalized = normalize_question(question)
    return hashlib.sha256(normalized.encode()).hexdigest()


def check_rate_limit(member_id):
    now = time.time()

    if member_id not in rate_limits:
        rate_limits[member_id] = []

    rate_limits[member_id] = [
        timestamp
        for timestamp in rate_limits[member_id]
        if now - timestamp < WINDOW_SECONDS
    ]

    if len(rate_limits[member_id]) >= MAX_REQUESTS:
        return False

    rate_limits[member_id].append(now)
    return True


def log_token_usage(session_id, input_tokens, output_tokens):
    input_rate = 0.001
    output_rate = 0.001

    estimated_cost = (
        (input_tokens / 1000) * input_rate
        + (output_tokens / 1000) * output_rate
    )

    with open("token_usage.csv", "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            session_id,
            datetime.now().isoformat(),
            input_tokens,
            output_tokens,
            estimated_cost
        ])


def traced_generate_answer(question, context, session_id, member_id, name):
    """
    Wrap the existing streaming LLM call in a Langfuse generation observation.
    The actual provider call remains inside rag_chatbot.generate_answer().
    """
    answer = ""

    with propagate_attributes(
        user_id=member_id,
        session_id=session_id,
        metadata={"service": "coverage-chatbot-api"},
    ):
        with langfuse.start_as_current_observation(
            as_type="generation",
            name=name,
            model="openai/gpt-oss-20b",
            input={
                "question": question,
                "context": context,
            },
        ) as generation:
            try:
                for token in generate_answer(question, context):
                    answer += token
                    yield token

                generation.update(
                    output=answer,
                    metadata={"output_tokens": count_tokens(answer)},
                )
            except Exception as exc:
                generation.update(
                    output={"error": str(exc)},
                    metadata={"status": "error"},
                )
                raise
            finally:
                langfuse.flush()


@app.post("/chat")
def chat(request: ChatRequest):
    if not check_input(request.message):
        return {
            "error": "Your message contains disallowed content. Please rephrase your request."
        }

    if not check_rate_limit(request.member_id):
        return {
            "error": "Too many requests. Please try again later."
        }

    if request.session_id not in sessions:
        sessions[request.session_id] = {
            "member_id": request.member_id,
            "messages": []
        }

    session = sessions[request.session_id]
    cache_key = get_cache_key(request.message)

    general_coverage = any(
        word in request.message.lower()
        for word in [
            "coverage",
            "covered",
            "deductible",
            "copay",
            "premium"
        ]
    )

    member_specific = any(
        word in request.message.lower()
        for word in [
            "claim",
            "member",
            "my claim",
            "claim id"
        ]
    )

    if general_coverage and not member_specific and cache_key in cache:
        return StreamingResponse(
            iter([f"data: {cache[cache_key]}\n\n"]),
            media_type="text/event-stream"
        )

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

            for token in traced_generate_answer(
                "",
                summary_prompt,
                request.session_id,
                request.member_id,
                "conversation-summary",
            ):
                summary += token

            history_text = (
                f"Conversation summary:\n{summary}\n\n"
                + "\n".join(
                    f"{role}: {content}"
                    for role, content in history[half:]
                )
            )

        context = retrieve(request.message)

        prompt = (
            f"Conversation history:\n{history_text}\n\n"
            f"Context:\n{context}\n\n"
            f"Question:\n{request.message}"
        )

        def stream():
            answer = ""

            for token in traced_generate_answer(
                request.message,
                prompt,
                request.session_id,
                request.member_id,
                "coverage-answer",
            ):
                answer += token
                yield f"data: {token}\n\n"

            input_tokens = count_tokens(prompt)
            output_tokens = count_tokens(answer)

            log_token_usage(
                request.session_id,
                input_tokens,
                output_tokens
            )

            if general_coverage and not member_specific:
                cache[cache_key] = answer

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
