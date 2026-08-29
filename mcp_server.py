from mcp.server.fastmcp import FastMCP
import sqlite3

mcp = FastMCP("Coverage Assistant")

@mcp.tool()
def check_coverage(plan_id: str, procedure: str) -> str:
    """Check whether a procedure is covered under a specific insurance plan."""

    from retrieval_engine import vector_lookup

    context = vector_lookup(
        f"Is {procedure} covered under plan {plan_id}?"
    )

    conn = sqlite3.connect("coverage.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT plan_name FROM plans WHERE plan_id = ?",
        (plan_id,)
    )

    row = cursor.fetchone()
    conn.close()

    plan_name = row[0] if row else plan_id

    return f"Plan: {plan_name}\nProcedure: {procedure}\n\nPolicy context:\n{context}"

@mcp.tool()
def get_claim_status(claim_id: str) -> str:
    """Get the status and details of an insurance claim."""

    conn = sqlite3.connect("coverage.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM claims WHERE claim_id = ?",
        (claim_id,)
    )

    row = cursor.fetchone()
    conn.close()

    if not row:
        return f"No claim was found with ID {claim_id}."

    return str(row)

if __name__ == "__main__":
    mcp.run()