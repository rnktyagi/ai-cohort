# Multi-Agent Comparison

## When Multi-Agent Is Worth It

Multi-agent architecture is useful when a system has genuinely different domains that need different expertise.

### Multi-agent helps

For example:

- Coverage questions → Coverage Specialist
- Claims questions → Claims Specialist
- Enrollment questions → Enrollment Specialist

A router can identify the domain and send the question to the correct specialist. This keeps each agent focused on its own tools and responsibilities.

### One agent is often enough

For simple questions within a single domain, a well-tooled agent is usually better.

Examples:

- Asking for a claim status
- Asking whether a procedure is covered
- Asking for basic plan details

Using multiple agents for these questions can add unnecessary complexity and extra LLM calls.

## Conclusion

Multi-agent systems are worth using when the domains are genuinely different and specialist handling provides a clear benefit.

For simple, single-domain questions, one well-tooled agent is usually enough and is easier to maintain.
