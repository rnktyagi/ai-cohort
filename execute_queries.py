import sqlite3
import pandas as pd

conn = sqlite3.connect("coverage.db")

query1 = """
SELECT plan_name, annual_deductible
FROM plans
WHERE plan_name = 'Gold PPO';
"""

query2 = """
SELECT COUNT(*) AS pending_claims
FROM claims
WHERE member_id = 'M1001'
AND status = 'Pending';
"""

query3 = """
SELECT plan_name, monthly_premium
FROM plans
WHERE monthly_premium < 400
ORDER BY monthly_premium ASC;
"""

query4 = """
SELECT
    c.claim_id,
    c.member_id,
    c.procedure,
    c.claim_amount,
    c.status,
    p.plan_name,
    p.monthly_premium,
    p.annual_deductible
FROM claims c
JOIN plans p
ON c.plan_id = p.plan_id;
"""

query5 = """
SELECT
    procedure,
    COUNT(*) AS claim_count
FROM claims
GROUP BY procedure
ORDER BY claim_count DESC
LIMIT 5;
"""

print("QUERY 1")
print(query1)
print("OUTPUT 1")
print(pd.read_sql_query(query1, conn))

print("\nQUERY 2")
print(query2)
print("OUTPUT 2")
print(pd.read_sql_query(query2, conn))

print("\nQUERY 3")
print(query3)
print("OUTPUT 3")
print(pd.read_sql_query(query3, conn))

print("\nQUERY 4")
print(query4)
print("OUTPUT 4")
print(pd.read_sql_query(query4, conn))

print("\nQUERY 5")
print(query5)
print("OUTPUT 5")
print(pd.read_sql_query(query5, conn))

conn.close()