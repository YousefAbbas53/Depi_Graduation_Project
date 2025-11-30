import sqlite3
import json

class SQLChatHistory:
    def __init__(self, db_path="chat_history.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        # Create tables if they don't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chat_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                role TEXT,
                content TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()

    def add_message(self, session_id, role, content):
        """Save a message to SQL."""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO chat_messages (session_id, role, content) VALUES (?, ?, ?)",
            (session_id, role, content)
        )
        self.conn.commit()

    def get_history(self, session_id, limit=10):
        """
        Retrieve the last 'limit' messages formatted for the AI.
        Returns list: [{"role": "user", "content": "..."}, ...]
        """
        cursor = self.conn.cursor()
        # Order by DESC to get newest first, then reverse back to ASC for the AI
        cursor.execute("""
            SELECT role, content 
            FROM chat_messages 
            WHERE session_id = ? 
            ORDER BY id DESC 
            LIMIT ?
        """, (session_id, limit))
        
        rows = cursor.fetchall()
        # Reverse rows to maintain chronological order (Oldest -> Newest)
        history = [{"role": r[0], "content": r[1]} for r in reversed(rows)]
        return history


# 1. Setup
db = SQLChatHistory()
session_id = "user_123_session"
user_input = "Can you help me fix my SQL query?"

# 2. Save User Input
db.add_message(session_id, "user", user_input)

# 3. Get Context (Last 5 messages)
context = db.get_history(session_id, limit=5)

# 4. Call AI (Pseudo-code for OpenAI/Anthropic/Local LLM)
# response = model.generate(messages=context)
ai_reply = "Sure! Please paste the query you are working on." 

# 5. Save AI Response
db.add_message(session_id, "assistant", ai_reply)

print("History Updated!")