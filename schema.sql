-- 1. Store distinct conversations (Sessions)
CREATE TABLE chat_sessions (
    session_id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(50),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 2. Store the actual history (Messages)
CREATE TABLE chat_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- Use SERIAL for PostgreSQL
    session_id VARCHAR(50),
    role VARCHAR(10) CHECK(role IN ('user', 'assistant', 'system')),
    content TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES chat_sessions(session_id)
);