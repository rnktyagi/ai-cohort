import sqlite3

conn = sqlite3.connect("coverage.db")

conn.execute("""
CREATE TABLE IF NOT EXISTS conversations (
    session_id TEXT,
    role TEXT,
    content TEXT,
    timestamp TEXT
)
""")

conn.commit()
conn.close()

print("conversations table created")