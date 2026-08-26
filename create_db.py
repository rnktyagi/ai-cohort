import sqlite3
import pandas as pd

plans = pd.read_csv("data/plans.csv")
claims = pd.read_csv("data/claims.csv")

conn = sqlite3.connect("coverage.db")

plans.to_sql("plans", conn, if_exists="replace", index=False)
claims.to_sql("claims", conn, if_exists="replace", index=False)


conn.commit()
conn.close()