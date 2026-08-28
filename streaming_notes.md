# Streaming Notes

The Streamlit UI receives the response using `requests.post(..., stream=True)` and displays tokens as they arrive using `response.iter_lines()` and `st.empty()`.

A "Thinking..." spinner is shown while waiting for the first token.

If the connection times out or drops during streaming, the UI shows a user-friendly error message and does not crash the application.

The request timeout is set to 30 seconds.