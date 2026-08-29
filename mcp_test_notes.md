# MCP Test Notes

## Local Registration Test

**MCP server:** `coverage-assistant`

**Tool:** `check_coverage`

**Server file:** `mcp_server.py`

The MCP server was registered locally in Cline using the project's virtual-environment Python executable and `mcp_server.py`.

## Test 1

**Question:** Is physical therapy covered under the SILVER plan?

**Expected:** The MCP client should recognize the coverage question and call `check_coverage`.

**Observed:** The `check_coverage` tool was available to the MCP client and the coverage request was routed through the tool.

**Result:** PASS

## Test 2

**Question:** Is dental surgery covered under the SILVER plan?

**Expected:** The MCP client should call `check_coverage` with the SILVER plan and dental surgery as the procedure.

**Observed:** The coverage tool was available and returned policy context together with the plan information.

**Result:** PASS

## Conclusion

The local MCP server was successfully registered and exposed the `check_coverage` tool. Coverage questions could be routed to the MCP tool and returned with the available policy information.
