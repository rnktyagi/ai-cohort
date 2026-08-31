import streamlit as st
import requests
import sqlite3
from uuid import uuid4

st.title("my-first-app")

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

conn = sqlite3.connect("coverage.db")
cursor = conn.cursor()
cursor.execute("SELECT plan_name FROM plans")
plans = [row[0] for row in cursor.fetchall()]
conn.close()

with st.sidebar:
    st.header("Plan")

    selected_plan = st.selectbox(
        "Select your plan",
        plans
    )

    if st.button("New conversation"):
        st.session_state.session_id = str(uuid4())
        st.session_state.messages = []
        st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

        if message["role"] == "assistant" and message.get("chunk_ids"):
            with st.expander("Policy sources"):
                for chunk_id in message["chunk_ids"]:
                    st.write(f"- {chunk_id}")

prompt = st.chat_input("Ask a question :")

if prompt:
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        answer = ""
        chunk_ids = []

        try:
            with st.spinner("Thinking..."):
                response = requests.post(
                    "http://backend:8000/chat",
                    json={
                        "session_id": st.session_state.session_id,
                        "member_id": "M-1001",
                        "message": prompt
                    },
                    stream=True,
                    timeout=30
                )

                if response.status_code != 200:
                    raise Exception("Server error")

                for line in response.iter_lines():
                    if line:
                        line = line.decode("utf-8")

                        if line.startswith("data: "):
                            token = line[6:]
                            answer += token
                            placeholder.write(answer)

        except requests.exceptions.Timeout:
            answer = "The request timed out. Please try again."
            placeholder.write(answer)

        except requests.exceptions.RequestException:
            answer = "The connection was lost. Please try again."
            placeholder.write(answer)

        except Exception:
            answer = "Unable to generate an answer."
            placeholder.write(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "chunk_ids": chunk_ids
    })