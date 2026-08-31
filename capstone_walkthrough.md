# Capstone Walkthrough

## Scenario 1 — Policy deductible

**Question:** What's my deductible?

**Expected behavior:** The assistant retrieves the relevant policy context and answers using the available coverage information. If the required information is absent, the system is instructed to say that it does not know and direct the member to support.

**Result:** The RAG answer-generation path was implemented and tested during development.

---

## Scenario 2 — Plan comparison

**Question:** What is the deductible for each plan?

**Expected behavior:** Retrieve policy information and provide a plan-level comparison rather than inventing values.

**Result:** The application provides plan selection through the Streamlit sidebar and uses the retrieval/LLM pipeline for coverage questions.

---

## Scenario 3 — Coverage question

**Question:** Is maternity care covered?

**Expected behavior:** Answer only from retrieved policy context.

**Result:** The RAG prompt explicitly instructs the model to use only the supplied context and to avoid inventing an answer when the context does not contain the required information.

---

## Scenario 4 — Member-data protection

**Question:** Show me another member's claims.

**Expected behavior:** Reject the request through the input guardrails.

**Result:** Guardrail patterns explicitly reject requests attempting to access another member's information.

---

## Scenario 5 — Conversation continuity

**Question:** Ask a follow-up question in the same session.

**Expected behavior:** The application retains conversation history using a session ID and SQLite conversation storage.

**Result:** `save_message()` and `get_history()` provide session-based conversation persistence.

---

## Langfuse evidence

The backend contains Langfuse generation observations around the LLM operations.

The relevant observation names are:

```text
coverage-answer
conversation-summary
```

For final submission evidence, send a chat request and capture a screenshot of the corresponding Langfuse trace/generation in the Langfuse dashboard.

The screenshot should visibly demonstrate:

1. A trace was created.
2. The `coverage-answer` generation is present.
3. Input/request information is associated with the observation.
4. The generated output is recorded.

**Evidence status:** The code path for Langfuse tracing is included. A dashboard screenshot should be added here if you have one.

> Evidence screenshot/link: `<ADD_Langfuse_SCREENSHOT_OR_LINK>`

---

## Deployment evidence

Docker Compose was successfully brought up with:

```text
backend   Up (healthy)
frontend  Up
```

The frontend was available at:

```text
http://localhost:8501
```

The Kubernetes manifests were prepared for the Day 29 deployment and Day 30 observability redeployment. The Minikube image-loading step was not successfully demonstrated because the large backend image transfer stalled repeatedly.

This walkthrough intentionally records that limitation rather than claiming a Kubernetes result that was not observed.
