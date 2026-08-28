import streamlit as st
import requests
import sqlite3
from uuid import uuid4

st.title("my-first-app")

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

conn = sqlite3.connect("../coverage.db")
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

prompt = st.chat_input("Ask a question :")

if prompt:
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.write(prompt)

    response = requests.post(
        "http://127.0.0.1:8000/chat",
        json={
            "session_id": st.session_state.session_id,
            "member_id": "M-1001",
            "message": prompt
        }
    )

    if response.status_code == 200:
        answer = response.json()["answer"]
    else:
        answer = "Unable to get a response from the server."

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    with st.chat_message("assistant"):
        st.write(answer)