# V2 Roadmap

## Priority 1 — Production-ready deployment

**Goal:** Make the Kubernetes deployment reproducible rather than dependent on manual local image transfer.

Tasks:

- Push versioned images to a container registry.
- Use immutable image tags instead of `latest`.
- Add a Kubernetes image-pull strategy.
- Add CI/CD for image builds and deployment.
- Add a staging environment before production.

**Compliance consideration:** Keep production secrets outside Git and use a managed secret store where appropriate.

---

## Priority 2 — Stronger member authorization

**Goal:** Move beyond pattern-based guardrails.

Tasks:

- Add real authentication.
- Associate authenticated identity with member records.
- Enforce authorization at the data-access layer.
- Prevent cross-member retrieval before data reaches the LLM.
- Audit sensitive data access.

**Compliance consideration:** Apply least privilege, minimize protected data exposure, retain audit records appropriately, and follow the organization's applicable privacy/security requirements.

---

## Priority 3 — Better retrieval quality

Tasks:

- Improve document chunking.
- Add metadata filtering by plan/member context.
- Add retrieval evaluation datasets.
- Measure precision/recall-style retrieval metrics.
- Add citation/source references to answers.
- Add automated regression tests for known policy questions.

---

## Priority 4 — LLM reliability and cost controls

Tasks:

- Add model fallback handling.
- Track token usage and cost centrally.
- Add request budgets and rate limits.
- Cache safe general coverage questions.
- Add structured output validation.
- Add timeout and retry policies.

---

## Priority 5 — Observability and alerting

Tasks:

- Expand Langfuse tracing to all important LLM operations.
- Track latency, errors, tokens, and cost.
- Create alerts for backend availability.
- Alert on abnormal LLM error rates.
- Alert on cost spikes.
- Add dashboards for request volume and latency.

---

## Priority 6 — User experience

Tasks:

- Improve plan-selection UX.
- Show source documents/chunks where appropriate.
- Add clearer error messages.
- Add conversation export.
- Add feedback buttons for answer quality.
- Improve accessibility and responsive layout.

---

## Priority 7 — Testing and engineering quality

Tasks:

- Unit tests for guardrails.
- Unit tests for retrieval.
- API integration tests.
- End-to-end frontend/backend smoke tests.
- Kubernetes deployment tests.
- Security tests for prompt injection and authorization bypasses.
- CI checks for secrets accidentally entering Git.

## V2 success criteria

A successful V2 should be:

- reproducibly deployable,
- observable,
- tested,
- cost-controlled,
- authorization-aware,
- resistant to cross-member data exposure,
- and suitable for a controlled production environment subject to the organization's compliance requirements.
