Chaos Test

Purpose

Test whether the multi-agent workflow handles an MCP tool failure without crashing.

Test Setup

The get_claim_status MCP tool was temporarily broken by changing its function name in mcp_server.py.

Test

Question: What is the status of claim CLM001?

Expected behavior: The MCP call should fail, retry once, and then return the fallback message.

Observed result:

The tool call failed as expected. After the retry, the system returned:

I'm having trouble accessing that right now, please contact member support

The application continued running and did not expose a raw exception or 500 error.

Result: PASS

Fix Verification

The original get_claim_status function name was restored.

The same claim question was run again.

Result: The MCP tool was reached successfully and returned the claim status.

Result: PASS