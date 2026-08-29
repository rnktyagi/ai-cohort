import sqlite3
from datetime import datetime

DB_PATH = "coverage.db"

def save_message(session_id, role, content):
    conn = sqlite3.connect(DB_PATH)

    conn.execute(
        """
        INSERT INTO conversations
        (session_id, role, content, timestamp)
        VALUES (?, ?, ?, ?)
        """,
        (session_id, role, content, datetime.now().isoformat())
    )

    conn.commit()
    conn.close()

def get_history(session_id, limit=10):
    conn = sqlite3.connect(DB_PATH)

    rows = conn.execute(
        """
        SELECT role, content
        FROM conversations
        WHERE session_id = ?
        ORDER BY timestamp DESC
        LIMIT ?
        """,
        (session_id, limit)
    ).fetchall()

    conn.close()

    return list(reversed(rows))